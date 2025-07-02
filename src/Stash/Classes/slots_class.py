#-------------------- Imports --------------------

from typing import Type, List, Optional
from src.Stash.Utils import check_metadata, get_annotations, create_init, create_repr, create_eq, create_frozen_setattr, conserve_methods

#-------------------- Slots Class (Mutable) --------------------

def create_slots_cls(cls: Type, freeze: bool) -> Type:
    fields_info = get_annotations(cls)
    slot_names = [field.value_name for field in fields_info]

    class_dict = {"__slots__": tuple(slot_names + (["_frozen"] if freeze else []))}

    for field in fields_info:
        if field.has_default:
            class_dict[field.value_name] = field.default_value

    class_dict["__init__"] = create_init(fields_info, freeze)
    class_dict["__repr__"] = create_repr(cls.__name__, fields_info)
    class_dict["__eq__"] = create_eq(fields_info)
    if freeze:
        class_dict["__setattr__"] = create_frozen_setattr()

    for key, value in cls.__dict__.items():
        if key.startswith("__") and key not in ("__init__", "__slots__"):
            continue
        if key in slot_names:
            continue
        class_dict[key] = value

    new_class = type(cls.__name__, cls.__bases__, class_dict)
    new_class.__foundation__ = cls
    
    check_metadata(cls, new_class)
    conserve_methods(cls, new_class)

    return new_class
