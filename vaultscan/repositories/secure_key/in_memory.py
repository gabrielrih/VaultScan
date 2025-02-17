from vaultscan.repositories.secure_key.base import SecureKeyRepository


class InMemorySecureKeyRepository(SecureKeyRepository):
    def __init__(self):
        self.keys = list()

    def initialize(self):
        self.keys.content = list()

    def add(self, name: str, value: str) -> None:
        content = {
            'name': name,
            'value': value
        }
        self.keys.append(content)
        return None

    def remove(self, name: str) -> None: 
        for key in self.keys:
            if key['name'] == name:
                self.keys.remove(key)
        return None

    def get(self, name: str) -> str:
        if not self.keys:
            return ''
        for key in self.keys:
            if key['name'] == name:
                return str(key['value'])
        return ''
