from dataclasses import dataclass
from typing import List, Dict
from abc import ABC, abstractmethod

from vaultscan.config.file import JSONFileHandler


@dataclass
class Vault:
    alias: str
    subscription_id: str
    resource_group_name: str
    vault_name: str


class VaultRepository(ABC):
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def add(self, new_vault: Vault) -> bool: pass

    @abstractmethod
    def remove(self, alias: str) -> bool: pass

    @abstractmethod
    def view(self) -> List[Vault]: pass

    @abstractmethod
    def reset(self) -> None: pass



class VaultRepositoryAsFile(VaultRepository):
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
