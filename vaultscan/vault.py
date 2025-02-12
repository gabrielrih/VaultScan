import os

from dataclasses import dataclass
from typing import List, Dict

from vaultscan.util.json import load_json_from_file, write_json_on_file


@dataclass
class Vault:
    alias: str
    subscription_id: str
    resource_group_name: str
    vault_name: str


class VaultManager:
    def __init__(self):
        self.file = ConfigFile()
        self.file.create_if_doesnt_exist()

    def add(self, new_vault: Vault) -> bool:
        content: Dict = self.file.read()
        vaults: List[Dict] = content['vaults']
        exists = False
        for vault in vaults:
            if vault['alias'] == new_vault.alias:
                exists = True
                break
        if exists:
            return False
        vaults.append(new_vault.__dict__)
        content['vaults'] = vaults
        self.file.write(content)
        return True

    def remove(self, alias: str) -> bool:
        content: List[Dict] = self.file.read()
        vaults: List[Dict] = content['vaults']
        if not vaults:
            return False
        removed = False
        for vault in vaults:
            if vault['alias'] == alias:
                vaults.remove(vault)
                content['vaults'] = vaults
                self.file.write(content)
                removed = True
                break
        return removed

    def view(self) -> List[Vault]:
        return self.file.read()
    
    def clear(self) -> None:
        content: Dict = {
            'vaults': list()
        }
        self.file.write(content)


class ConfigFile:
    def __init__(self):
        self._filename = 'vaults.json'
        self.folder = ConfigFolder()

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def path(self) -> str:
        return str(os.path.join(self.folder.path, self.filename))

    @property
    def exists(self) -> bool:
        return os.path.exists(self.path)

    def read(self) -> List[Dict]:
        if not self.exists:
            return list()
        return load_json_from_file(self.path)
    
    def write(self, content: List[Dict]) -> None:
        write_json_on_file(content, self.path)

    def create_if_doesnt_exist(self) -> None:
        if self.exists:
            return
        self.folder.create_if_doesnt_exist()
        print(f'Creating empty file {self.path}')
        content: Dict = {
            'vaults': list()
        }
        write_json_on_file(content, self.path)


class ConfigFolder:
    def __init__(self):
        self._foldername = '.vaultscan'

    @property
    def name(self) -> str:
        return self._foldername

    @property
    def path(self) -> str:
        home = self._get_home_directory()
        if not home:
            raise EnvironmentError('Unable to determine the user home directory')
        return str(os.path.join(home, self.name))
    
    def create_if_doesnt_exist(self) -> None:
        os.makedirs(self.path, exist_ok = True)

    def _get_home_directory(self) -> str:
        if os.name == 'nt':  # Windows
            return os.getenv('USERPROFILE')
        if os.name == 'posix':  # Linux
            return os.getenv('HOME')
        raise EnvironmentError('Unsupported OS')
