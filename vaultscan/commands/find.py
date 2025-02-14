import click

from typing import List, Dict

from vaultscan.core.scanner import SecretScanner, FindType
from vaultscan.repositories.factory import VaultRepositoryFactory
from vaultscan.util.output.formatter import OutputFormat, OutputHandler
from vaultscan.util.output.logger import LoggerFactory


vault_repository = VaultRepositoryFactory.create()


logger = LoggerFactory.get_logger()


@click.group()
def find() -> None:
    ''' Find objects on vaults  '''
    pass


@find.command()
@click.argument("secret")
@click.option('--only-vault',
              type = click.STRING,
              required = False,
              default = '',
              help = 'Search only in a specific vault')
@click.option('--exact',
              is_flag = True,
              required = False,
              help = 'Search for an exact match instead of a regex')
# @click.option('--show-values',
#               is_flag = True,
#               required = False,
#               help = 'Show the value of the secrets')
@click.option('--output-format', '-o',
              type = click.Choice(OutputFormat.get_values()),
              required = False,
              default = OutputFormat.TABLE.value,
              help = 'Output format')
def secrets(secret: str, only_vault: str, exact: bool, output_format: str) -> None:
    ''' Find secrets across vaults '''
    logger.verbose(f'Args: {str(locals())}')

    # Getting vaults
    vaults: List[Dict] = get_vaults(only_vault)
    if not vaults:
        logger.error(f'No vault matching alias {only_vault}')
        return
    
    # Finding secrets
    find_type = FindType.BY_REGEX
    if exact:
        find_type = FindType.EXACTLY_MATCH
    scanner = SecretScanner(vaults)
    secrets: List[Dict] = scanner.find(
        secret_name = secret,
        type = find_type
    )

    # Printing results
    OutputHandler(
        format = OutputFormat(output_format)
    ).print(secrets)


def get_vaults(only_vault: str = '') -> List[Dict]:
    if only_vault:
        vault: Dict = vault_repository.get(alias = only_vault)
        logger.verbose(f'Vault {only_vault} content: {vault}')
        if not vault:
            return list()
        return [ vault ]
    return vault_repository.get_all()
