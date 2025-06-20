#-------------------- Imports --------------------

from typing import Type, List, Optional
import inspect
import warnings
import types

#-------------------- Utility Functions --------------------

def check_cls(cls: Type, allow_fallback: bool) -> List[str]:
    if hasattr(cls, "__annotations__") and cls.__annotations__:
        return list(cls.__annotations__.keys())
    
    elif allow_fallback and callable(getattr(cls, "__init__", None)):
        sig = inspect.signature(cls.__init__)
        params = list(sig.parameters.values())[1:]
        
        if not params:
            raise ValueError(f"Class {cls.__name__} has no __init__ parameters to infer fields from.")
        
        return [param.name for param in params]
    
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
        