from typing import Type, TypeVar, Union
import enum

from .base import Field, PT, RT
from .exception import FieldValueError

__all__ = [
    'EnumField',
]


T = TypeVar('T')


class EnumField(Field[str, T]):
    def __init__(
            self,
            dtype: Union[Type[T], Type[enum.Enum]],
            name: str = None,
            required: bool = False,
            default: Union[T, enum.Enum] = None,
            description: str = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            parse_type=str,
            return_type=str,
            description=description,
        )

        self.__dtype = dtype

    @property
    def dtype(self) -> Union[Type[T], enum.Enum]:
        return self.__dtype
    
    @dtype.setter
    def dtype(self, value: Union[Type[T], enum.Enum]) -> None:
        self.__dtype = value
    
    def parse(self, value: str) -> str:
        try:
            clean_value = self.dtype(value)
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid enum value!",
                value,
                self.dtype,
            ) from err

        return clean_value
