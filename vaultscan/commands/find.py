import click

from typing import List, Dict

from vaultscan.core.scanner import MultiVaultScannerBuilder
from vaultscan.util.output.formatter import OutputFormat, OutputHandler
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


@click.group()
def find() -> None:
    ''' Find objects on vaults  '''
    pass


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
              default = OutputFormat.TABLE.value,
              help = 'Output format')
def secrets(filter: str, only_vault: str, exact: bool, show_values: bool, output_format: str) -> None:
    ''' Find secrets across vaults '''
    logger.debug(f'Args: {str(locals())}')
    scanner = MultiVaultScannerBuilder.create(
        only_vault = only_vault,
        exact_match = exact
    )
    secrets: List[Dict] = scanner.find(
        filter = filter,
        is_value = show_values
    )
    if not secrets:
        return
    OutputHandler(
        format = OutputFormat(output_format)
    ).print(secrets)
