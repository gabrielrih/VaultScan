import click

from typing import List, Dict

from vaultscan.core.vaults import get_vaults
from vaultscan.core.scanner import MultiVaultScannerBuilder
from vaultscan.core.configs import AvailableConfigs, ConfigManager
from vaultscan.core.friendly_messages import VaultMessages
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


@click.group()
def find() -> None:
    ''' Find objects across vaults  '''
    pass


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(AvailableConfigs.OUTPUT_FORMAT).get_value()  # getting it from user configuration
@find.command()
@click.argument("filter")
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
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = DEFAULT_OUTPUT_FORMAT.value,
              help = 'Output format')
def secrets(filter: str, only_vault: str, exact: bool, show_values: bool, output_format: str) -> None:
    ''' Find secrets across vaults '''
    logger.debug(f'Args: {str(locals())}')
    vaults = get_vaults(only_vault = only_vault)
    if not vaults:
        logger.error(VaultMessages.NO_VAULTS.value)
        return
    scanner = MultiVaultScannerBuilder.create(vaults = vaults, exact_match = exact)
    secrets: List[Dict] = scanner.find(
        filter = filter,
        is_value = show_values
    )
    OutputHandler(
        format = OutputFormat(output_format)
    ).print(secrets)
