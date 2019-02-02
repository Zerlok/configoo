from typing import Type, TypeVar, List, Callable

from .base import Field, PT, RT, FieldDefinition
from ..exception import FieldValueError

__all__ = [
    'ListField',
]


T = TypeVar('T')


class ListField(Field[str, T]):
    __SEPARATOR = ','

    def __init__(
            self,
            dtype: Field[str, T],
            name: str = None,
            required: bool = False,
            default: List[T] = None,
            description: str = None,
            separator: str = None,
            not_empty: bool = False,
            skip_empty_parts: bool = None,
            length: int = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=List[T],
        )

        self.__dtype = dtype
        self.__separator = separator or self.__SEPARATOR
        self.__not_empty = not_empty
        self.__skip_empty_parts = skip_empty_parts
        self.__length = length
    
    @property
    def dtype(self) -> Field[str, T]:
        return self.__dtype
    
    @dtype.setter
    def dtype(self, value: Field[str, T]) -> None:
        self.__dtype = value
    
    def parse(self, value: str) -> List[T]:
        try:
            if not isinstance(value, list):
                parts = value.split(self.__separator) if len(value) else []
            else:
                parts = value
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid list value!",
                value,
            )
        
        clean_list = []

        for i, part in enumerate(parts):
            try:
                clean_part = self.__dtype.parse(part)
    
            except FieldValueError as err:
                raise FieldValueError(
                    "Invalid list item value!",
                    i,
                    part,
                ) from err

            if not self.__skip_empty_parts or clean_part:
                clean_list.append(clean_part)

        if self.__not_empty and not clean_list:
            raise FieldValueError(
                "List is empty!",
                value,
                self.__separator,
            )
        
        if self.__length is not None and len(clean_list) != self.__length:
            raise FieldValueError(
                "List length is invalid!",
                len(clean_list),
                self.__length,
            )
        
        return clean_list

    def define(
            self,
            model: 'Model',
    ) -> 'FieldDefinition[PT, RT]':
        return ListDefinition.create_from_model_field(model, self)


class ListDefinition(FieldDefinition[PT, RT]):
    @classmethod
    def create_from_model_field(
            cls,
            model: 'Model',
            field: ListField[RT],
    ) -> 'ListDefinition[PT, RT]':
        return cls(
            model=model,
            dtype=field.dtype,
            name=field.name,
            required=field.required,
            default=field.default,
            description=field.description,
            parse_type=field.parse_type,
            return_type=field.return_type,
            parser=field.parse,
        )
    
    def __init__(
            self,
            *,
            model: 'Model',
            dtype: Field[PT, RT],
            name: str,
            required: bool,
            default: List[RT],
            description: str,
            parse_type: Type[PT],
            return_type: Type[RT],
            parser: Callable[[PT], List[RT]],
    ) -> None:
        super().__init__(
            model=model,
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=parse_type,
            return_type=return_type,
            parser=parser,
        )

        self.__dtype = dtype
    
    @property
    def default(self) -> List[RT]:
        return super().default.copy()
