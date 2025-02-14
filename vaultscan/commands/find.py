import click

from vaultscan.util.logger import LoggerFactory


logger = LoggerFactory.get_logger()


@click.group()
def find() -> None:
    ''' Find objects on vaults  '''
    pass


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
@click.option('--verbose',
              is_flag = True,
              help = "Enable verbose output")
def secrets(only_vault: str = '', show_values: bool = False, verbose: bool = False) -> None:
    ''' Find secrets '''
    pass
