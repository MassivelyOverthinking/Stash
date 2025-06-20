#-------------------- Imports --------------------

from typing import Type, List
import inspect

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
        