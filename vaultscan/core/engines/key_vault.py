import concurrent.futures

from typing import List, Dict, Type
from dataclasses import dataclass, fields
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError

from vaultscan.core.engines.base import (
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
from vaultscan.core.cache.singleton import CacheManagerSingleton
from vaultscan.core.configs import AvailableConfigs, ConfigManager
from vaultscan.core.output.logger import LoggerFactory
from vaultscan.repositories.vault.base import VaultStatus


logger = LoggerFactory.get_logger(__name__)


AZURE_KEY_VAULT = 'key_vault'


@dataclass
class KeyVaultConfig(BaseVaultConfig):
    vault_name: str

    def __post_init__(self):
        self.type = AZURE_KEY_VAULT
        return super().__post_init__()
    
    @classmethod
    def from_dict(cls, content: Dict) -> 'KeyVaultConfig':
        kwargs = {}
        for f in fields(cls):
            if f.name == 'type':  # skip 'type" to prevent TypeError
                continue
            value = content.get(f.name)
            if f.name == 'status':
                value = VaultStatus(value)
            kwargs[f.name] = value
        return cls(**kwargs)


ENABLE_CONCURRENCY: bool = ConfigManager(
    AvailableConfigs.ENABLE_CONCURRENCY
).get_value()  # getting it from user configuration
class KeyVaultSecretEngineProvider:
    @staticmethod
    def create() -> Type[BaseVaultEngine]:
        if ENABLE_CONCURRENCY:
            return KeyVaultSecretEngineConcurrent
        return KeyVaultSecretEngine


class KeyVaultSecretEngine(BaseVaultEngine):
    '''' Vault implementation for the Azure Key Vault engine '''
    def __init__(self, vault: KeyVaultConfig):
        super().__init__(vault)
        self.client = KeyVaultSecretClient(vault_name = vault.vault_name)

    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]:
        filter = filter.lower()  # normalize the filter
        response = list()
        secrets: List[str] = self.client.get_all_secrets()
        for name in secrets:
            name = name.lower()  # normalize the secret name
            if filter:
                if not self.is_match([ name ], filter, type):
                    continue
            value = ''
            if is_value:
                try:
                    value = self.client.get_value(name)
                except Exception as exc:
                    # it may happen if the secret is deleted when it's being processing
                    # in this case it prints the error and then ignores the secret
                    logger.warning("Error fetching value from secret %r: %s", name, exc)
                    continue
            response.append(
                Secret(
                    vault = self.vault.alias,
                    name = name,
                    value = value
                )
            )
        return response


class KeyVaultSecretEngineConcurrent(BaseVaultEngine):
    '''' Vault implementation for the Azure Key Vault engine (using concurrent) '''
    def __init__(self, vault: KeyVaultConfig):
        super().__init__(vault)
        self.client = KeyVaultSecretClient(vault_name = vault.vault_name)

    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]:
        # Fetching all the secrets on the vault (without filter)
        secrets: List[str] = self.client.get_all_secrets()

        if filter:
            # Filtering secret names based on your matching function.
            # This reduces the set that may need the expensive "get_value" call.
            filter = filter.lower()  # normalize the filter
            matching_secrets = [ 
                secret_name for secret_name in secrets
                if self.is_match([ secret_name.lower() ], filter, type) 
            ]
        else:
            # no filter, so add all secrets
            matching_secrets = secrets

        # Return secrets without its value
        response = list()
        if not is_value:
            response = [
                Secret(vault = self.vault.alias, name = secret_name)
                for secret_name in matching_secrets
            ]
            return response

        # Return secrets with its value
        with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
            future_to_name = { executor.submit(self._fetch_secret_with_its_value, secret_name): secret_name for secret_name in matching_secrets }
            for future in concurrent.futures.as_completed(future_to_name):
                try:
                    response.append(future.result())
                except Exception as exc:
                    logger.error("Error fetching secret %r: %s", future_to_name[future], exc)
        return response

    def _fetch_secret_with_its_value(self, secret_name: str) -> Secret:
        value = self.client.get_value(secret_name)
        return Secret(
            vault = self.vault.alias,
            name = secret_name,
            value = value
        )


CACHE_ENABLED: bool = ConfigManager(
    AvailableConfigs.CACHE_ENABLED
).get_value()
class KeyVaultSecretClient:
    def __init__(self, vault_name: str):
        self.vault_name = vault_name
        self.cache = CacheManagerSingleton.get_instance() if CACHE_ENABLED else None
        self.client = SecretClient(
            vault_url = f"https://{vault_name}.vault.azure.net",
            credential = DefaultAzureCredential()
        )

    def get_all_secrets(self) -> List[str]:
        cache_key = f"keyvault:{self.vault_name}:secrets"
        
        if self.cache and self.cache.exists(cache_key):
            return self.cache.get(cache_key)

        logger.debug(f"Fetching secret names from Azure KV: {self.vault_name}")
        secrets = []
        is_first = True
        for secret in self.client.list_properties_of_secrets():
            if is_first:
                logger.info(secret.updated_on)
                logger.info(secret.created_on)
                is_first = False
            logger.info(secret.updated_on)
            secrets.append(secret.name)
        #secrets: List[str] = [ secret.name for secret in self.client.list_properties_of_secrets() ]
        if self.cache:
            self.cache.set(cache_key, secrets)
        
        return secrets

    def get_value(self, secret_name: str) -> str:
        logger.debug(f'Getting the latest value for {secret_name =} on {self.vault_name =}')
        try:
            secret = self.client.get_secret(secret_name)
            return str(secret.value)
        except ResourceNotFoundError:
            raise KeyVaultSecretNotFound(f'Secret "{secret_name}" not found in vault "{self.vault_name}"')
        except ClientAuthenticationError as e:
            raise RuntimeError(f'Authentication failed when accessing Key Vault "{self.vault_name}"') from e


class KeyVaultSecretNotFound(Exception):
    pass
