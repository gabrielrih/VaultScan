from enum import Enum
from typing import List, Any, Type, Optional

from vaultscan.repositories.config.base import Config
from vaultscan.repositories.config.factory import ConfigRepositoryFactory


repository = ConfigRepositoryFactory.create()


class OutputFormatConfig(Enum):
    JSON = "json"
    TABLE = "table"
    STANDARD = "standard"

    @classmethod
    def get_values(cls) -> List[str]:
        return [e.value for e in cls]


class AvailableConfigs(Enum):
    ''' 
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

    def to_right_type(self, value: str) -> Any:
        ''' Receive the value in string format and convert it to the right value_type '''
        if isinstance(self.value_type, bool):
            return value.lower() in ['true']
        return self.value_type(value)
    
    @property
    def value(self) -> Any:
        ''' It returns the value using its original datatype (field value_type) '''
        custom_config: Optional[Config] = get_custom_config_by_name(self.config_name)
        if not custom_config:
            return self.to_right_type(self.default_value)
        return self.to_right_type(value = custom_config.value)
    
    @property
    def value_as_string(self) -> str:
        ''' It returns the value in string format (usefull to parse as json) '''
        custom_config: Optional[Config] = get_custom_config_by_name(self.config_name)
        if not custom_config:
            return str(self.default_value)
        return str(custom_config.value)


def get_custom_config_by_name(config_name: str) -> Optional[Config]:
    custom_config = repository.get(name = config_name)
    if custom_config:
        return Config.from_dict(custom_config)
    return None


def get_available_config_by_name(config_name: str) -> Optional[AvailableConfigs]:
    for config in AvailableConfigs:
        if config.config_name == config_name:
            return config
    return None  # Return None if no match is found


def is_a_value_allowed_for_a_given_config(config: AvailableConfigs, value: str) -> bool:
    for possible_value in config.possible_values:
        if possible_value == value:
            return True
    return False
