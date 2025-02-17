from cryptography.fernet import Fernet

from vaultscan.repositories.secure_key.base import SecureKeyRepository
from vaultscan.repositories.secure_key.keyring import KeyRingSecureKeyRepository
from vaultscan.util.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


class DataCipher:
    def __init__(self, repository: SecureKeyRepository = KeyRingSecureKeyRepository()):
        self.repository = repository
        self.key_name = 'global_key'
        self.encoding = 'utf-8'
        self.cipher = Fernet(
            key = self.key
        )

    @property
    def key(self) -> str:
        value = self.repository.get(name = self.key_name)
        if value:
            logger.debug('The key already exists on a persistent repository, so just returning it')
            return value
        logger.debug('Generating and saving a new key to be used on encryption')
        key = Fernet.generate_key().decode(encoding = self.encoding)
        self.repository.add(
            name = self.key_name,
            value = key
        )
        return str(key)


    def encrypt(self, value: str) -> str:
        encrypted_value = self.cipher.encrypt(
            data = value.encode(self.encoding)
        ).decode()
        return encrypted_value

    def decrypt(self, encrypted_value: str) -> str:
        value = self.cipher.decrypt(
            token = encrypted_value.encode(encoding = self.encoding)
        ).decode()
        return value
