from typing import TypeVar, Type, Iterable, Tuple, Any, ClassVar, Dict

from ..field import Field, FieldDefinition

__all__ = [
    'Model',
]


class Model:
    __annotations__: Dict[str, Type] = {}
    
    __FIELDS: ClassVar[Dict[str, FieldDefinition]]

    __data: Dict[str, Any]

    def __init_subclass__(cls, *args, **kwargs) -> None:
        cls.__FIELDS = {}

        for key, value in cls._iter_attributes(cls):
            if not key.startswith('_') and isinstance(value, Field):
                field = cls._create_field_definition(key, value)
                cls._append_field(key, field)
    
    @classmethod
    def _iter_attributes(cls, model: Type['Model']) -> Iterable[Tuple[str, Any]]:
        return (
            (
                key,
                getattr(model, key)
            )
            for key in dir(model)
        )
 
    @classmethod
    def _create_field_definition(cls, name: str, field: Field) -> FieldDefinition:
        field.name = field.name or name
        return field.define(
            model=cls,
        )

    @classmethod
    def _append_field(cls, key: str, field: FieldDefinition) -> None:
        cls.__FIELDS[key] = field

        def field_value_getter(self) -> field.return_type:
            return self.__data[key]
        
        field_property = property(
            fget=field_value_getter,
            doc=field.description,
        )
        
        setattr(cls, key, field_property)
        cls.__annotations__[key] = field.return_type
    
    @classmethod
    def iter_fields(cls) -> Iterable[Tuple[str, FieldDefinition]]:
        return (
            (
                key,
                field,
            )
            for key, field in cls.__FIELDS.items()
        )
    
    def __init__(
            self,
            data: Dict[str, Any],
    ) -> None:
        self.__data = data
    
    def __str__(self) -> str:
        values = ', '.join(
            f"{key}={value}"
            for key, value in self
        )

        return f"{self.__class__.__name__}(" \
                f"{values}" \
                ")"
    
    __repr__ = __str__

    def __iter__(self) -> Iterable[Tuple[str, Any]]:
        return (
            (
                key,
                value,
            )
            for key, value in self.__data.items()
        )
