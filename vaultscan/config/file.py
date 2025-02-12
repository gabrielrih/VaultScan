import os

from typing import List, Dict

from vaultscan.util.json import load_json_from_file, write_json_on_file


class ConfigFile:
    def __init__(self):
        self._filename = 'vaults.json'
        self.folder = ConfigFolder()
        self.folder.create_if_doesnt_exist()

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
