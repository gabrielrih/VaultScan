from typing import Dict, List
from dataclasses import dataclass

from vaultscan.engines.base import (
    EngineType,
    BaseVaultConfig,
    BaseVaultEngine
)


@dataclass
class KeePassConfig(BaseVaultConfig):
    path: str
    password: str

    def __post_init__(self):
        self.type = EngineType.KEYPASS.value
        return super().__post_init__()
    
    @classmethod
    def from_list(cls, content: List[Dict]) -> List['KeePassConfig']:
        vaults = list()
        for vault in content:
            vaults.append(
                KeePassConfig.from_dict(vault)
            )
        return vaults

    @classmethod
    def from_dict(cls, content: Dict) -> 'KeePassConfig':
        return KeePassConfig(
            alias = content['alias'],
            path = content['path'],
            password = content['password']
        )


class KeepassSecretEngine(BaseVaultEngine):
    pass
