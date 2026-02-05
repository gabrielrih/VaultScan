import re

from typing import List, Dict

from vaultscan.repositories.vault.base import (
    VaultRepository,
    BaseVaultConfig,
    VaultStatus
)
from vaultscan.repositories.file_handler import FileHandler


class VaultRepositoryAsJson(VaultRepository):
    ''' Repository implementation to persist vaults on a file '''
    def __init__(self, file: FileHandler):
        self.file = file
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
        removed = False
        for vault in vaults:
            if vault['alias'] == alias:
                vaults.remove(vault)
                content['vaults'] = vaults
                self.file.write(content)
                removed = True
                break
        return removed

    def remove_all(self) -> None:
        self.initialize()

    def rename(self, old_alias: str, new_alias: str) -> bool:
        content: Dict = self.file.read()
        vaults: List[Dict] = content['vaults']
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

    def get_all(self, filter: str = '') -> List[Dict]:
        content: Dict = self.file.read()
        vaults = content['vaults']

        if not filter:
            return vaults
        
        filtered_vaults = []
        for vault in vaults:
            searchable_text = f"{vault.get('alias', '')}"
            if re.search(filter, searchable_text, re.IGNORECASE):
                filtered_vaults.append(vault)
        
        return filtered_vaults
