import click

from vaultscan.commands.config import config
from vaultscan.commands.find import find


@click.group()
def main(): pass


main.add_command(config)
main.add_command(find)
if __name__ == '__main__':
    main()
