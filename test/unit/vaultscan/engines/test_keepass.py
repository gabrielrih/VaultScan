from unittest import TestCase
from unittest.mock import patch
from typing import Dict

from vaultscan.engines.base import VaultStatus
# from vaultscan.engines.keepass import (
#     KEEPASS,
#     KeePassConfig
# )


class TestKeePassConfig(TestCase):
    pass
    # def test_to_dict(self):
    #     # When
    #     alias = 'keepass'
    #     keepass = KeePassConfig(
    #         alias = alias,
    #         status = VaultStatus.ENABLED.value,
    #         path = 'C:\\database.kdbx',
    #         password = 'fake_password'
    #     )
    #     content = keepass.to_dict()

    #     # Then
    #     self.assertIsInstance(content, Dict)
    #     # Cheching some fields within the dictionary
    #     self.assertEqual(content['type'], KEEPASS)
    #     self.assertEqual(content['alias'], alias)

    # @patch('vaultscan.repositories.secure_key.cipher.DataCipher')
    # def test_from_dict(self, mock_datacipher):
    #     # Given
    #     mock_datacipher.return_value = MockDataCipher()
    #     type = 'keepass'
    #     alias = 'keepass'
    #     path = 'C:\\database.kdbx'
    #     status = VaultStatus.ENABLED
    #     content = {
    #         'type': type,
    #         'status': status,
    #         'alias': alias,
    #         'path': path,
    #         'password': {
    #             'encrypted': True,
    #             'value': 'gAAAAABnszFi8bBm9j8cxv-mbwrlHG8pYlaGAH2n-EWYNb6UMTU_3KoQNkFNrHsDuv7XVMxLK6Bz3leeBzWJY2dXuh_S-SwBbQ=='
    #         }
    #     }

    #     # When
    #     keepass = KeePassConfig.from_dict(content)

    #     # Then
    #     print(str(keepass))
    #     self.assertTrue(False)
    #     mock_datacipher.is_called_once()
    #     self.assertIsInstance(keepass, KeePassConfig)
    #     self.assertEqual(keepass.type, type)
    #     self.assertEqual(keepass.status, status)
    #     self.assertEqual(keepass.alias, alias)
    #     self.assertEqual(keepass.path, path)
    #     expected_password = 'fake_password'
    #     self.assertEqual(keepass.password, expected_password)



# class MockDataCipher:
#     def __init__(self, *args, **kwargs):
#         pass

#     @property
#     def key(self) -> str:
#         return 'fake_key'
    
#     def encrypt(self, value: str) -> str:
#         print("Entrou aqui Mock")
#         return f'encrypted-{value}'
    
#     def decrypt(self, value: str) -> str:
#         return value.replace('encrypted-', '')


class TestKeePassSecretEngine(TestCase):
    pass