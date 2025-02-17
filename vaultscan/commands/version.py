import click
import importlib.metadata

from vaultscan.settings import PACKAGE_NAME
from vaultscan.util.output.logger import LoggerFactory
from vaultscan.util.output.formatter import OutputFormat, OutputHandler


logger = LoggerFactory.get_logger(__name__)


@click.command()
def version() -> None:
    ''' Package version '''
    try:
        version = importlib.metadata.version(PACKAGE_NAME)
    except importlib.metadata.PackageNotFoundError:
        logger.error(f'{PACKAGE_NAME} is not installed via pip!')
    message = f'{PACKAGE_NAME} version: {version}'
    OutputHandler(
        format = OutputFormat(OutputFormat.STANDARD.value)
    ).print(message)
