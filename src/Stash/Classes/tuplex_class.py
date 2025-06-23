
#-------------------- Experimental Tuplex Class (Disabled) --------------------
# NOTE: This section is currently under development and therefore unused during runtime.

# def create_tuplex_cls(cls: Type, allow_fallback: bool, preserve: Optional[List[str]]) -> Type:
#     fields_info = analyze_fields(cls, allow_fallback)

#     annotations = {}
#     defaults = {}

#     for field in fields_info:
#         annotations[field.value_name] = field.type_annotation
#         if field.has_default:
#             defaults[field.value_name] = field.default_value

#     class_namespace = {
#         "__annotations__": annotations,
#         "__slots__": (),
#         **defaults,
#     }

#     NTBase = NamedTuple(cls.__name__, annotations.items())
#     new_class = type(cls.__name__, (NTBase,), class_namespace)

#     for name, attr in cls.__dict__.items():
#         if isinstance(attr, types.FunctionType) and not name.startswith("__"):
#             setattr(new_class, name, attr)

#     check_metadata(cls, new_class)
#     preserve_methods(cls, new_class, preserve)

#     return new_class