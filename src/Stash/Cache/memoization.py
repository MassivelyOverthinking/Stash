#-------------------- Imports --------------------

import time
import threading
from typing import Type, Optional, Any
from collections import OrderedDict, abc

#-------------------- Caching Configuration --------------------

MAX_CACHE_SIZE = 68
DEFAULT_TTL = 150
CACHING_LOCK = threading.RLock()

#-------------------- Caching Mechanism --------------------

class CacheEntry():
    __slots__ = ("value", "expiry")

    def __init__(self, value: Any, ttl: int = DEFAULT_TTL):
        self.value = value
        self.expiry = time.time() + ttl

    def is_expired(self):
        return time.time() > self.expiry
        

stash_cache: "OrderedDict[Any, CacheEntry]" = OrderedDict()


def add_to_cache(key: Any, value: Any, ttl: int = DEFAULT_TTL) -> None:
    with CACHING_LOCK:

        delete_expired()

        if not isinstance(key, abc.Hashable):
            raise TypeError(f"Caching key must be a hashable value - Current type: {type(key)}")

        if key in stash_cache:
            stash_cache.pop(key, None)

        while len(stash_cache) >= MAX_CACHE_SIZE:
            stash_cache.popitem(last=False)

        stash_cache[key] = CacheEntry(value, ttl)


def validate_cache_value(key: Any) -> bool:
        with CACHING_LOCK:
            entry = stash_cache.get(key)
            if entry is None:
                return False
            if entry.is_expired():
                stash_cache.pop(key, None)
                return False
            return True
    

def return_cache_value(key: Any) -> Optional[Type]:
    with CACHING_LOCK:
        if validate_cache_value(key):
            stash_cache.move_to_end(key)
            return stash_cache[key].value
        return None


def delete_expired():
    with CACHING_LOCK:
        for key, value in list(stash_cache.items()):
            if value.is_expired():
                del stash_cache[key]


def clear_cache():
    with CACHING_LOCK:
        stash_cache.clear()