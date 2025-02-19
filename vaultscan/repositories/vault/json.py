from typing import List, Dict

from vaultscan.repositories.vault.base import (
    VaultRepository,
    BaseVaultConfig,
    VaultStatus
)
from vaultscan.repositories.file_handler import JSONFileHandler


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

    def remove_all(self) -> None:
        self.initialize()

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
