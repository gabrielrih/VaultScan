from enum import Enum, auto

from vaultscan.repositories.config.base import ConfigRepository
from vaultscan.repositories.config.json import ConfigRepositoryAsJson
from vaultscan.repositories.config.in_memory import InMemoryConfigRepository
from vaultscan.repositories.file_handler import JSONFileHandler


class ConfigRepositoryType(Enum):
    JSON = auto()
    IN_MEMORY = auto()


class ConfigRepositoryFactory:
    @staticmethod
    def create(type: ConfigRepositoryType = ConfigRepositoryType.JSON) -> ConfigRepository:
        if type == ConfigRepositoryType.JSON:
            file = JSONFileHandler(folder_name = '.vaultscan', filename = 'configs.json')
            return ConfigRepositoryAsJson(file)
        if type == ConfigRepositoryType.IN_MEMORY:
            return InMemoryConfigRepository()
        raise ValueError(f'The specified ConfigRepositoryType {type} is not valid!')
