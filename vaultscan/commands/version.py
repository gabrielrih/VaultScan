import click
import importlib.metadata

from vaultscan.core.output.logger import LoggerFactory
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.friendly_messages import VersionMessages
from vaultscan.util.package import PACKAGE_NAME


logger = LoggerFactory.get_logger(__name__)


@click.command()
def version() -> None:
    ''' Package version '''
    try:
        version = importlib.metadata.version(PACKAGE_NAME)
    except importlib.metadata.PackageNotFoundError:
        message = VersionMessages.PACKAGE_NOT_INSTALLED.value.format(
            package_name = PACKAGE_NAME
        )
        logger.error(message)
        return
    message = VersionMessages.INSTALLED_VERSION.value.format(
        package_name = PACKAGE_NAME,
        version = version
    )
    OutputHandler(format = OutputFormat.STANDARD).print(message)
