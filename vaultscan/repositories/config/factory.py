from enum import Enum, auto

from vaultscan.repositories.config.base import ConfigRepository
from vaultscan.repositories.config.json import ConfigRepositoryAsJson


class ConfigRepositoryType(Enum):
    JSON = auto()


class ConfigRepositoryFactory:
    @staticmethod
    def create(type: ConfigRepositoryType = ConfigRepositoryType.JSON) -> ConfigRepository:
        if type == ConfigRepositoryType.JSON:
            return ConfigRepositoryAsJson()
        raise ValueError(f'The specified ConfigRepositoryType {type} is not valid!')
