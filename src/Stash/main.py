#-------------------- Imports --------------------

from typing import Type, Callable, List

from src.Stash.Classes import create_slots_cls
from src.Stash.Cache import check_cache_value, return_cache_value, add_to_cache

#-------------------- Main Application --------------------

def Stash(Frozen: bool = False, Allow_fallback: bool = False, Preserve: List[str] = None) -> Callable[[Type], Type]:
    if not isinstance(Frozen, bool):
        raise TypeError(f"Parameter 'Frozen' must be of Type: Boolean, not {type(Frozen).__name__}'")
    if not isinstance(Allow_fallback, bool):
        raise TypeError(f"Parameter 'Allow_fallback' must be of Type: Boolean, not {type(Allow_fallback).__name__}")
    if Preserve is not None:
        if not isinstance(Preserve, list):
            raise TypeError(f"Parameter 'Preserve' must be of Type: List[str], not {type(Preserve).__name__}")
        if not all(isinstance(item, str) for item in Preserve):
            raise TypeError(f"All items in 'Preserve' must be of Type: str")

    def wrapper(cls: Type) -> Type:
        if Frozen:
            raise NotImplementedError("Immutable class generation is currently disabled")
        else:
            key = (cls, Allow_fallback, tuple(Preserve) if Preserve else ())

            if check_cache_value(key):
                return return_cache_value(key)

            new_cls = create_slots_cls(cls, Allow_fallback, Preserve)
            add_to_cache(key, new_cls)

            return new_cls

    return wrapper
    