from enum import Enum, auto

from vaultscan.repositories.vault.base import VaultRepository
from vaultscan.repositories.vault.json import VaultRepositoryAsJson


class VaultRepositoryType(Enum):
    JSON = auto()


class VaultRepositoryFactory:
    @staticmethod
    def create(type: VaultRepositoryType = VaultRepositoryType.JSON) -> VaultRepository:
        if type == VaultRepositoryType.JSON:
            return VaultRepositoryAsJson()
        raise ValueError(f'The specified VaultRepositoryType {type} is not valid!')
