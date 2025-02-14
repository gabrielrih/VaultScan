import click

from vaultscan.repository.factory import VaultRepositoryFactory
from vaultscan.repository.common import Vault
from vaultscan.util.json import JsonHandler
from vaultscan.util.logger import LoggerFactory


repository = VaultRepositoryFactory.create()


logger = LoggerFactory.get_logger()



@click.group()
def config() -> None:
    ''' Manage the configuration '''
    pass



@config.command()
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
@click.option('--vault-name',
              type = click.STRING,
              required = True,
              help = 'Azure Key Vault name')
@click.option('--resource-group-name',
              type = click.STRING,
              required = True,
              help = 'Azure Resource Group Name where the vault is located')
@click.option('--subscription-id',
              type = click.STRING,
              required = True,
              help = 'Azure Subscription ID where the vault is located')
def add(alias: str, vault_name: str, resource_group_name: str, subscription_id: str) -> None:
    ''' Add a new vault on the configuration '''
    vault = Vault(
        alias = alias,
        subscription_id = subscription_id,
        resource_group_name = resource_group_name,
        vault_name = vault_name
    )
    created = repository.add(vault)
    if not created:
        logger.warning(f'The alias "{alias}" is already registered!')
        return
    logger.success('The vault was added on the configuration!')

@config.command()
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


@config.command()
def reset() -> None:
    ''' Reset the configuration '''
    repository.reset()
    logger.success('The configuration has been reset!')


@config.command()
def view() -> None:
    ''' View configuration '''
    click.echo(
        JsonHandler.beatifull_print(
            repository.view()
        )
    )
