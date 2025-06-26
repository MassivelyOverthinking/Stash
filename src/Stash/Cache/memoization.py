#-------------------- Imports --------------------

import time
import threading
from typing import Type, Optional, Any
from collections import OrderedDict, abc
from src.Stash.Classes.cacheconfig import CacheConfig

#-------------------- Caching Mechanism --------------------

class CacheEntry():
    __slots__ = ("value", "expiry")

    def __init__(self, value: Any, ttl: int = 600):
        self.value = value
        self.expiry = time.time() + ttl

    def is_expired(self):
        return time.time() > self.expiry

class CacheManager():
    __slots__ = ("config", "cache", "lock")

    def __init__(self, config: Optional[CacheConfig] = None):
        self.config = config or CacheConfig()
        self.cache: "OrderedDict[Any, CacheEntry]" = OrderedDict()
        self.lock = threading.RLock()

    def add_to_cache(self, key: Any, value: Any) -> None:
        with self.lock:

            self.delete_expired()

            if not isinstance(key, abc.Hashable):
                raise TypeError(f"Caching key must be a hashable value - Current type: {type(key)}")
            
            if key in self.cache:
                self.cache.pop(key, None)

            while len(self.cache) >= self.config.MAX_CACHE_SIZE:
                self.cache.popitem(last=False)

            self.cache[key] = CacheEntry(
                value=value,
                ttl=self.config.DEFAULT_TTL
            )

    def validate_cache_value(self, key: Any) -> bool:
        with self.lock:
            entry = self.cache.get(key)
            if entry is None:
                return False
            if entry.is_expired():
                self.cache.pop(key, None)
                return False
            return True
        
    def return_cache_value(self, key: Any) -> Optional[Type]:
        with self.lock:
            if self.validate_cache_value(key):
                self.cache.move_to_end(key)
                return self.cache[key].value
            return None
        
    def delete_expired(self) -> None:
        with self.lock:
            for key, value in list(self.cache.items()):
                if value.is_expired():
                    del self.cache[key]

    def clear_cache(self) -> None:
        with self.lock:
            self.cache.clear()