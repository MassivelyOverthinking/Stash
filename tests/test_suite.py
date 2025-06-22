#-------------------- Imports --------------------

import types
import typing
import inspect
from typing import Optional
from dataclasses import dataclass

#-------------------- Testing Suite --------------------

@dataclass
class FieldInfo():
    name: str
    value: any
    has_default: bool
    default_value: Optional[any]

class TestField():
    name: str
    age: int
    grades: list[int]
    is_active: bool

    def __init__(self, name: str, age: int = None, grades: list[int] = [], is_active: bool = False):
        pass

def random_func(x: int, y: int = 10):
    return x * y

sig = inspect.signature(random_func)
sig2 = inspect.signature(TestField)
# print(sig)

# for param_name, param in sig.parameters.items():
#     print(f"Parameter name: {param_name}")
#     print(f"Paramter kind: {param.kind}")
#     print(f"Default Value: {param.default if param.default is not inspect.Parameter.empty else 'No Default'}")
#     print(f"Annotation: {param.annotation if param.annotation is not inspect.Parameter.empty else 'No Annotation'}")

def get_info(sig: inspect.Signature):
    results = []
    for param_name, param in sig.parameters.items():
        results.append(FieldInfo(
            name=param_name,
            value=param.annotation,
            has_default=param.default is not inspect.Parameter.empty,
            default_value=param.default if param.default is not inspect.Parameter.empty else None
        ))
    return results

def rebuild_class (name: str, fields: list[FieldInfo]):
    annotations = {}
    class_dict = {}

    for field in fields:
        annotations[field.name] = field.value
        if field.has_default:
            class_dict[field.name] = field.default_value

    class_dict["__annotations__"] = annotations

    return type(name, (object,), class_dict)


print("\n---------- Fields ----------")
results = get_info(sig2)
new_cls = rebuild_class("New_Class", results)
sig3 = inspect.signature(new_cls.__init__)

for param_name, param in sig3.parameters.items():
    print(f"Paramter name: {param_name}")
    print(f"Paramter kind: {param.kind}")
    print(f"Default Value: {param.default if param.default is not inspect.Parameter.empty else 'No Default'}")
    print(f"Annotation: {param.annotation if param.annotation is not inspect.Parameter.empty else 'No Annotation'}")