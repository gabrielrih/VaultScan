
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


logger = LoggerFactory.get_logger()


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
        secrets = list()
        raw_secrets: List[str] = self.client.get_secrets()
        for raw_secret in raw_secrets:
            secrets.append(
                Secret(
                    vault_alias = self.vault.alias,
                    secret_name = raw_secret
                )
            )
        logger.verbose(str(secrets))
        return secrets

    def find_by_name(self, secret_name: str) -> List[Secret]:
        return get_fake_secrets()



class KeyVaultSecretAPI:
    def __init__(self, vault_name: str):
        self.vault_name = vault_name
        self.client = SecretClient(
            vault_url = f"https://{vault_name}.vault.azure.net",
            credential = DefaultAzureCredential()
        )
        
    def get_secrets(self) -> List[str]:
        return [ secret.name for secret in self.client.list_properties_of_secrets() ]


def get_fake_secrets() -> List[Secret]:
    secrets = list()
    secrets.append(
        Secret(
            vault_alias = 'vault1',
            secret_name = 'my_secret_1'
        ))
    secrets.append(
        Secret(
            vault_alias = 'vault1',
            secret_name = 'other'
        ))
    secrets.append(
        Secret(
            vault_alias = 'other_vault',
            secret_name = 'kkk'
        ))
    return secrets
