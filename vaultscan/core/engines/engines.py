from enum import Enum

from vaultscan.core.engines.base import BaseVaultConfig, BaseVaultEngine
from vaultscan.core.engines.key_vault import AZURE_KEY_VAULT, KeyVaultConfig, KeyVaultSecretEngine
from vaultscan.core.engines.keepass import KEEPASS, KeePassConfig, KeePassSecretEngine


class AvailableEngines(Enum):
    AZURE_KEY_VAULT = (AZURE_KEY_VAULT, KeyVaultConfig, KeyVaultSecretEngine)
    KEEPASS = (KEEPASS, KeePassConfig, KeePassSecretEngine)

    def __init__(self, type: str, config: BaseVaultConfig, engine: BaseVaultEngine):
        super().__init__()
        self.type = type
        self.config = config
        self.engine = engine


def get_engine_from_type(type: str) -> AvailableEngines:
    if type == AvailableEngines.AZURE_KEY_VAULT.type:
        return AvailableEngines.AZURE_KEY_VAULT
    if type == AvailableEngines.KEEPASS.type:
        return AvailableEngines.KEEPASS
    raise ValueError(f'Vault type not valid or not specified {type}')
