from unittest import TestCase


from vaultscan.repositories.secure_key.factory import SecureKeyRepositoryType, SecureKeyRepositoryFactory
from vaultscan.repositories.secure_key.keyring import KeyRingSecureKeyRepository
from vaultscan.repositories.secure_key.in_memory import InMemorySecureKeyRepository


class TestSecureKeyRepositoryFactory(TestCase):
    def test_create_when_default(self):
        repository = SecureKeyRepositoryFactory.create()
        self.assertIsInstance(repository, KeyRingSecureKeyRepository)

    def test_create_when_keyring(self):
        repository = SecureKeyRepositoryFactory.create(
            type = SecureKeyRepositoryType.KEYRING
        )
        self.assertIsInstance(repository, KeyRingSecureKeyRepository)

    def test_create_when_in_memory(self):
        repository = SecureKeyRepositoryFactory.create(
            type = SecureKeyRepositoryType.IN_MEMORY
        )
        self.assertIsInstance(repository, InMemorySecureKeyRepository)
