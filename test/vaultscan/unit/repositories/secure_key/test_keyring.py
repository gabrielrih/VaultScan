from unittest import TestCase
from unittest.mock import patch

from vaultscan.repositories.secure_key.keyring import KeyRingSecureKeyRepository
from vaultscan.util.package import PACKAGE_NAME

class TestKeyRingSecureKeyRepository(TestCase):
    @patch('vaultscan.repositories.secure_key.keyring.keyring')
    def test_add(self, mock_keyring):
        repo = KeyRingSecureKeyRepository()
        repo.add('test_key', 'test_key_value')
        mock_keyring.set_password.assert_called_once_with(
            service_name=PACKAGE_NAME,
            username='test_key',
            password='test_key_value'
        )

    @patch('vaultscan.repositories.secure_key.keyring.keyring')
    def test_remove(self, mock_keyring):
        repo = KeyRingSecureKeyRepository()
        repo.remove('test_key')
        mock_keyring.delete_password.assert_called_once_with(
            service_name=PACKAGE_NAME,
            username='test_key'
        )

    @patch('vaultscan.repositories.secure_key.keyring.keyring')
    def test_get_existing_key(self, mock_keyring):
        mock_keyring.get_password.return_value = 'test_key_value'
        repo = KeyRingSecureKeyRepository()
        result = repo.get('test_key')
        mock_keyring.get_password.assert_called_once_with(
            service_name=PACKAGE_NAME,
            username='test_key'
        )
        self.assertEqual(result, 'test_key_value')

    @patch('vaultscan.repositories.secure_key.keyring.keyring')
    def test_get_non_existing_key(self, mock_keyring):
        mock_keyring.get_password.return_value = None  # Simulating no stored password
        repo = KeyRingSecureKeyRepository()
        result = repo.get('non_existent_user')
        
        mock_keyring.get_password.assert_called_once_with(
            service_name=PACKAGE_NAME,
            username='non_existent_user'
        )
        self.assertEqual(result, '')  # Should return an empty string
