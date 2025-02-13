import os
from typing import List, Dict

from vaultscan.repository.common import VaultRepository, Vault
from vaultscan.util.json import JsonFileManager
from vaultscan.util.user import CurrentUser
from vaultscan.util.logger import LoggerFactory


logger = LoggerFactory.get_logger()


class VaultRepositoryAsJson(VaultRepository):
    def __init__(self):
        self.file = JSONFileHandler(
            folder_name = '.vaultscan',
            filename = 'vaults.json'
        )
        if not self.file.exists:
            self.initialize()

    def initialize(self):
        content: Dict = {
            'vaults': list()
        }
        self.file.write(content)

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
    
    def reset(self) -> None:
        self.initialize()


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

    def read(self) -> List[Dict]:
        if not self.exists:
            logger.verbose(f'File {self.path} doesnt exists!')
            return list()
        return JsonFileManager.load(self.path)
    
    def write(self, content: List[Dict]) -> None:
        logger.verbose(f'Writing file {self.path} on disk')
        JsonFileManager.write(content, self.path)


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
