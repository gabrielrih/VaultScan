from dataclasses import dataclass, field
from enum import Enum
from abc import ABC


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


class BaseVaultEngine(ABC):
    pass
