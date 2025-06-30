#-------------------- Imports --------------------

from typing import Type, List, Optional, Callable
from src.Stash.Classes import FieldInfo
import warnings
import types
import sys

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

def get_values_from_anno(cls: Type) -> List[FieldInfo]:
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

#-------------------- Dynamic Method Creators --------------------

def create_init(fields_info: List[FieldInfo], freeze: bool) -> Callable:
    def __init__(self, *args, **kwargs):
        for i, field in enumerate(fields_info):
            if field.value_name in kwargs:
                value = kwargs[field.value_name]
            elif i < len(args):
                value = args[i]
            elif field.has_default:
                value = field.default_value
            else:
                raise TypeError(f"Missing required argument: {field.value_name}")

            if field.type_annotation is str and isinstance(value, str):
                value = sys.intern(value)
            setattr(self, field.value_name, value)
        if freeze:
            object.__setattr__(self, "_frozen", True)
    return __init__

def create_repr(class_name: str, field_info: List[FieldInfo]) -> Callable:
    def __repr__(self):
        values = ", ".join(f"{f.value_name}={repr(getattr(self, f.value_name))}" for f in field_info)
        return f"{class_name}({values})"
    return __repr__

def create_eq(field_info: List[FieldInfo]) -> Callable:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return all(getattr(self, f.value_name) == getattr(other, f.value_name) for f in field_info)
    return __eq__

def create_frozen_setattr() -> Callable:
    def __setattr__(self, key, value):
        if getattr(self, "_frozen", False):
            raise AttributeError("Cannot modify frozen variables")
        object.__setattr__(self, key, value)
    return __setattr__
        