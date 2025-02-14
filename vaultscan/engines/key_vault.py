
from typing import List, Dict
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from vaultscan.engines.base import (
    EngineType,
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


@dataclass
class KeyVaultConfig(BaseVaultConfig):
    subscription_id: str
    resource_group_name: str
    vault_name: str

    def __post_init__(self):
        self.type = EngineType.AZURE_KEY_VAULT.value
        return super().__post_init__()
    
    @classmethod
    def from_list(cls, content: List[Dict]) -> List['KeyVaultConfig']:
        vaults = list()
        for vault in content:
            vaults.append(
                KeyVaultConfig.from_dict(vault)
            )
        return vaults

    @classmethod
    def from_dict(cls, content: Dict) -> 'KeyVaultConfig':
        return KeyVaultConfig(
            alias = content['alias'],
            subscription_id = content['subscription_id'],
            resource_group_name = content['resource_group_name'],
            vault_name = content['vault_name']
        )


class KeyVaultSecretEngine(BaseVaultEngine):
    def __init__(self, vault: KeyVaultConfig):
        super().__init__(vault)
        self.client = KeyVaultSecretAPI(vault_name = vault.vault_name)

    def find(self, filter: str, type: FilterType, is_value = False):
        filter = filter.lower()  # normalize the filter
        response = list()
        secrets: List[str] = self.client.get_all_secrets()
        for name in secrets:
            if not self._is_match(name, filter, type):
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

    def _is_match(self, secret_name: str, filter: str, type: FilterType) -> bool:
        if type == FilterType.BY_MATCH:
            return filter == secret_name
        if type == FilterType.BY_REGEX:
            return filter in secret_name
        raise ValueError(f'Invalid FilterType {str(type)}!')


class KeyVaultSecretAPI:
    def __init__(self, vault_name: str):
        self.vault_name = vault_name
        self.client = SecretClient(
            vault_url = f"https://{vault_name}.vault.azure.net",
            credential = DefaultAzureCredential()
        )
        
    def get_all_secrets(self) -> List[str]:
        return [ secret.name for secret in self.client.list_properties_of_secrets() ]

    def get_value(self, secret_name: str) -> str:
        logger.debug(f'Getting value for {secret_name =}')
        secret = self.client.get_secret(secret_name)
        return str(secret.value)
