from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

from vaultscan.repositories.vault.base import BaseVaultConfig


@dataclass
class Secret:
    vault: str
    name: str
    value: Optional[str] = ''


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
