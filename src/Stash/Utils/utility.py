#-------------------- Imports --------------------

from typing import Type
import inspect

#-------------------- Utility Functions --------------------

def check_cls(cls: Type) -> list[str]:
    if hasattr(cls, "__annotations__"):
        fields = list(cls.__annotations__.keys())
    elif hasattr(cls, "__init__"):
        sig = inspect.signature(cls.__init__)
        fields = list([param.name for param in list(sig.parameters.values())[1:]])
    else:
        raise ValueError(f"Class {cls.__name__} does not contain '__annotations__' or '__init__' methods")
    
    return fields

def check_metadata(source_cls: Type, target_cls: Type):
    for attr in ("__doc__", "__module__", "__annotations__", "__qualname__"):
        if hasattr(source_cls, attr):
            setattr(target_cls, attr, getattr(source_cls, attr))
        