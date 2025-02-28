import click

from vaultscan.core.engines.key_vault import KeyVaultConfig
from vaultscan.core.engines.keepass import KeePassConfig
from vaultscan.core.configs import AvailableConfigs, ConfigManager
from vaultscan.core.friendly_messages import VaultMessages
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

alias = click.option('--alias', type = click.STRING, required = True, help = 'Vault alias')

@add.command()
@alias
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
        message = VaultMessages.VAULT_ALREADY_EXISTS.value.format(alias = alias)
        logger.warning(message)
        return
    message = VaultMessages.VAULT_ADDED.value.format(alias = alias)
    logger.success(message)


@add.command
@alias
@click.option('--path',
              type = click.STRING,
              required = True,
              help = 'Path of KDBX file')
def keepass(alias: str, path: str) -> None:
    ''' Add a KeePass database on the configuration '''
    logger.debug(f'Args: {str(locals())}')
    # checking it in the first time to avoid prompting the password when the alias already exists
    if repository.get(alias = alias):
        message = VaultMessages.VAULT_ALREADY_EXISTS.value.format(alias = alias)
        logger.warning(message)
        return
    password = click.prompt(f'Password for "{path}"', hide_input = True, type = str)
    vault = KeePassConfig(
        alias = alias,
        status = VaultStatus.ENABLED.value,
        path = path, 
        password = password
    )
    created = repository.add(vault)
    # Checking again because technically the vault could have been created from another terminal
    if not created:
        message = VaultMessages.VAULT_ALREADY_EXISTS.value.format(alias = alias)
        logger.warning(message)
        return
    logger.success(VaultMessages.VAULT_ADDED.value.format(alias = alias))


@vault.command()
@alias
def remove(alias: str) -> None:
    ''' Remove a vault from the configuration '''
    logger.debug(f'Args: {str(locals())}')
    removed = repository.remove(alias)
    if not removed:
        message = VaultMessages.VAULT_NOT_FOUND.value.format(alias = alias)
        logger.warning(message)
        return
    message = VaultMessages.VAULT_REMOVED.value.format(alias = alias)
    logger.success(message)


@vault.command()
@alias
@click.option('--new-alias',
              type = click.STRING,
              required = True,
              help = 'New vault alias')
def rename(alias: str, new_alias: str) -> None:
    ''' Change the vault alias '''
    logger.debug(f'Args: {str(locals())}')
    renamed = repository.rename(alias, new_alias)
    if not renamed:
        message = VaultMessages.VAULT_NOT_FOUND.value.format(alias = alias)
        logger.warning(message)
        return
    message = VaultMessages.VAULT_RENAMED.value.format(old_alias = alias, new_alias = new_alias)
    logger.success(message)


@vault.command()
def remove_all() -> None:
    ''' Remove all vaults from the configuration '''
    repository.remove_all()
    logger.success(VaultMessages.ALL_VAULTS_REMOVED.value)


@vault.command()
@alias
def disable(alias: str) -> None:
    ''' Ignore a vault for future searches '''
    logger.debug(f'Args: {str(locals())}')
    status = VaultStatus.DISABLED
    disabled = repository.change_status(alias = alias, status = status)
    if not disabled:
        message = VaultMessages.VAULT_NOT_FOUND.value.format(alias = alias)
        logger.warning(message)
        return
    message = VaultMessages.VAULT_STATUS_CHANGED.value.format(alias = alias, status = status.value)
    logger.success(message)


@vault.command()
@alias
def enable(alias: str) -> None:
    ''' Enable a vault for future searches '''
    logger.debug(f'Args: {str(locals())}')
    status = VaultStatus.ENABLED
    disabled = repository.change_status(alias = alias, status = status)
    if not disabled:
        message = VaultMessages.VAULT_NOT_FOUND.value.format(alias = alias)
        logger.warning(message)
        return
    message = VaultMessages.VAULT_STATUS_CHANGED.value.format(alias = alias, status = status.value)
    logger.success(message)


DEFAULT_OUTPUT_FORMAT: OutputFormat = ConfigManager(
    AvailableConfigs.OUTPUT_FORMAT
).get_value()  # getting it from user configuration

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
    logger.info(
        VaultMessages.NUMBER_OF_VAULTS_FOUND.value.format(quantity = len(vaults))
    )
    OutputHandler(
        format = OutputFormat(output_format)
    ).print(vaults)
