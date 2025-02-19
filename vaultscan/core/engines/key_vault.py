
from typing import List, Dict
from dataclasses import dataclass, fields
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from vaultscan.core.engines.base import (
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
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


class KeyVaultSecretEngine(BaseVaultEngine):
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
