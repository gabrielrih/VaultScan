from abc import ABC, abstractmethod
from typing import Any, Optional, Dict


class CacheProviderBase(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]: pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None: pass
    
    @abstractmethod
    def delete(self, key: str) -> bool: pass
    
    @abstractmethod
    def clear(self) -> None: pass
    
    @abstractmethod
    def exists(self, key: str) -> bool: pass
    
    @abstractmethod
    def get_stats(self) -> Dict: pass
