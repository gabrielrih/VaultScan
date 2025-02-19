import click

from vaultscan.core.engines.key_vault import KeyVaultConfig
from vaultscan.core.engines.keepass import KeePassConfig
from vaultscan.core.configs import AvailableConfigs, ConfigManager
from vaultscan.core.output.formatter import OutputHandler, OutputFormat
from vaultscan.core.output.logger import LoggerFactory
from vaultscan.repositories.vault.base import VaultStatus
from vaultscan.repositories.vault.factory import VaultRepositoryFactory


repository = VaultRepositoryFactory.create()
logger = LoggerFactory.get_logger(__name__)


@click.group()
def vault() -> None:
    ''' Configure a list of vaults used for searching objects '''
    pass


@vault.group
def add() -> None:
    ''' Add a vault on the configuration '''
    pass


@add.command()
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
@click.option('--vault-name', '--name',
              type = click.STRING,
              required = True,
              help = 'Azure Key Vault name')
def kv(alias: str, vault_name: str) -> None:
    ''' Add an Azure Key Vault on the configuration '''
    logger.debug(f'Args: {str(locals())}')
    vault = KeyVaultConfig(
        alias = alias,
        status = VaultStatus.ENABLED.value,
        vault_name = vault_name
    )
    created = repository.add(vault)
    if not created:
        logger.warning(f'The alias "{alias}" is already registered! It must be unique.')
        return
    logger.success('The vault was added on the configuration!')


@add.command
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
@click.option('--path',
              type = click.STRING,
              required = True,
              help = 'Path of KDBX file')
def keepass(alias: str, path: str) -> None:
    ''' Add a KeePass database on the configuration '''
    logger.debug(f'Args: {str(locals())}')
    if repository.get(alias = alias):  # check in the first time to avoid prompting the password and them generating the error
        logger.warning(f'The alias "{alias}" is already registered! It must be unique.')
        return
    password = click.prompt(f'Password for {path}', hide_input = True, type = str)
    vault = KeePassConfig(
        alias = alias,
        status = VaultStatus.ENABLED.value,
        path = path, 
        password = password
    )
    created = repository.add(vault)
    if not created:
        logger.warning(f'The alias "{alias}" is already registered! It must be unique.')
        return
    logger.success('The vault was added on the configuration!')


@vault.command()
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
def remove(alias: str) -> None:
    ''' Remove a vault from the configuration '''
    logger.debug(f'Args: {str(locals())}')
    removed = repository.remove(alias)
    if not removed:
        logger.warning(f'The alias "{alias}" was not found on the configuration!')
        return
    logger.success(f'The alias "{alias}" was removed from the configuration!')


@vault.command()
@click.option('--old-alias',
              type = click.STRING,
              required = True,
              help = 'Old vault alias')
@click.option('--new-alias',
              type = click.STRING,
              required = True,
              help = 'New vault alias')
def rename(old_alias: str, new_alias: str) -> None:
    ''' Change the vault alias '''
    logger.debug(f'Args: {str(locals())}')
    renamed = repository.rename(old_alias, new_alias)
    if not renamed:
        logger.warning(f'The alias "{old_alias}" was not found on the configuration!')
        return
    logger.success(f'The alias "{old_alias}" has been renamed to "{new_alias}"!')


@vault.command()
def remove_all() -> None:
    ''' Remove all vaults from the configuration '''
    repository.remove_all()
    logger.success('All the vaults has been removed from the configuration!')


@vault.command()
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
def disable(alias: str) -> None:
    ''' Ignore a vault for future searches '''
    logger.debug(f'Args: {str(locals())}')
    status = VaultStatus.DISABLED
    disabled = repository.change_status(alias = alias, status = status)
    if not disabled:
        logger.warning(f'The alias "{alias}" was not found on the configuration!')
        return
    logger.success(f'The status of alias "{alias}" has been changed to "{status.value}"!')


@vault.command()
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
def enable(alias: str) -> None:
    ''' Enable a vault for future searches '''
    logger.debug(f'Args: {str(locals())}')
    status = VaultStatus.ENABLED
    disabled = repository.change_status(alias = alias, status = status)
    if not disabled:
        logger.warning(f'The alias "{alias}" was not found on the configuration!')
        return
    logger.success(f'The status of alias "{alias}" has been changed to "{status.value}"!')


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(AvailableConfigs.OUTPUT_FORMAT).get_value()  # getting it from user configuration
@vault.command()
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = DEFAULT_OUTPUT_FORMAT.value,
              help = 'Output format')
def list(output_format: str) -> None:
    ''' List all vaults on the configuration '''
    logger.debug(f'Args: {str(locals())}')
    vaults = repository.get_all()
    logger.info(f'{len(vaults)} vault(s) found!')
    logger.debug(f'Vaults before the print: {vaults}')
    OutputHandler(
        format = OutputFormat(output_format)
    ).print(vaults)
