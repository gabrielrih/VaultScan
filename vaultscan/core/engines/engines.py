from enum import Enum

from vaultscan.core.engines.base import BaseVaultConfig, BaseVaultEngine
from vaultscan.core.engines.key_vault import AZURE_KEY_VAULT, KeyVaultConfig, KeyVaultSecretEngineProvider
from vaultscan.core.engines.keepass import KEEPASS, KeePassConfig, KeePassSecretEngine


class AvailableEngines(Enum):
    AZURE_KEY_VAULT = (AZURE_KEY_VAULT, KeyVaultConfig, KeyVaultSecretEngineProvider.create())
    KEEPASS = (KEEPASS, KeePassConfig, KeePassSecretEngine)

    def __init__(self, type: str, config: BaseVaultConfig, engine: BaseVaultEngine):
        super().__init__()
        self.type = type
        self.config = config
        self.engine = engine

    @classmethod
    def from_type(cls, type: str) -> 'AvailableEngines':
        try:
            return next(e for e in cls if e.type == type)
        except StopIteration:
            raise ValueError(f'Vault type not valid or not specified {type}')
