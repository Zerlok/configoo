from typing import Type, Union

from .base import Field, PT, RT
from .exception import FieldValueError

__all__ = [
    'NumField',
]


Num = Union[int, float]


class NumField(Field[str, Num]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Num = None,
            description: str = None,
            min_value: Num = None,
            max_value: Num = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=Num,
        )
        
        self.__min_value = min_value
        self.__max_value = max_value
    
    def parse(self, value: str) -> Num:
        try:
            clean_value = float(value)
            if clean_value.is_integer():
                clean_value = int(clean_value)
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid number value!",
                value,
            )

        if (
                self.__min_value is not None
                and clean_value < self.__min_value
        ):
            raise FieldValueError(
                "Number exceeds min value!",
                value,
                self.__min_value,
            )
        
        if (
                self.__max_value is not None
                and clean_value > self.__max_value
        ):
            raise FieldValueError(
                "Number exceeds max value!",
                value,
                self.__max_value,
            )
        
        return clean_value
