#-------------------- Imports --------------------

from typing import Type, Callable, List, Optional

from src.Stash.Classes import create_slots_cls, CacheConfig
from src.Stash.Cache import CacheManager

#-------------------- Main Application --------------------

def Stash(
        Allow_fallback: bool = False,
        Preserve: List[str] = None,
        Config: Optional[CacheConfig] = None
    ) -> Callable[[Type], Type]:

    if not isinstance(Allow_fallback, bool):
        raise TypeError(f"Parameter 'Allow_fallback' must be of Type: Boolean, not {type(Allow_fallback).__name__}")
    if Preserve is not None:
        if not isinstance(Preserve, list):
            raise TypeError(f"Parameter 'Preserve' must be of Type: List[str], not {type(Preserve).__name__}")
        if not all(isinstance(item, str) for item in Preserve):
            raise TypeError(f"All items in 'Preserve' must be of Type: str")
    if Config is not None and not isinstance(Config, CacheConfig):
        raise TypeError(f"Parameter 'Config' must be of Type: CacheConfig, not {type(Config).__name__}")
    
    cache_manager = CacheManager(Config)

    def wrapper(cls: Type) -> Type:

        key = (cls.__name__, cls.__module__, cls.__qualname__, id(cls))

        if cache_manager.validate_cache_value(key):
            return cache_manager.return_cache_value(key)
        
        new_cls = create_slots_cls(cls, Allow_fallback, Preserve)
        cache_manager.add_to_cache(key, new_cls)

        return new_cls

    return wrapper
    