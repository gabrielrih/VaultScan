import click

from typing import Dict, List

from vaultscan.repositories.config.base import Config
from vaultscan.repositories.config.factory import ConfigRepositoryFactory
from vaultscan.core.configs import AvailableConfigs, ConfigManager, ConfigValidator
from vaultscan.core.friendly_messages import ConfigMessages
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.output.logger import LoggerFactory


repository = ConfigRepositoryFactory.create()
logger = LoggerFactory.get_logger(__name__)


@click.group()
def config() -> None:
    ''' Manage configurations '''
    pass


config_name = click.option('--name', type = click.Choice(AvailableConfigs.get_values()), required = True, help = 'Config name')

@config.command()
@config_name
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
        ''' It should never get in here because the click should validate
            the right option when using the click.Choice type '''
        message = ConfigMessages.INVALID_VALUE.value.format(
            value = value,
            config = name,
            possible_values = str(config.possible_values)
        )
        logger.error(message)
        return
    config = Config(
        name = name,
        value = value
    )
    repository.set(new_config = config)
    message = ConfigMessages.CONFIG_SET.value.format(config = name)
    logger.success(message)


@config.command()
@config_name
def reset(name: str) -> None:
    '''  Reset configuration to its original state '''
    logger.debug(f'Args: {str(locals())}')
    config: AvailableConfigs = AvailableConfigs.from_config_name(config_name = name)
    repository.unset(name = config.config_name)
    message = ConfigMessages.CONFIG_RESET.value.format(config = config.config_name)
    logger.success(message)


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(
    AvailableConfigs.OUTPUT_FORMAT
).get_value()  # getting it from user configuration

@config.command()
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = DEFAULT_OUTPUT_FORMAT.value,
              help = 'Output format')
def list(output_format: str) -> None:
    ''' List configurations '''
    logger.debug(f'Args: {str(locals())}')
    configs = get_configs_current_and_default_values()
    message = ConfigMessages.NUMBER_OF_CONFIGS_FOUND.value.format(quantity = len(configs))
    logger.info(message)
    OutputHandler(
        format = OutputFormat(output_format)
    ).print(configs)


# FIX IT
# It should be here?
def get_configs_current_and_default_values() -> List[Dict]:
    response = []
    for available_config in AvailableConfigs:
        available_config = {
            'name': available_config.config_name,
            'current_value': ConfigManager(available_config).get_value_as_string(),
            'default_value': available_config.default_value
        }
        response.append(available_config)
    return response
