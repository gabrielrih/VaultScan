import os

from unittest import TestCase
from typing import Dict, List, Any

from vaultscan.core.engines.key_vault import KeyVaultConfig
from vaultscan.repositories.vault.json import VaultRepositoryAsJson
from vaultscan.repositories.vault.base import VaultStatus
from vaultscan.repositories.file_handler import FileHandler


ALREADY_EXISTED_VAULT_NAME = 'vault_one'
VAULT_NAME_THAT_DOESNT_EXIST = 'new_vault'


class TestVaultRepositoryAsJson(TestCase):
    def setUp(self):
        file = FakeJSONFileHandler('any_folder', 'any_file')
        self.repository = VaultRepositoryAsJson(file = file)

    def test_add_when_its_new(self):
        vault = KeyVaultConfig(
            alias = VAULT_NAME_THAT_DOESNT_EXIST,
            status = VaultStatus.ENABLED.value,
            vault_name = VAULT_NAME_THAT_DOESNT_EXIST
        )
        added = self.repository.add(new_vault = vault)
        self.assertTrue(
            added,
            msg = 'The vault should have been added!'
        )

    def test_add_when_it_already_exists(self):
        vault = KeyVaultConfig(
            alias = ALREADY_EXISTED_VAULT_NAME,
            status = VaultStatus.ENABLED.value,
            vault_name = ALREADY_EXISTED_VAULT_NAME
        )
        added = self.repository.add(new_vault = vault)
        self.assertFalse(
            added,
            msg = 'The vault should not have been added because it already exists on the configuration!'
        )

    def test_remove_when_it_doesnt_exist(self):
        removed = self.repository.remove(
            alias = VAULT_NAME_THAT_DOESNT_EXIST
        )
        self.assertFalse(
            removed,
            msg = 'The alias should not have been removed because it should not exist on the configuration'
        )

    def test_remove_when_it_exists(self):
        removed = self.repository.remove(
            alias = ALREADY_EXISTED_VAULT_NAME
        )
        self.assertTrue(
            removed,
            msg = 'The alias should have been removed because it exists on the configuration'
        )
        
    def test_remove_all(self):
        self.repository.remove_all()

    def test_rename_when_it_doesnt_exist(self):
        renamed = self.repository.rename(
            old_alias = VAULT_NAME_THAT_DOESNT_EXIST,
            new_alias = 'any_alias'
        )
        self.assertFalse(
            renamed,
            msg = 'The vault should not have been renamed because it doesnt exist on the configuration'
        )

    def test_rename_when_it_exists(self):
        renamed = self.repository.rename(
            old_alias = ALREADY_EXISTED_VAULT_NAME,
            new_alias = 'any_alias'
        )
        self.assertTrue(
            renamed,
            msg = 'The vault should have been renamed because it exists on the configuration'
        )

    def test_change_status_when_it_doesnt_exist(self):
        changed = self.repository.change_status(
            alias = VAULT_NAME_THAT_DOESNT_EXIST,
            status = VaultStatus.DISABLED
        )
        self.assertFalse(
            changed,
            msg = 'The vault should not have been changed because it doesnt exist on the configuration'
        )

    def test_change_status_when_it_exists(self):
        changed = self.repository.change_status(
            alias = ALREADY_EXISTED_VAULT_NAME,
            status = VaultStatus.DISABLED
        )
        self.assertTrue(
            changed,
            msg = 'The vault should have been changed because it exists on the configuration'
        )

    def test_get_when_it_doesnt_exist(self):
        vault: Dict = self.repository.get(
            alias = VAULT_NAME_THAT_DOESNT_EXIST
        )
        self.assertIsInstance(vault, Dict)
        self.assertEqual(vault, {})

    def test_get_when_it_exists(self):
        vault: Dict = self.repository.get(
            alias = ALREADY_EXISTED_VAULT_NAME
        )
        self.assertIsInstance(vault, Dict)
        self.assertEqual(vault['alias'], ALREADY_EXISTED_VAULT_NAME)

    def test_get_all(self):
        vaults: List[Dict] = self.repository.get_all()
        self.assertIsInstance(vaults, List)
        expected_qty_of_vaults = 1
        self.assertEqual(len(vaults), expected_qty_of_vaults)


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
        fake_vaults = {
            "vaults": [
                {
                    "alias": ALREADY_EXISTED_VAULT_NAME,
                    "type": "key_vault",
                    "vault_name": ALREADY_EXISTED_VAULT_NAME,
                    "status": "enabled"
                }
            ]
        }
        return fake_vaults

    def write(self, *args, **kwargs) -> None:
        '''There is no need to actually save the data anywhere, so do nothing here'''
        pass
