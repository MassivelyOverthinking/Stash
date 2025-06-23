#-------------------- Imports --------------------

from typing import Type, List, Optional
from src.Stash.Utils import check_metadata, preserve_methods, analyze_fields

#-------------------- Slots Class (Mutable) --------------------

def create_slots_cls(cls: Type, allow_fallback: bool, preserve: Optional[List[str]]) -> Type:
    fields_info = analyze_fields(cls, allow_fallback)
    slot_names = [field.value_name for field in fields_info]

    class_dict = {}

    class_dict["__slots__"] = tuple(slot_names)

    for key, value in cls.__dict__.items():
        if key.startswith("__") and key not in ("__init__", "__slots__"):
            continue
        if key in slot_names:
            continue
        class_dict[key] = value

    for field in fields_info:
        if field.has_default:
            class_dict[field.value_name] = field.default_value

    new_class = type(cls.__name__, cls.__bases__, class_dict)
    
    check_metadata(cls, new_class)
    preserve_methods(cls, new_class, preserve)

    return new_class