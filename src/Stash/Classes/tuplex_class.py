#-------------------- Imports --------------------

from typing import Type
from collections import namedtuple
from src.Stash.Utils import check_cls, check_metadata

import types

#-------------------- Tuplex Class (Immutable) --------------------

def create_tuplex_cls(cls: Type) -> Type:
    fields = check_cls(cls)

    NTBase = namedtuple(f"{cls.__name__}", fields)

    new_class = type(cls.__name__, (NTBase,), {
        "__slots__": (),
    })

    for name, attr in cls.__dict__.items():
        if isinstance(attr, types.FunctionType) and not name.startswith("__"):
            setattr(new_class, name, attr)

    check_metadata(cls, new_class)

    return new_class