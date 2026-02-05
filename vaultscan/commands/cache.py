import click

from vaultscan.core.cache.singleton import CacheManagerSingleton
from vaultscan.core.friendly_messages import CacheMessages
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.output.logger import LoggerFactory
from vaultscan.core.configs import AvailableConfigs, ConfigManager


logger = LoggerFactory.get_logger(__name__)


@click.group()
def cache() -> None:
    ''' Manage cache '''
    pass


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(
    AvailableConfigs.OUTPUT_FORMAT
).get_value()
CACHE_ENABLED: bool = ConfigManager(
    AvailableConfigs.CACHE_ENABLED
).get_value()
@cache.command()
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = DEFAULT_OUTPUT_FORMAT.value,
              help = 'Output format')
def status(output_format: str) -> None:
    ''' Show cache status and statistics '''
    logger.debug(f'Args: {str(locals())}')
    cache_manager = CacheManagerSingleton.get_instance()
    stats = cache_manager.get_stats()
    stats['cache_enabled'] = CACHE_ENABLED
    
    OutputHandler(
        format = OutputFormat(output_format)
    ).print([stats])

@cache.command()
def reset() -> None:
    ''' Reset cache '''
    cache_manager = CacheManagerSingleton.get_instance()
    cache_manager.clear()
    logger.success(CacheMessages.CACHE_RESET.value)
