import click

from typing import Optional

from vaultscan.core.configs import (
    AvailableConfigs,
    get_available_config_by_name,
    is_a_value_allowed_for_a_given_config
)
from vaultscan.repositories.config.base import Config
from vaultscan.repositories.config.factory import ConfigRepositoryFactory
from vaultscan.util.output.formatter import OutputFormat, OutputHandler
from vaultscan.util.output.logger import LoggerFactory


repository = ConfigRepositoryFactory.create()


logger = LoggerFactory.get_logger(__name__)



@click.group()
def config() -> None:
    ''' Manage configurations '''
    pass


@config.command()
@click.option('--name',
              type = click.Choice( [ config.config_name for config in AvailableConfigs]),
              required = True,
              help = 'Config name')
@click.option('--value',
              type = click.STRING,
              required = True,
              help = 'Config value')
def set(name: str, value: str) -> None:
    ''' Set configuration '''
    logger.debug(f'Args: {str(locals())}')

    # Getting the AvailableConfig
    config: Optional[AvailableConfigs] = get_available_config_by_name(config_name = name)
    if not config:
        ''' It should never happen because the click.Choice are loading the right configs, but... '''
        raise RuntimeError(f'The value of config variable should be one of the type {AvailableConfigs.__name__}')
    
    # Checking if the given value is allowed for this config (looking at the possible_values)
    is_valid_value = is_a_value_allowed_for_a_given_config(config = config, value = value)
    if not is_valid_value:
        message = f'The value "{value}" is not valid for the "{name}" configuration. The possible values are: {str(config.possible_values)}'
        logger.error(message)
        return
    
    # Save the custom configuration
    config = Config(
        name = name,
        value = value
    )
    repository.set(new_config = config)
    logger.success(f'The config "{name}" was set using the given value!')


@config.command()
@click.option('--name',
              type = click.Choice( [ config.config_name for config in AvailableConfigs]),
              required = True,
              help = 'Config name')
def unset(name: str) -> None:
    '''  Revert configuration to its original state '''
    logger.debug(f'Args: {str(locals())}')
    
    # Getting the AvailableConfig
    config: Optional[AvailableConfigs] = get_available_config_by_name(config_name = name)
    if not config:
        ''' It should never happen because the click.Choice are loading the right configs, but... '''
        raise RuntimeError(f'The value of config variable should be one of the type {AvailableConfigs.__name__}')
    
    # Reset to the default configuration
    repository.unset(name = config.config_name)
    logger.success(f'The config "{config.config_name}" has been reverted to its original value!')


@config.command()
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = OutputFormat.JSON.value,
              help = 'Output format')
def list(output_format: str) -> None:
    ''' List configurations '''
    logger.debug(f'Args: {str(locals())}')
    format = OutputFormat(output_format)
    configs = []
    for available_config in AvailableConfigs:
        config = {
            'name': available_config.config_name,
            'current_value': available_config.value_as_string,
            'default_value': str(available_config.default_value)
        }
        configs.append(config)
    logger.info(f'{len(configs)} configs found!')
    response = {
        'configs': configs
    }
    OutputHandler(format).print(response)
