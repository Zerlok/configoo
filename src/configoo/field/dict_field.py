from typing import Type, TypeVar, Dict, Callable, Tuple

from .base import Field, PT, RT, FieldDefinition
from .exception import FieldValueError

__all__ = [
    'DictField',
]


T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class DictField(Field[str, T]):
    __SEPARATOR = (':', ',')

    def __init__(
            self,
            key_dtype: Field[str, K],
            value_dtype: Field[str, V],
            name: str = None,
            required: bool = False,
            default: Dict[K, V] = None,
            description: str = None,
            separator: Tuple[str, str] = None,
            not_empty: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=Dict[K, V],
        )

        self.__key_dtype = key_dtype
        self.__value_dtype = value_dtype
        self.__separator = separator or self.__SEPARATOR
        self.__not_empty = not_empty
    
    @property
    def key_dtype(self) -> Field[str, K]:
        return self.__key_dtype
    
    @key_dtype.setter
    def key_dtype(self, value: Field[str, K]) -> None:
        self.__key_dtype = value
    
    @property
    def value_dtype(self) -> Field[str, K]:
        return self.__value_dtype
    
    @value_dtype.setter
    def value_dtype(self, value: Field[str, K]) -> None:
        self.__value_dtype = value

    def parse(self, value: str) -> Dict[K, V]:
        key_value_separator, pair_separator = self.__separator

        try:
            pairs = value.split(pair_separator) if len(value) else []
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid Dict value!",
                value,
            )
        
        clean_dict = {}

        for i, pair in enumerate(pairs):
            try:
                key, value = pair.split(key_value_separator, 1)
                
                clean_key = self.key_dtype.parse(key)
                clean_value = self.value_dtype.parse(value)

                clean_dict[clean_key] = clean_value
            
            except ValueError as err:
                raise FieldValueError(
                    "Invalid dict pair format!",
                    i,
                    pair,
                    self.__separator,
                )
    
            except FieldValueError as err:
                raise FieldValueError(
                    "Invalid dict pair value!",
                    i,
                    key,
                    value,
                ) from err

        if self.__not_empty and not clean_dict:
            raise FieldValueError(
                "Dict is empty!",
                value,
                self.__separator,
            )
        
        return clean_dict

    def define(
            self,
            model: 'Model',
    ) -> 'DictDefinition[PT, RT]':
        return DictDefinition.create_from_model_field(model, self)


class DictDefinition(FieldDefinition[PT, RT]):
    @classmethod
    def create_from_model_field(
            cls,
            model: 'Model',
            field: DictField[RT],
    ) -> 'DictDefinition[PT, RT]':
        return cls(
            model=model,
            key_dtype=field.key_dtype,
            value_dtype=field.value_dtype,
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
            key_dtype: Field[PT, K],
            value_dtype: Field[PT, V],
            name: str,
            required: bool,
            default: Dict[K, V],
            description: str,
            parse_type: Type[PT],
            return_type: Type[RT],
            parser: Callable[[PT], Dict[K, V]],
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

        self.__key_dtype = key_dtype
        self.__value_dtype = value_dtype
    
    @property
    def key_dtype(self) -> Field[str, K]:
        return self.__key_dtype
    
    @property
    def value_dtype(self) -> Field[str, K]:
        return self.__value_dtype

    @property
    def default(self) -> Dict[K, V]:
        return super().default.copy()
