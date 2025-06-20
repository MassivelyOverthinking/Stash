#-------------------- Imports --------------------

from typing import Type, Callable

from src.Stash.Classes import create_tuplex_cls, create_slots_cls

#-------------------- Main Application --------------------

def Stash(Frozen: bool = False, Allow_fallback: bool = False) -> Callable[[Type], Type]:
    if not isinstance(Frozen, bool):
        raise TypeError(f"Parameter 'Frozen' must be of Type: Boolean, not {type(Frozen).__name__}'")
    if not isinstance(Allow_fallback, bool):
        raise TypeError(f"Parameter 'Allow_fallback' must be of Type: Boolean, not {type(Allow_fallback).__name__}")

    def wrapper(cls: Type) -> Type:
        if Frozen:
            return  create_tuplex_cls(cls, Allow_fallback)
        else:
            return  create_slots_cls(cls, Allow_fallback)
    
    return wrapper
    