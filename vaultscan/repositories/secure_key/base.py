from abc import ABC, abstractmethod


class SecureKeyRepository(ABC):
    ''' Base class to a repository of secure keys '''
    @abstractmethod
    def initialize(self): pass

    @abstractmethod
    def add(self, name: str, value: str) -> None: pass

    @abstractmethod
    def remove(self, name: str) -> None: pass

    @abstractmethod
    def get(self, name: str) -> str: pass
