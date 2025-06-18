#-------------------- Imports --------------------

from typing import Type, Callable

#-------------------- Main Application --------------------

def Stash(Frozen: bool = False) -> Callable[[Type], Type]:
    if not isinstance(Frozen, bool):
        raise TypeError(f"Parameter 'Forzen must be of Type: Boolean, not {type(Frozen.__name__)}'")

    def wrapper(cls: Type) -> Type:
        if Frozen:
            return  # Not specified yet (Class-type)
        else:
            return  # Not specified yet (Class-type)
    
    return wrapper
    