from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod


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
