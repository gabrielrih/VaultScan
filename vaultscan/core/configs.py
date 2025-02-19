from enum import Enum
from typing import List, Any, Type, Optional

from vaultscan.repositories.config.base import Config, ConfigRepository
from vaultscan.repositories.config.factory import ConfigRepositoryFactory


class OutputFormatConfig(Enum):
    JSON = "json"
    TABLE = "table"
    STANDARD = "standard"

    @classmethod
    def get_values(cls) -> List[str]:
        return [ e.value for e in cls ]


class AvailableConfigs(Enum):
    ''' 
        Enum to define available configurations 

        The "value_type" must be the actual type to be used INSIDE THE CODE.
            Example, if the config is using an Enum, the value_type should be the class.
            If the values are True or False, the value_type should be bool.

        The "config_name", "default_value" and "possible_values" should be in a STRING format even if the value_type is not a string.
            It's important because this parameters are used by user (by typing it).
    '''
    VERBOSE = ('verbose', bool, 'False', [ 'True', 'False' ])
    OUTPUT_FORMAT = ('output_format', OutputFormatConfig, OutputFormatConfig.JSON.value, OutputFormatConfig.get_values())

    def __init__(self, config_name: str, value_type: Type, default_value: str, possible_values: List[str]):
        self.config_name: str = config_name
        self.value_type: Type = value_type
        self.default_value: str = default_value
        self.possible_values: List[str] = possible_values

    @classmethod
    def get_values(cls) -> List[str]:
        return [ config.config_name for config in AvailableConfigs ]

    @staticmethod
    def from_config_name(config_name: str) -> 'AvailableConfigs':
        """ Find an AvailableConfigs enum by name """
        for config in AvailableConfigs:
            if config.config_name == config_name:
                return config
        ''' It should never happen because the click.Choice are loading the right configs, but... '''
        raise ConfigNotFoundError(
            f'Configuration "{config_name}" not found in {AvailableConfigs.__name__}'
        )


class ConfigNotFoundError(Exception):
    ''' Raised when a configuration is not found '''
    pass


class ConfigManager:
    ''' Handles reading config values '''
    def __init__(self, config: AvailableConfigs, repository: ConfigRepository = ConfigRepositoryFactory.create()):
        self.config = config
        self.repository = repository

    def get_value(self) -> Any:
        ''' Get the value of the given config, falling back to the default '''
        custom_config: Optional[Config] = self._get_custom_config()
        if not custom_config:
            return ConfigManager._convert_to_type(
                value = self.config.default_value,
                value_type = self.config.value_type
            )
        return ConfigManager._convert_to_type(
            value = custom_config.value,
            value_type = self.config.value_type
        )
    
    def get_value_as_string(self) -> str:
        ''' It returns the value in string format (usefull to parse as json) '''
        custom_config: Optional[Config] = self._get_custom_config()
        if custom_config:
            return str(custom_config.value)
        return str(self.config.default_value)

    def _get_custom_config(self) -> Optional[Config]:
        ''' Retrieve custom configuration from repository '''
        custom_config = self.repository.get(name = self.config.config_name)
        return Config.from_dict(custom_config) if custom_config else None
    
    @staticmethod
    def _convert_to_type(value: str, value_type: Type) -> Any:
        ''' Convert a string value to the appropriate type '''
        if issubclass(value_type, bool):
            return value.lower() == 'true'
        return value_type(value)


class ConfigValidator:
    """ Handles validation of configuration values """
    @classmethod
    def is_a_valid_value(cls, config: AvailableConfigs, value: str) -> bool:
        """ Check if the given value is allowed for the specified config """
        return value in config.possible_values
