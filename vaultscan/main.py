import click

from vaultscan.commands.vault import vault
from vaultscan.commands.find import find


@click.group()
def main(): pass


main.add_command(vault)
main.add_command(find)
if __name__ == '__main__':
    main()
