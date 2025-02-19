from unittest import TestCase


from vaultscan.repositories.config.factory import (
    ConfigRepositoryFactory,
    ConfigRepositoryType
)
from vaultscan.repositories.config.json import ConfigRepositoryAsJson
from vaultscan.repositories.config.in_memory import InMemoryConfigRepository


class TestConfigRepositoryFactory(TestCase):
    def test_create_when_default(self):
        repository = ConfigRepositoryFactory.create()
        self.assertIsInstance(repository, ConfigRepositoryAsJson)

    def test_create_when_json(self):
        repository = ConfigRepositoryFactory.create(
            type = ConfigRepositoryType.JSON
        )
        self.assertIsInstance(repository, ConfigRepositoryAsJson)

    def test_create_when_in_memory(self):
        repository = ConfigRepositoryFactory.create(
            type = ConfigRepositoryType.IN_MEMORY
        )
        self.assertIsInstance(repository, InMemoryConfigRepository)
