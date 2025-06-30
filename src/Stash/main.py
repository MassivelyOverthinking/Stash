#-------------------- Imports --------------------

from typing import Type, Callable, List, Optional

from src.Stash.Classes import create_slots_cls, CacheConfig
from src.Stash.Cache import CacheManager

#-------------------- Main Application --------------------

def Stash(
        freeze: bool = False,
        preserve: List[str] = None,
        config: Optional[CacheConfig] = None
    ) -> Callable[[Type], Type]:

    if not isinstance(freeze, bool):
        raise TypeError(f"Paramater 'Freeze' must be of Type: Boolean, not {type(freeze).__name__}")
    if preserve is not None:
        if not isinstance(preserve, list):
            raise TypeError(f"Parameter 'Preserve' must be of Type: List[str], not {type(preserve).__name__}")
        if not all(isinstance(item, str) for item in preserve):
            raise TypeError(f"All items in 'Preserve' must be of Type: str")
    if config is not None and not isinstance(config, CacheConfig):
        raise TypeError(f"Parameter 'Config' must be of Type: CacheConfig, not {type(config).__name__}")
    
    cache_manager = CacheManager(config)

    def wrapper(cls: Type) -> Type:

        key = (cls.__name__, cls.__module__, cls.__qualname__, id(cls))

        if cache_manager.validate_cache_value(key):
            return cache_manager.return_cache_value(key)
        
        new_cls = create_slots_cls(cls, freeze, preserve)
        cache_manager.add_to_cache(key, new_cls)

        return new_cls

    return wrapper
    