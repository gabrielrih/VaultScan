
from typing import List, Dict
from dataclasses import dataclass

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from vaultscan.engines.base import (
    EngineType,
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

    def find_by_regex(self, secret_name: str) -> List[Secret]:
        secret_name = secret_name.lower()
        secrets = list()
        raw_secrets: List[str] = self.client.get_all_secrets()
        secrets = [
            Secret(vault = self.vault.alias, name = raw_secret)
            for raw_secret in raw_secrets
            if secret_name in raw_secret.lower()
        ]
        logger.debug(f'{len(secrets)} secrets found on KV {self.vault.alias} mathing the regex {secret_name}')
        return secrets

    def find_by_name(self, secret_name: str) -> List[Secret]:
        secret_name = secret_name.lower()
        secrets = list()
        raw_secrets: List[str] = self.client.get_all_secrets()
        secrets = [
            Secret(vault = self.vault.alias, name = raw_secret)
            for raw_secret in raw_secrets
            if secret_name == raw_secret.lower()
        ]
        logger.debug(f'{len(secrets)} secrets found on KV {self.vault.alias} mathing the regex {secret_name}')
        return secrets


class KeyVaultSecretAPI:
    def __init__(self, vault_name: str):
        self.vault_name = vault_name
        self.client = SecretClient(
            vault_url = f"https://{vault_name}.vault.azure.net",
            credential = DefaultAzureCredential()
        )
        
    def get_all_secrets(self) -> List[str]:
        return [ secret.name for secret in self.client.list_properties_of_secrets() ]
