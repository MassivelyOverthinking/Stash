#-------------------- Imports --------------------

from typing import Type, Callable, List, Optional

from src.Stash.Classes import create_tuplex_cls, create_slots_cls

#-------------------- Main Application --------------------

def Stash(Frozen: bool = False, Allow_fallback: bool = False, Preserve: List[str] = None) -> Callable[[Type], Type]:
    if not isinstance(Frozen, bool):
        raise TypeError(f"Parameter 'Frozen' must be of Type: Boolean, not {type(Frozen).__name__}'")
    if not isinstance(Allow_fallback, bool):
        raise TypeError(f"Parameter 'Allow_fallback' must be of Type: Boolean, not {type(Allow_fallback).__name__}")
    if Preserve is not None and not isinstance(Preserve, list):
        raise TypeError(f"Parameter 'Preserve' must be of Type: List[str], not {type(Preserve).__name__}")

    def wrapper(cls: Type) -> Type:
        if Frozen:
            return  create_tuplex_cls(cls, Allow_fallback, Preserve)
        else:
            return  create_slots_cls(cls, Allow_fallback, Preserve)
    
    return wrapper
    