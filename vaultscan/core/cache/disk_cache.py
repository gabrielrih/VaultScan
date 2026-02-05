from typing import Any, Optional, Dict
from diskcache import Cache as DiskCache
from pathlib import Path

from vaultscan.core.cache.base import CacheProviderBase
from vaultscan.core.output.logger import LoggerFactory


logger = LoggerFactory.get_logger(__name__)


class DiskCacheProvider(CacheProviderBase):
    def __init__(self, cache_dir: str = ".cache/vaultscan", default_ttl: int = 600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        self._cache = DiskCache(cache_dir)
        logger.debug(f"Cache initialized at {cache_dir}")
    
    def get(self, key: str) -> Optional[Any]:
        value = self._cache.get(key)
        logger.debug(f"Cache {'HIT' if value is not None else 'MISS'} for key: {key}")
        return value
    
    def set(self, key: str, value: Any) -> None:
        self._cache.set(key, value, expire = self.default_ttl)
        logger.debug(f"Cache SET for key: {key} (TTL: {self.default_ttl}s)")
    
    def delete(self, key: str) -> bool:
        result = self._cache.delete(key)
        logger.debug(f"Cache DELETE for key: {key} - {'Success' if result else 'Not found'}")
        return result
    
    def clear(self) -> None:
        self._cache.clear()
    
    def exists(self, key: str) -> bool:
        return key in self._cache
    
    def get_stats(self) -> Dict:
        cache_path = Path(self.cache_dir)
        total_size = sum(f.stat().st_size for f in cache_path.rglob('*') if f.is_file())
        keys_list = list(self._cache.iterkeys())
        return {
            'cache_dir': self.cache_dir,
            'default_ttl_seconds': self.default_ttl,
            'size': {
                'bytes': total_size,
                'mb': round(total_size / (1024 * 1024), 2),  
            },
            'keys': {
                'total_keys': len(self._cache),
                'sample_keys': keys_list[:5] if keys_list else []  # Show first 5 keys as sample
            }
        }
