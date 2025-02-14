from dataclasses import dataclass

from vaultscan.engines.base import (
    EngineType,
    BaseVaultConfig
)


@dataclass
class KeyVaultConfig(BaseVaultConfig):
    subscription_id: str
    resource_group_name: str
    vault_name: str

    def __post_init__(self):
        self.type = EngineType.AZURE_KEY_VAULT.value
        return super().__post_init__()
