from typing import Type, TypeVar, List, Callable

from .base import Field, PT, RT, FieldDefinition
from .exception import ParseError

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
            separator: str = None,
            not_empty: bool = False,
            skip_empty_parts: bool = None,
            length: int = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
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
        return self.__dtype
    
    def parse(self, value: str) -> List[T]:
        try:
            parts = value.split(self.__separator)
        
        except (TypeError, ValueError) as err:
            raise ParseError(
                "Invalid list value!",
                value,
            )
        
        cleanList = []

        for i, part in enumerate(parts):
            if not self.__skip_empty_parts or part:
                try:
                    clean_part = self.__dtype.parse(part)
        
                except ParseError as err:
                    raise ParseError(
                        "Invalid list item value!",
                        i,
                        part,
                    ) from err
                
                else:
                    cleanList.append(clean_part)

        if self.__not_empty and not cleanList:
            raise ParseError(
                "List is empty!",
                value,
                self.__separator,
            )
        
        if self.__length is not None and len(cleanList) != self.__length:
            raise ParseError(
                "List length is invalid!",
                len(cleanList),
                self.__length,
            )
        
        return cleanList

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
            parse_type: Type[PT],
            return_type: Type[RT],
            parser: Callable[[PT], List[RT]],
    ) -> None:
        super().__init__(
            model=model,
            name=name,
            required=required,
            default=default,
            parse_type=parse_type,
            return_type=return_type,
            parser=parser,
        )

        self.__dtype = dtype
    
    @property
    def default(self) -> List[RT]:
        return super().default.copy()
