#-------------------- Imports --------------------

from typing import Type, Callable

from src.Stash.Classes import create_tuplex_cls, create_slots_cls

#-------------------- Main Application --------------------

def Stash(Frozen: bool = False) -> Callable[[Type], Type]:
    if not isinstance(Frozen, bool):
        raise TypeError(f"Parameter 'Frozen' must be of Type: Boolean, not {type(Frozen).__name__}'")

    def wrapper(cls: Type) -> Type:
        if Frozen:
            return  create_tuplex_cls(cls)
        else:
            return  create_slots_cls(cls)
    
    return wrapper
    