import os

from json import load, dump
from typing import List, Dict

from vaultscan.util.user import CurrentUser


class JSONFileHandler:
    def __init__(self, folder_name: str, filename: str):
        self._filename = filename
        self.folder = DefaultConfigFolder(name = folder_name)
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

    def read(self) -> Dict:
        if self.exists:
            return JsonFileIO.load(self.path)
        return {}
    
    def write(self, content: List[Dict]) -> None:
        JsonFileIO.write(content, self.path)


class DefaultConfigFolder:
    def __init__(self, name: str):
        self._folder_name = name
        self._current_user = CurrentUser()

    @property
    def name(self) -> str:
        return self._folder_name

    @property
    def path(self) -> str:
        path = os.path.join(self._current_user.home_path, self.name)
        return str(path)
    
    def create_if_doesnt_exist(self) -> None:
        os.makedirs(self.path, exist_ok = True)


class JsonFileIO:
    @staticmethod
    def load(path: str) -> Dict:
        with open(path, "r") as file:
            return load(file)

    @staticmethod
    def write(content: Dict, path: str) -> None:
        with open(path, 'w') as f:
            dump(content, f, indent=4)
