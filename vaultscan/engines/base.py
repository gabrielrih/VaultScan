from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod


@dataclass
class Secret:
    vault: str
    name: str
    value: Optional[str] = ''


@dataclass
class BaseVaultConfig:
    alias: str
    type: str = field(init = False)  # Each subclass should set this

    def __post_init__(self):
        if not hasattr(self, "type"):
            raise NotImplementedError("Subclasses must define a 'type attribute")

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, content: Dict) -> 'BaseVaultConfig': pass


class FilterType(Enum):
    BY_MATCH = 'match', lambda value, filter: value == filter
    BY_REGEX = 'regex', lambda value, filter: filter in value

    def __init__(self, _, matcher):
        self.matcher = matcher


class BaseVaultEngine(ABC):
    def __init__(self, vault: BaseVaultConfig):
        self.vault = vault

    @abstractmethod
    def find(self, filter: str, type: FilterType, is_value: bool = False) -> List[Secret]: pass

    def is_match(self, values: List[str], filter: str, type: FilterType) -> bool:
        if not isinstance(type, FilterType):
            raise ValueError(f'Invalid FilterType {str(type)}!')
        return any(type.matcher(value, filter) for value in values)
