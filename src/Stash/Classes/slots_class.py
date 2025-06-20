#-------------------- Imports --------------------

from typing import Type
from collections import namedtuple
from src.Stash.Utils import check_cls, check_metadata

#-------------------- Slots Class (Mutable) --------------------

def create_slots_cls(cls: Type, allow_fallback: bool) -> Type:
    fields = check_cls(cls, allow_fallback)

    class_dict = dict(cls.__dict__)
    class_dict["__slots__"] = tuple(fields)

    class_dict.pop("__dict__", None)
    class_dict.pop("__weakref__", None)

    class_dict = {key: value for key, value in class_dict.items() if not (key.startswith("__") and key.endswith("__") and key not in ("__slots__", "__init__"))}

    new_class = type(cls.__name__, cls.__bases__, class_dict)
    
    check_metadata(cls, new_class)

    return new_class