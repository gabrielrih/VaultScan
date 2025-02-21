import keyring

from vaultscan.repositories.secure_key.base import SecureKeyRepository
from vaultscan.util.package import PACKAGE_NAME


class KeyRingSecureKeyRepository(SecureKeyRepository):
    ''' Repository implementation to persist secure keys using the keyring library '''
    def initialize(self):
        pass

    def add(self, name: str, value: str) -> None:
        keyring.set_password(
            service_name = PACKAGE_NAME,
            username = name,
            password = value
        )
        return None

    def remove(self, name: str) -> None: 
        keyring.delete_password(
            service_name = PACKAGE_NAME,
            username = name
        )

    def get(self, name: str) -> str:
        value = keyring.get_password(
            service_name = PACKAGE_NAME,
            username = name
        )
        if not value:  # to avoid returning None
            return ''
        return value
