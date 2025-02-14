from dataclasses import dataclass
from typing import List, Dict
from abc import ABC, abstractmethod


@dataclass
class Vault:
    alias: str
    subscription_id: str
    resource_group_name: str
    vault_name: str

    @classmethod
    def from_dict(cls, content: Dict) -> 'Vault':
        return Vault(
            alias = content['alias'],
            subscription_id = content['subscription_id'],
            resource_group_name = content['resource_group_name'],
            vault_name = content['vault_name']
        )


class VaultRepository(ABC):
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def add(self, new_vault: Vault) -> bool: pass

    @abstractmethod
    def remove(self, alias: str) -> bool: pass

    @abstractmethod
    def get(self, alias: str) -> Dict: pass

    @abstractmethod
    def get_all(self) -> List[Dict]: pass

    @abstractmethod
    def reset(self) -> None: pass
