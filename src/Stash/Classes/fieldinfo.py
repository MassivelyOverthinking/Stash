#-------------------- Imports --------------------

from dataclasses import dataclass
from typing import Optional

#-------------------- FieldInfos Class --------------------

@dataclass
class FieldInfo():
    value_name: str
    type_annotation: any
    has_default: bool
    default_value: Optional[any]