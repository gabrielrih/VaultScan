from typing import Dict, List
from dataclasses import dataclass

from vaultscan.engines.base import (
    FilterType,
    BaseVaultConfig,
    BaseVaultEngine,
    Secret
)
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


@dataclass
class KeePassConfig(BaseVaultConfig):
    path: str
    password: str

    def __post_init__(self):
        self.type = 'keepass' # FIX IT: From engines.py?
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
    def __init__(self, vault: KeePassConfig):
        super().__init__(vault)

    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]:
        return list()
