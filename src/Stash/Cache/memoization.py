#-------------------- Imports --------------------

from typing import Type, Optional, Any

#-------------------- Caching --------------------

stash_cache: dict[Any, Any] = {}

def add_to_cache(key: Any, value: Type) -> None:
    stash_cache.update({key: value})

def clear_cache():
    stash_cache.clear()

def check_cache_value(key: Any) -> bool:
    return key in stash_cache

def return_cache_value(key: Any) -> Optional[Type]:
    return stash_cache.get(key)