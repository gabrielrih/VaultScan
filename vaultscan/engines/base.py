from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC


@dataclass
class Secret:
    vault: str
    name: str
    value: Optional[str] = ''


class EngineType(Enum):
    AZURE_KEY_VAULT = 'key_vault'
    KEYPASS = 'keypass'


@dataclass
class BaseVaultConfig:
    alias: str
    type: EngineType = field(init = False)  # Each subclass should set this

    def __post_init__(self):
        if not hasattr(self, "type"):
            raise NotImplementedError("Subclasses must define a 'type attribute")
        
    @classmethod
    def from_list(cls, content: List[Dict]) -> List['BaseVaultConfig']: pass

    @classmethod
    def from_dict(cls, content: Dict) -> 'BaseVaultConfig': pass


class BaseVaultEngine(ABC):
    def __init__(self, vault: BaseVaultConfig):
        self.vault = vault

    def find_by_regex(self, secret_name: str) -> List[Secret]: pass

    def find_by_name(self, secret_name: str) -> List[Secret]: pass
