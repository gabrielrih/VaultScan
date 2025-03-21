from enum import Enum, auto

from vaultscan.repositories.vault.base import VaultRepository
from vaultscan.repositories.vault.json import VaultRepositoryAsJson
from vaultscan.repositories.file_handler import JSONFileHandler


class VaultRepositoryType(Enum):
    JSON = auto()


class VaultRepositoryFactory:
    @staticmethod
    def create(type: VaultRepositoryType = VaultRepositoryType.JSON) -> VaultRepository:
        if type == VaultRepositoryType.JSON:
            file = JSONFileHandler(folder_name = '.vaultscan', filename = 'vaults.json')
            return VaultRepositoryAsJson(file = file)
        raise ValueError(f'The specified VaultRepositoryType {type} is not valid!')
