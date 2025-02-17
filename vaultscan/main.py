import click

from vaultscan.commands.vault import vault
from vaultscan.commands.find import find
from vaultscan.commands.version import version


@click.group()
def main(): pass


main.add_command(vault)
main.add_command(find)
main.add_command(version)
if __name__ == '__main__':
    main()
