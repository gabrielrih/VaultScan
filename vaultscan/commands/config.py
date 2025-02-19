import click

from vaultscan.core.configs import AvailableConfigs, ConfigManager, ConfigValidator
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
              type = click.Choice(AvailableConfigs.get_values()),
              required = True,
              help = 'Config name')
@click.option('--value',
              type = click.STRING,
              required = True,
              help = 'Config value')
def set(name: str, value: str) -> None:
    ''' Set configuration '''
    logger.debug(f'Args: {str(locals())}')
    config: AvailableConfigs = AvailableConfigs.from_config_name(config_name = name)
    is_valid_value = ConfigValidator.is_a_valid_value(config = config, value = value)
    if not is_valid_value:
        message = f'The value "{value}" is not valid for the "{name}" configuration. The possible values are: {str(config.possible_values)}'
        logger.error(message)
        return
    config = Config(
        name = name,
        value = value
    )
    repository.set(new_config = config)
    logger.success(f'The config "{name}" was set using the given value!')

@config.command()
@click.option('--name',
              type = click.Choice(AvailableConfigs.get_values()),
              required = True,
              help = 'Config name')
def reset(name: str) -> None:
    '''  Reset configuration to its original state '''
    logger.debug(f'Args: {str(locals())}')
    config: AvailableConfigs = AvailableConfigs.from_config_name(config_name = name)
    repository.unset(name = config.config_name)
    logger.success(f'The config "{config.config_name}" has been reverted to its original value!')

# FIX IT
# The the outputformat from configs.py
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
    for config in AvailableConfigs:
        manager = ConfigManager(config = config) 
        config = {
            'name': config.config_name,
            'current_value': manager.get_value_as_string(),
            'default_value': config.default_value
        }
        configs.append(config)
    logger.info(f'{len(configs)} configs found!')
    response = {
        'configs': configs
    }
    OutputHandler(format).print(response)
