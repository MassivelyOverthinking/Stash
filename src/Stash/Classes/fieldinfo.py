#-------------------- Imports --------------------

from dataclasses import dataclass
from typing import Optional, Any

#-------------------- FieldInfos Class --------------------

@dataclass
class FieldInfo():
    value_name: str
    type_annotation: Any
    has_default: bool
    default_value: Optional[Any]