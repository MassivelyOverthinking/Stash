#-------------------- Imports --------------------

from typing import Type, List, Optional
from src.Stash.Classes import FieldInfo
import inspect
import warnings
import types

#-------------------- Utility Functions --------------------
    
def analyze_fields(cls: Type, allow_fallback: bool) -> List[FieldInfo]:
    if hasattr(cls, "__annotations__",) and cls.__annotations__:
        return get_values_from_anno(cls)
    
    elif allow_fallback and callable(getattr(cls, "__init__", None)):
        return get_values_from_init(cls)
            
    else:
        raise ValueError(f"Class {cls.__name__} must include type annotations to produce fields")


def check_metadata(source_cls: Type, target_cls: Type):
    for attr in ("__doc__", "__module__", "__annotations__", "__qualname__"):
        if hasattr(source_cls, attr):
            value = getattr(source_cls, attr, None)
            if value is not None:
                setattr(target_cls, attr, value)


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

def get_values_from_anno(cls: Type) -> list[FieldInfo]:
    results = []
    for param_name, param_value in cls.__annotations__.items():
        if param_name in cls.__dict__:
            has_default = True
            default_value = cls.__dict__[param_name]
        else:
            has_default = False
            default_value = None
        results.append(FieldInfo(
            value_name=param_name,
            type_annotation=param_value,
            has_default=has_default,
            default_value=default_value
        ))
    
    return results

def get_values_from_init(cls: Type) -> list[FieldInfo]:
    results = []
    sig = inspect.signature(cls.__init__)
    params = list(sig.parameters.values())[1:]
    for param in params:
        results.append(FieldInfo(
            value_name=param.name,
            type_annotation=param.annotation,
            has_default=param.default is not inspect.Signature.empty,
            default_value=param.default if param.default is not inspect.Signature.empty else None
        ))

    if not results:
        raise ValueError(f"Class {cls.__name__} has no __init__ parameters to infer fields from.")
    
    return results
        