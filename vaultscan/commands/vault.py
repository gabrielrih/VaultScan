import click

from vaultscan.repositories.vault.factory import VaultRepositoryFactory
from vaultscan.engines.key_vault import KeyVaultConfig
from vaultscan.engines.keepass import KeePassConfig
from vaultscan.util.output.formatter import OutputFormat, OutputHandler
from vaultscan.util.output.logger import LoggerFactory


repository = VaultRepositoryFactory.create()


logger = LoggerFactory.get_logger(__name__)



@click.group()
def vault() -> None:
    ''' Manage vaults '''
    pass


@vault.group
def add() -> None:
    ''' Add a new vault on the configuration '''
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
@click.option('--resource-group-name', '--rg',
              type = click.STRING,
              required = True,
              help = 'Azure Resource Group Name where the vault is located')
@click.option('--subscription-id',
              type = click.STRING,
              required = True,
              help = 'Azure Subscription ID where the vault is located')
def kv(alias: str, vault_name: str, resource_group_name: str, subscription_id: str) -> None:
    ''' Azure Key Vault '''
    vault = KeyVaultConfig(
        alias = alias,
        subscription_id = subscription_id,
        resource_group_name = resource_group_name,
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
    ''' KeePass database '''
    if repository.get(alias = alias):  # check in the first time to avoid prompting the password and them generating the error
        logger.warning(f'The alias "{alias}" is already registered! It must be unique.')
        return
    password = click.prompt(f'Password for {path}', hide_input = True, type = str)
    vault = KeePassConfig(
        alias = alias,
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
    ''' Remove a vault from the configuration'''
    removed = repository.remove(alias)
    if not removed:
        logger.warning(f'The alias "{alias}" was not found on the configuration!')
        return
    logger.success(f'The alias "{alias}" was removed from the configuration!')


@vault.command()
def reset() -> None:
    ''' Reset the vaults'''
    repository.reset()
    logger.success('The configuration has been reset!')


@vault.command()
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = OutputFormat.JSON.value,
              help = 'Output format')
def list(output_format: str) -> None:
    ''' List vaults '''
    logger.debug(f'Args: {str(locals())}')
    format = OutputFormat(output_format)
    vaults = repository.get_all()
    logger.info(f'{len(vaults)} vault(s) found!')
    OutputHandler(format).print(vaults)
