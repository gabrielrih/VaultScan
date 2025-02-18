from typing import List, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields


@dataclass
class Config:
    name: str
    value: str

    @classmethod
    def from_dict(cls, content: Dict) -> 'Config':
        kwargs = {}
        for f in fields(cls):
            kwargs[f.name] = content.get(f.name)
        return cls(**kwargs)

    def to_dict(self) -> Dict:
        return self.__dict__


class ConfigRepository(ABC):
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def set(self, new_config: Config) -> None: pass

    @abstractmethod
    def unset(self, name: str) -> None: pass

    @abstractmethod
    def get(self, name: str) -> Dict: pass

    @abstractmethod
    def get_all(self) -> List[Dict]: pass
