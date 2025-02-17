from typing import List, Dict
from abc import ABC, abstractmethod

from vaultscan.engines.base import BaseVaultConfig


class VaultRepository(ABC):
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def add(self, new_vault: BaseVaultConfig) -> bool: pass

    @abstractmethod
    def remove(self, alias: str) -> bool: pass

    @abstractmethod
    def rename(self, old_alias: str, new_alias: str) -> bool: pass

    @abstractmethod
    def get(self, alias: str) -> Dict: pass

    @abstractmethod
    def get_all(self) -> List[Dict]: pass

    @abstractmethod
    def reset(self) -> None: pass
