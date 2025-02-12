import click

from vaultscan.config.repository import Vault, VaultRepository
from vaultscan.util.json import beatifull_print


repository = VaultRepository()


class Log:
    def info(message: str):
        message = f'INFO: {message}' 
        click.secho(message, fg='blue')

    def success(message: str):
        message = f'SUCCESS: {message}' 
        click.secho(message, fg='green')

    def warning(message: str):
        message = f'WARNING: {message}' 
        click.secho(message, fg='yellow')

    def error(message: str):
        message = f'ERROR: {message}' 
        click.secho(message, fg='red')


@click.group()
def main(): pass


@click.group()
def config() -> None:
    ''' Manage the configuration '''
    pass


@click.group()
def find() -> None:
    ''' Find objects on vaults  '''
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
        Log.warning(f'The alias "{alias}" is already registered!')
        return
    Log.success('The vault was added on the configuration!')

@config.command()
@click.option('--alias',
              type = click.STRING,
              required = True,
              help = 'Vault alias')
def remove(alias: str) -> None:
    ''' Remove a vault from the configuration'''
    removed = repository.remove(alias)
    if not removed:
        Log.warning(f'The alias "{alias}" was not found on the configuration!')
        return
    Log.success(f'The alias "{alias}" was removed from the configuration!')


@config.command()
def reset() -> None:
    ''' Reset the configuration '''
    repository.reset()
    Log.success('The configuration has been reset!')


@config.command()
def view() -> None:
    ''' View configuration '''
    click.echo(
        beatifull_print(
            repository.view()
        )
    )


@find.command()
@click.option('--only-vault',
              type = click.STRING,
              required = False,
              default = '',
              help = 'Vault alias where it''s going to search')
@click.option('--show-values',
              is_flag = True,
              required = False,
              help = 'Show the value of the secrets')
def secrets(only_vault: str = '', show_values: bool = False) -> None:
    ''' Find secrets '''
    pass


main.add_command(config)
main.add_command(find)
if __name__ == '__main__':
    main()
