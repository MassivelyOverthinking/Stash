#-------------------- Imports --------------------

import time
from typing import Type, Optional, Any
from collections import OrderedDict

#-------------------- Caching Configuration --------------------

MAX_CACHE_SIZE = 128
DEFAULT_TTL = 150

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
    if key in stash_cache:
        del stash_cache[key]

    while len(stash_cache) >= MAX_CACHE_SIZE:
        stash_cache.popitem(last=False)

    stash_cache[key] = CacheEntry(value, ttl)

def check_cache_value(key: Any) -> bool:
    entry = stash_cache.get(key)
    if entry is None:
        return False
    if entry.is_expired():
        del stash_cache[key]
        return False
    return True

def return_cache_value(key: Any) -> Optional[Type]:
    if check_cache_value(key):
        stash_cache.move_to_end(key)
        return stash_cache[key].value
    return None

def clear_cache():
    stash_cache.clear()