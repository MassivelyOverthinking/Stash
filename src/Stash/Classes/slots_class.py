#-------------------- Imports --------------------

from typing import Type, List, Optional
from src.Stash.Utils import check_cls, check_metadata, preserve_methods

#-------------------- Slots Class (Mutable) --------------------

def create_slots_cls(cls: Type, allow_fallback: bool, preserve: Optional[List[str]]) -> Type:
    fields = check_cls(cls, allow_fallback)

    class_dict = dict(cls.__dict__)
    class_dict["__slots__"] = tuple(fields)

    class_dict.pop("__dict__", None)
    class_dict.pop("__weakref__", None)

    class_dict = {key: value for key, value in class_dict.items() if not (key.startswith("__") and key.endswith("__") and key not in ("__slots__", "__init__"))}

    new_class = type(cls.__name__, cls.__bases__, class_dict)
    
    check_metadata(cls, new_class)

    preserve_methods(cls, new_class, preserve)

    return new_class