import os

from unittest import TestCase
from typing import Dict, List, Any

from vaultscan.repositories.config.base import Config
from vaultscan.repositories.config.json import ConfigRepositoryAsJson
from vaultscan.repositories.file_handler import FileHandler


VALID_VERBOSE_CONFIG_NAME = 'verbose'
EXPECTED_VALID_CONFIG = {
    "name": VALID_VERBOSE_CONFIG_NAME,
    "value": "True"
}
EXPECTED_CONFIG_QUANTITY = 1


class TestConfigRepositoryAsJson(TestCase):
    def setUp(self):
        file = FakeJSONFileHandler('any_folder', 'any_file')
        self.repository = ConfigRepositoryAsJson(file = file)

    def test_set(self):
        config = Config(
            name = VALID_VERBOSE_CONFIG_NAME,
            value = 'True'
        )
        self.repository.set(new_config = config)

    def test_unset(self):
        self.repository.unset(name = VALID_VERBOSE_CONFIG_NAME)

    def test_get(self):
        config: Dict = self.repository.get(
            name = VALID_VERBOSE_CONFIG_NAME
        )
        self.assertIsInstance(config, Dict)
        self.assertEqual(config, EXPECTED_VALID_CONFIG)

    def test_get_all(self):
        configs: List[Dict] = self.repository.get_all()
        self.assertIsInstance(configs, List)
        self.assertEqual(
            len(configs),
            EXPECTED_CONFIG_QUANTITY,
            msg = f'Should have {EXPECTED_CONFIG_QUANTITY} config(s) on the response'
        )
        first_config: Dict = configs[0]
        self.assertEqual(
            first_config,
            EXPECTED_VALID_CONFIG,
            msg = 'The expected first config should be as defined on the EXPECTED_VALID_CONFIG variable'
        )


class FakeJSONFileHandler(FileHandler):
    ''' Simulating the JSONFileHandler class but without actually handling a file on disk '''
    def __init__(self, folder_name, filename):
        super().__init__(folder_name, filename)

    @property
    def path(self) -> str:
        return str(os.path.join(self.folder_name, self.filename))

    @property
    def exists(self) -> str:
        return False

    def read(self) -> Dict:
        fake_configs = {
            "configs": [ EXPECTED_VALID_CONFIG ]
        }
        return fake_configs

    def write(self, *args, **kwargs) -> None:
        '''There is no need to actually save the data anywhere, so do nothing here'''
        pass
