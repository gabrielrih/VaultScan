from enum import Enum, auto

from vaultscan.repositories.secure_key.base import SecureKeyRepository
from vaultscan.repositories.secure_key.keyring import KeyRingSecureKeyRepository
from vaultscan.repositories.secure_key.in_memory import InMemorySecureKeyRepository


class SecureKeyRepositoryType(Enum):
    KEYRING = auto()
    IN_MEMORY = auto()


class SecureKeyRepositoryFactory:
    @staticmethod
    def create(type: SecureKeyRepositoryType = SecureKeyRepositoryType.KEYRING) -> SecureKeyRepository:
        if type == SecureKeyRepositoryType.KEYRING:
            return KeyRingSecureKeyRepository()
        if type == SecureKeyRepositoryType.IN_MEMORY:
            return InMemorySecureKeyRepository()
        raise ValueError(f'The specified SecureKeyRepositoryType {type} is not valid!')
