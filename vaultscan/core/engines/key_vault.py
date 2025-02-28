import concurrent.futures

from typing import List, Dict, Type
from dataclasses import dataclass, fields
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from vaultscan.core.engines.base import (
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
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
            if not self.is_match([ name ], filter, type):
                continue
            value = ''
            if is_value:
                value = self.client.get_value(name)
            response.append(
                Secret(
                    vault = self.vault.alias,
                    name = name,
                    value = value
                )
            )
        logger.debug(f'{len(response)} secrets found on KV {self.vault.alias} mathing the regex {filter}')
        return response


class KeyVaultSecretEngineConcurrent(BaseVaultEngine):
    '''' Vault implementation for the Azure Key Vault engine (using concurrent) '''
    def __init__(self, vault: KeyVaultConfig):
        super().__init__(vault)
        self.client = KeyVaultSecretClient(vault_name = vault.vault_name)

    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]:
        # Fetching all the secrets on the vault (without filter)
        secrets: List[str] = self.client.get_all_secrets()

        # Filtering secret names based on your matching function.
        # This reduces the set that may need the expensive "get_value" call.
        filter = filter.lower()  # normalize the filter
        matching_secrets = [ secret_name for secret_name in secrets if self.is_match([ secret_name.lower() ], filter, type) ]

        # Return secrets without its value
        response = list()
        if not is_value:
            response = [
                Secret(
                    vault = self.vault.alias,
                    name = secret_name
                )
                for secret_name in matching_secrets
            ]
            logger.debug(f'{len(response)} secrets found on KV {self.vault.alias} mathing the regex {filter}')
            return response

        # Return secrets with its value
        with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
            future_to_name = { executor.submit(self._fetch_secret_with_its_value, secret_name): secret_name for secret_name in matching_secrets }
            for future in concurrent.futures.as_completed(future_to_name):
                try:
                    response.append(future.result())
                except Exception as exc:
                    logger.error("Error fetching secret %r: %s", future_to_name[future], exc)
        logger.debug(f'{len(response)} secrets found on KV {self.vault.alias} mathing the regex {filter}')
        return response
    
    def _fetch_secret_with_its_value(self, secret_name: str) -> Secret:
        value = self.client.get_value(secret_name)
        return Secret(
            vault = self.vault.alias,
            name = secret_name,
            value = value
        )


class KeyVaultSecretClient:
    def __init__(self, vault_name: str):
        self.vault_name = vault_name
        self.client = SecretClient(
            vault_url = f"https://{vault_name}.vault.azure.net",
            credential = DefaultAzureCredential()
        )

    def get_all_secrets(self) -> List[str]:
        return [ secret.name for secret in self.client.list_properties_of_secrets() ]

    def get_value(self, secret_name: str) -> str:
        logger.debug(f'Getting value for {secret_name =} on {self.vault_name =}')
        secret = self.client.get_secret(secret_name)
        return str(secret.value)
