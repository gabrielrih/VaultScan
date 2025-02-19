from typing import List, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class VaultStatus(Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'


@dataclass
class BaseVaultConfig:
    alias: str
    type: str = field(init = False)  # Each subclass should set this
    status: str

    def __post_init__(self):
        if not hasattr(self, "type"):
            raise NotImplementedError("Subclasses must define a 'type attribute")

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, content: Dict) -> 'BaseVaultConfig': pass


class VaultRepository(ABC):
    ''' Base class to repository of vaults '''
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def add(self, new_vault: BaseVaultConfig) -> bool: pass

    @abstractmethod
    def remove(self, alias: str) -> bool: pass

    @abstractmethod
    def remove_all(self) -> None: pass

    @abstractmethod
    def rename(self, old_alias: str, new_alias: str) -> bool: pass

    @abstractmethod
    def change_status(self, alias: str, status: VaultStatus) -> bool: pass

    @abstractmethod
    def get(self, alias: str) -> Dict: pass

    @abstractmethod
    def get_all(self) -> List[Dict]: pass
