import click
import importlib.metadata

from vaultscan.core.output.logger import LoggerFactory
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.util.package import PACKAGE_NAME


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
        format = OutputFormat.STANDARD
    ).print(message)
