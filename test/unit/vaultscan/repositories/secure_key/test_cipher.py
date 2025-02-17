from unittest import TestCase, skip
from unittest.mock import patch

from vaultscan.repositories.secure_key.in_memory import InMemorySecureKeyRepository
from vaultscan.repositories.secure_key.cipher import DataCipher


class TestEncryption(TestCase):
    def setUp(self):
        self.repository = InMemorySecureKeyRepository()
        self.key_in_bytes = b'r8e2ulxoU_1TuHc1JKUw-nWBDOOXOfdlV8jWdWjSYEM='

    @patch('cryptography.fernet.Fernet.generate_key')
    def test_get_key(self, mock_generate_key):
        # Given
        mock_generate_key.return_value = MockFernetGenerateKey(
            expected_key_in_bytes = self.key_in_bytes 
        )
        cipher = DataCipher(repository = self.repository)

        # When
        key = cipher.key

        # Then
        mock_generate_key.is_called_once()
        self.assertEqual(key, self.key_in_bytes.decode(cipher.encoding))
        self.assertIsInstance(key, str)

    @patch('cryptography.fernet.Fernet.generate_key')
    def test_encrypt(self, mock_generate_key):
        # Given
        mock_generate_key.return_value = MockFernetGenerateKey(
            expected_key_in_bytes = self.key_in_bytes 
        )
        cipher = DataCipher(repository = self.repository)

        # When
        value = 'my_value'
        encrypted_value = cipher.encrypt(value)
        print(encrypted_value)

        # Then
        mock_generate_key.is_called_once()
        self.assertIsInstance(encrypted_value, str)
        self.assertGreaterEqual(
            len(encrypted_value),
            10,
            msg = 'The encrypted value should have more than 10 characteres'
        )

    @patch('cryptography.fernet.Fernet.generate_key')
    def test_decrypt(self, mock_generate_key):
        # Given
        mock_generate_key.return_value = MockFernetGenerateKey(
            expected_key_in_bytes = self.key_in_bytes 
        )
        cipher = DataCipher(repository = self.repository)
        expected_decrypted_value = 'my_value'

        # When
        encrypted_value = 'gAAAAABnsyoGUlB3d0y0kSozD-9dwpfL1g3wmGEpb4XnClBITOcv96ALjQT__eNfnapOVKkGVsEFkc5QQblRzp3mD6VTpATk5g=='
        value = cipher.decrypt(encrypted_value)

        # Then
        mock_generate_key.is_called_once()
        self.assertIsInstance(value, str)
        self.assertEqual(value, expected_decrypted_value)


class MockFernetGenerateKey:
    def __init__(self, expected_key_in_bytes: bytes):
        # Static fake key generated just for the unit tests
        self.key_in_bytes = expected_key_in_bytes #b'r8e2ulxoU_1TuHc1JKUw-nWBDOOXOfdlV8jWdWjSYEM='

    def decode(self, *args, **kwargs) -> str:
        return self.key_in_bytes.decode(*args, **kwargs)

    def __str__(self):
        return self.key_in_bytes.decode()


@skip(reason = 'Real repository implementation. The key is different on each computer')
class TestEncryptionUsingTheRealRepository(TestCase):
    ''' Using this class just sometimes to test the real implementation of
     keyring or other persistent repository
    '''
    def setUp(self):
        self.cipher = DataCipher()

    def test_get_key(self):
        key = self.cipher.key
        self.assertEqual(key, 'hKtsHyBd40NCAw65VULTdifqRIeSVjGFD2VVq4Dd-Mw=')
        self.assertIsInstance(key, str)

    def test_encrypt(self):
        value = 'my_value'
        encrypted_value = self.cipher.encrypt(value)
        self.assertIsInstance(encrypted_value, str)
        self.assertGreaterEqual(
            len(encrypted_value),
            10,
            msg = 'The encrypted value should have more than 10 characteres')

    def test_decrypt(self):
        encrypted_value = 'gAAAAABnsyEQ8fvOA32rPfKsjtTmHpovnyq5TSDLuz76VDTzVA0CNvprUc8L-18K_lK1M1QWk5jL50vOxt9dUA2mACPYTG6AMQ=='
        expected_decrypted_value = 'my_value'
        value = self.cipher.decrypt(encrypted_value)
        self.assertIsInstance(value, str)
        self.assertEqual(value, expected_decrypted_value)
