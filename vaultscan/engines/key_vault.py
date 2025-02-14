from typing import List, Dict
from dataclasses import dataclass

from vaultscan.engines.base import (
    EngineType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)


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

    def find_by_regex(self, secret_name: str) -> List[Secret]:
        return get_fake_secrets()

    def find_by_name(self, secret_name: str) -> List[Secret]:
        return get_fake_secrets()



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
