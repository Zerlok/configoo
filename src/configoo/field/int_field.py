from typing import Type

from .base import Field, PT, RT
from .exception import FieldValueError

__all__ = [
    'IntField',
]


class IntField(Field[str, int]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: int = None,
            description: str = None,
            min_value: int = None,
            max_value: int = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=int,
        )
        
        self.__min_value = min_value
        self.__max_value = max_value
    
    def parse(self, value: str) -> int:
        try:
            clean_value = int(value)
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid integer value!",
                value,
            )
        
        self.check_min_value(clean_value)
        self.check_max_value(clean_value)

        return clean_value

    def check_min_value(self, value: int) -> bool:
        if (
                self.__min_value is not None
                and value < self.__min_value
        ):
            raise FieldValueError(
                "Integer exceeds min value!",
                value,
                self.__min_value,
            )
        
        return True
    
    def check_max_value(self, value: int) -> bool:        
        if (
                self.__max_value is not None
                and value > self.__max_value
        ):
            raise FieldValueError(
                "Integer exceeds max value!",
                value,
                self.__max_value,
            )
        
        return True
