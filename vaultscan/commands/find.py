import click

from vaultscan.application.find_service import FindSecretService
from vaultscan.application.result import ServiceResult
from vaultscan.core.configs import AvailableConfigs, ConfigManager
from vaultscan.core.output.time_execution import time_execution
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


@click.group()
def find() -> None:
    ''' Find objects across vaults  '''
    pass


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(
    AvailableConfigs.OUTPUT_FORMAT
).get_value()  # getting it from user configuration

@find.command()
@click.argument("filter", required = False, default = '')
@click.option('--only-vault',
              type = click.STRING,
              required = False,
              default = '',
              help = 'Search only in a specific vault')
@click.option('--exact',
              is_flag = True,
              required = False,
              help = 'Search for an exact match instead of a regex')
@click.option('--show-values',
              is_flag = True,
              required = False,
              help = 'Show the value of the secrets')
@click.option('--only-count',
              is_flag = True,
              required = False,
              help = 'Show only the count of secrets')
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = DEFAULT_OUTPUT_FORMAT.value,
              help = 'Output format')
@time_execution
def secrets(filter: str, only_vault: str, exact: bool, show_values: bool, only_count: bool, output_format: str) -> None:
    ''' Find secrets across vaults '''
    logger.debug(f'Args: {str(locals())}')

    find_service = FindSecretService(only_vault = only_vault)
    result: ServiceResult = find_service.find(
        filter = filter,
        exact = exact,
        show_values = show_values,
        only_count = only_count
    )

    if not result.success:
        logger.error(result.message)
        return
    
    for warning in result.warnings:
        logger.warning(warning)

    if result.data:
        OutputHandler(
            format = OutputFormat(output_format)
        ).print(result.data)

    if result.message:
        logger.info(result.message)
