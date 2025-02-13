from enum import Enum, auto

from vaultscan.repository.common import VaultRepository
from vaultscan.repository.json import VaultRepositoryAsJson


class VaultRepositoryType(Enum):
    JSON = auto()


class VaultRepositoryFactory:
    @staticmethod
    def create(type: VaultRepositoryType = VaultRepositoryType.JSON) -> VaultRepository:
        if type == VaultRepositoryType.JSON:
            return VaultRepositoryAsJson()
        raise ValueError(f'The specified VaultRepositoryType {type} is not valid!')
