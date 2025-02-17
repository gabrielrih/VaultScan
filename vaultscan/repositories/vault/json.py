import os
from typing import List, Dict

from vaultscan.repositories.vault.base import VaultRepository
from vaultscan.engines.base import BaseVaultConfig, VaultStatus
from vaultscan.util.json import JsonFileManager
from vaultscan.util.user import CurrentUser
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


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

    def add(self, new_vault: BaseVaultConfig) -> bool:
        content: Dict = self.file.read()
        vaults: List[Dict] = content['vaults']
        exists = False
        for vault in vaults:
            if vault['alias'] == new_vault.alias:
                exists = True
                break
        if exists:
            return False
        vaults.append(new_vault.to_dict())
        content['vaults'] = vaults
        self.file.write(content)
        return True

    def remove(self, alias: str) -> bool:
        content: Dict = self.file.read()
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

    def rename(self, old_alias: str, new_alias: str) -> bool:
        content: Dict = self.file.read()
        vaults: List[Dict] = content['vaults']
        if not vaults:
            return False
        renamed = False
        for vault in vaults:
            if vault['alias'] == old_alias:
                vault['alias'] = new_alias
                content['vaults'] = vaults
                self.file.write(content)
                renamed = True
                break
        return renamed

    def change_status(self, alias: str, status: VaultStatus) -> bool:
        content: Dict = self.file.read()
        vaults: List[Dict] = content['vaults']
        if not vaults:
            return False
        changed = False
        for vault in vaults:
            if vault['alias'] == alias:
                vault['status'] = status.value
                content['vaults'] = vaults
                self.file.write(content)
                changed = True
                break
        return changed

    def get(self, alias: str) -> Dict:
        content: Dict = self.file.read()
        vaults: List[Dict] = content['vaults']
        for vault in vaults:
            if vault['alias'] == alias:
                return vault
        return {}

    def get_all(self) -> List[Dict]:
        content: Dict = self.file.read()
        return content['vaults']
    
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

    def read(self) -> Dict:
        if not self.exists:
            logger.debug(f'File {self.path} doesnt exists!')
            return {}
        return JsonFileManager.load(self.path)
    
    def write(self, content: List[Dict]) -> None:
        logger.debug(f'Writing file {self.path} on disk')
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
