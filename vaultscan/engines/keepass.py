from dataclasses import dataclass

from vaultscan.engines.base import (
    EngineType,
    BaseVaultConfig
)


@dataclass
class KeePassConfig(BaseVaultConfig):
    path: str
    password: str

    def __post_init__(self):
        self.type = EngineType.KEYPASS.value
        return super().__post_init__()
