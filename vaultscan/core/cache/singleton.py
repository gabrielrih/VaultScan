from typing import Optional

from vaultscan.core.cache.disk_cache import DiskCacheProvider
from vaultscan.core.cache.base import CacheProviderBase
from vaultscan.core.configs import AvailableConfigs, ConfigManager


class CacheManagerSingleton:
    _instance: Optional[CacheProviderBase] = None
    
    @classmethod
    def get_instance(cls) -> CacheProviderBase:
        if cls._instance is None:
            cache_ttl = ConfigManager(AvailableConfigs.CACHE_TTL).get_value()
            cls._instance = DiskCacheProvider(
                cache_dir = '.cache/vaultscan',
                default_ttl = cache_ttl
            )
        return cls._instance
