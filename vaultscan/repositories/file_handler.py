import os

from abc import ABC, abstractmethod
from json import load, dump
from typing import List, Dict, Any

from vaultscan.util.user import CurrentUser



class FileHandler(ABC):
    def __init__(self, folder_name: str, filename: str):
        self._filename = filename
        self.folder_name = folder_name

    @property
    def filename(self) -> str:
        return self._filename
    
    @property
    @abstractmethod
    def path(self) -> str: pass

    @property
    @abstractmethod
    def exists(self) -> bool: pass

    @abstractmethod
    def read(self) -> Any: pass
    
    @abstractmethod
    def write(self, content: Any) -> None: pass


class JSONFileHandler(FileHandler):
    ''' It handles a JSON file on a given folder '''
    def __init__(self, folder_name, filename):
        super().__init__(folder_name, filename)
        self.folder = DefaultConfigFolder(name = folder_name)
        self.folder.create_if_doesnt_exist()

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
    ''' It manages the user home folder '''
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
    ''' Write and load json file on disk '''
    @staticmethod
    def load(path: str) -> Dict:
        with open(path, "r") as file:
            return load(file)

    @staticmethod
    def write(content: Dict, path: str) -> None:
        with open(path, 'w') as f:
            dump(content, f, indent=4)
