from unittest import TestCase


from vaultscan.repositories.vault.factory import VaultRepositoryType, VaultRepositoryFactory
from vaultscan.repositories.vault.json import VaultRepositoryAsJson


class TestVaultRepositoryFactory(TestCase):
    def test_create_when_default(self):
        repository = VaultRepositoryFactory.create()
        self.assertIsInstance(repository, VaultRepositoryAsJson)

    def test_create_when_json(self):
        repository = VaultRepositoryFactory.create(
            type = VaultRepositoryType.JSON
        )
        self.assertIsInstance(repository, VaultRepositoryAsJson)