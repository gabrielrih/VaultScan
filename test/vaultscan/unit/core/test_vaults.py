from unittest import TestCase
from unittest.mock import patch, MagicMock
from typing import List, Dict

from vaultscan.core.vaults import get_vaults
from vaultscan.repositories.vault.factory import VaultRepositoryFactory


class TestGetVaults(TestCase):
    @patch.object(VaultRepositoryFactory, 'create')
    def test_get_vaults_no_filter(self, mock_create):
        # Given
        mock_vault_repo = MagicMock()
        mock_vault_repo.get_all.return_value = [{'alias': 'vault1'}, {'alias': 'vault2'}]
        mock_create.return_value = mock_vault_repo
        
        # When
        vaults: List[Dict] = get_vaults()
        
        # Then
        mock_vault_repo.get_all.assert_called_once()
        self.assertIsInstance(vaults, List)
        self.assertEqual(vaults, [{'alias': 'vault1'}, {'alias': 'vault2'}])
    
    @patch.object(VaultRepositoryFactory, 'create')
    def test_get_vaults_with_existing_vault(self, mock_create):
        # Given
        mock_vault_repo = MagicMock()
        vault_alias = 'vault1'
        mock_vault_repo.get.return_value = {'alias': vault_alias}
        mock_create.return_value = mock_vault_repo
        
        # When
        vaults: List[Dict] = get_vaults(only_vault = vault_alias)
        
        # Then
        mock_vault_repo.get.assert_called_once_with(alias='vault1')
        self.assertIsInstance(vaults, List)
        self.assertEqual(vaults, [{'alias': 'vault1'}])
    
    @patch.object(VaultRepositoryFactory, 'create')
    def test_get_vaults_with_non_existing_vault(self, mock_create):
        # Given
        mock_vault_repo = MagicMock()
        mock_vault_repo.get.return_value = None
        mock_create.return_value = mock_vault_repo
        unknown_alias = 'unknown_vault'
        
        # When
        vaults: List[Dict] = get_vaults(only_vault = unknown_alias)
        
        # Then
        mock_vault_repo.get.assert_called_once_with( alias = unknown_alias)
        self.assertIsInstance(vaults, List)
        self.assertEqual(vaults, [])
