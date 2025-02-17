from unittest import TestCase
from typing import Dict

from vaultscan.engines.keepass import (
    KEEPASS,
    KeePassConfig
)


class TestKeePassConfig(TestCase):
    def test_to_dict(self):
        # When
        alias = 'keepass'
        keepass = KeePassConfig(
            alias = alias,
            path = 'C:\\database.kdbx',
            password = 'fake_password'
        )
        content = keepass.to_dict()

        # Then
        self.assertIsInstance(content, Dict)
        # Cheching some fields within the dictionary
        self.assertEqual(content['type'], KEEPASS)
        self.assertEqual(content['alias'], alias)

    def test_from_dict(self):
        # Given
        type = 'keepass'
        alias = 'keepass'
        path = 'C:\\database.kdbx'
        content = {
            'type': type,
            'alias': alias,
            'path': path,
            'password': {
                'encrypted': True,
                'value': 'gAAAAABnszFi8bBm9j8cxv-mbwrlHG8pYlaGAH2n-EWYNb6UMTU_3KoQNkFNrHsDuv7XVMxLK6Bz3leeBzWJY2dXuh_S-SwBbQ=='
            }
        }

        # When
        keepass = KeePassConfig.from_dict(content)

        # Then
        self.assertIsInstance(keepass, KeePassConfig)
        self.assertEqual(keepass.type, type)
        self.assertEqual(keepass.alias, alias)
        self.assertEqual(keepass.path, path)
        expected_password = 'fake_password'
        self.assertEqual(keepass.password, expected_password)


class TestKeePassSecretEngine(TestCase):
    pass