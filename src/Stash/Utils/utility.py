#-------------------- Imports --------------------

from typing import Type, List, Optional
from src.Stash.Classes import FieldInfo
import warnings
import types

#-------------------- Utility Functions --------------------

def check_metadata(source_cls: Type, target_cls: Type):
    for attr in ("__doc__", "__module__", "__annotations__", "__qualname__"):
        if hasattr(source_cls, attr):
            setattr(target_cls, attr, getattr(source_cls, attr))


def preserve_methods(source_cls: Type, target_cls: Type, preserve: Optional[List[str]]) -> None:
    if preserve is None:
        return

    for attr in preserve:
        if attr not in source_cls.__dict__:
            warnings.warn(
                f"Attribute {attr} not found in class: {source_cls.__name__}."
                f"Check for possible typos or unintended omissions",
                UserWarning
            )
            continue

        attr_value = source_cls.__dict__[attr]

        if isinstance(attr_value, (types.FunctionType, classmethod, staticmethod, property)):
            setattr(target_cls, attr, attr_value)
        else:
            warnings.warn(
                f"Attribute {attr} in class {source_cls.__name__} is not a method or descriptor."
                f"Only methods, staticmethods, classmethods, properties are preserved",
                UserWarning
            )

def get_annotations(cls: Type) -> List[FieldInfo]:
    results = []
    for param, anno in cls.__annotations__.items():
        default = cls.__dict__.get(param, None)
        results.append(FieldInfo(
            value_name=param,
            type_annotation=anno,
            has_default=param in cls.__dict__,
            default_value=default
        ))
        
    return results

        