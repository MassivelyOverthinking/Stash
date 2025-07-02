#-------------------- Imports --------------------

from typing import Type, Callable, List

from src.Stash.Classes import create_slots_cls
from src.Stash.Cache import get_global_cache_manager

#-------------------- Main Application --------------------

def Stash(
        freeze: bool = False,
        preserve: List[str] = None
    ) -> Callable[[Type], Type]:

    """
    A Python class-decorator designed for memory optimization by dynamically generating a __slots__-bassed class.

    Decorator reduces general memory overhead by eliminating __dict__,
    and automatically generating __init__, __repr__, __eq__ methods.

    Args:
        Freeze (bool): If True, prevents attribute mutation after instantiation.
        Preserve (list[str]): List of individual methods preserved from teh original class.

    Returns:
        Callable[[Type], Type]Dynamically creates a new class-object instead of initial class.

    Exceptions:
        TypeErrors: Raised if individual params are not of the correct Type. 
    """

    if not isinstance(freeze, bool):
        raise TypeError(f"Paramater 'Freeze' must be of Type: Boolean, not {type(freeze).__name__}")
    if preserve is not None:
        if not isinstance(preserve, list):
            raise TypeError(f"Parameter 'Preserve' must be of Type: List[str], not {type(preserve).__name__}")
        if not all(isinstance(item, str) for item in preserve):
            raise TypeError(f"All items in 'Preserve' must be of Type: str")
    
    cache_manager = get_global_cache_manager()

    def wrapper(cls: Type) -> Type:

        key = (
            cls.__module__,
            cls.__qualname__,
            tuple(sorted(cls.__annotations__.items())),
            freeze,
            tuple(sorted(preserve or ()))
        )

        cached = cache_manager.get(key)
        if cached is not None:
            return cached
        
        new_cls = create_slots_cls(cls, freeze, preserve)
        cache_manager.add(key, new_cls)

        return new_cls

    return wrapper
    