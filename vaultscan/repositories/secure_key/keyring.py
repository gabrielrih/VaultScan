import keyring

from vaultscan.repositories.secure_key.base import SecureKeyRepository


class KeyRingSecureKeyRepository(SecureKeyRepository):
    def initialize(self):
        pass

    def add(self, name: str, value: str) -> None:
        keyring.set_password(
            service_name = self.SERVICE_NAME,
            username = name,
            password = value
        )
        return None

    def remove(self, name: str) -> None: 
        keyring.delete_password(
            service_name = self.SERVICE_NAME,
            username = name
        )

    def get(self, name: str) -> str:
        value = keyring.get_password(
            service_name = self.SERVICE_NAME,
            username = name
        )
        if not value:  # to avoid returning None
            return ''
        return value
