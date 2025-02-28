from vaultscan.commands.main import main
from vaultscan.commands.config import config
from vaultscan.commands.vault import vault
from vaultscan.commands.find import find
from vaultscan.commands.version import version


__version__ = "0.3.3"


main.add_command(vault)
main.add_command(config)
main.add_command(find)
main.add_command(version)
if __name__ == '__main__':
    main()
