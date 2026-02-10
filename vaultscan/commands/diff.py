import click

from vaultscan.application.diff_service import CompareSecretOnVaults
from vaultscan.application.base import ServiceResult
from vaultscan.core.configs import AvailableConfigs, ConfigManager
from vaultscan.core.output.time_execution import time_execution
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(
    AvailableConfigs.OUTPUT_FORMAT
).get_value()  # getting it from user configuration

@click.command()
@click.argument("source", required = True)
@click.argument("target", required = True)
@click.option('--compare-values',
              is_flag = True,
              required = False,
              help = 'Compare secret values')
@click.option('--show-details',
              is_flag = True,
              required = False,
              help = 'Show list of secrets')
@time_execution
def diff(source: str, target: str, compare_values: bool, show_details: bool) -> None:
    ''' Compare secrets between vaults '''
    logger.debug(f'Args: {str(locals())}')

    compare = CompareSecretOnVaults()
    result: ServiceResult = compare.execute(
        source_vault = source,
        target_vault = target,
        compare_values = compare_values,
        show_details = show_details
    )

    if not result.success:
        logger.error(result.message)
        return

    for warning in result.warnings:
        logger.warning(warning)

    if result.data:
        OutputHandler(
            format = OutputFormat.JSON
        ).print(result.data)

    if result.message:
        logger.info(result.message)
