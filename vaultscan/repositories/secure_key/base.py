from abc import ABC, abstractmethod


class SecureKeyRepository(ABC):
    SERVICE_NAME = 'vaultscan'
    
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def add(self, name: str, value: str) -> None: pass

    @abstractmethod
    def remove(self, name: str) -> None: pass

    @abstractmethod
    def get(self, name: str) -> str: pass
