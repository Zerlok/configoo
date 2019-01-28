from typing import Type

from .base import Field, PT, RT
from .exception import ParseError

__all__ = [
    'Float',
]


class Float(Field[str, float]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: float = None,
            min_value: float = None,
            max_value: float = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            parse_type=str,
            return_type=float,
        )
        self.__min_value = min_value
        self.__max_value = max_value
    
    def parse(self, value: str) -> float:
        try:
            clean_value = float(value)
        
        except (TypeError, ValueError) as err:
            raise ParseError(
                "Invalid float value!",
                value,
            )

        if (
                self.__min_value is not None
                and clean_value < self.__min_value
        ):
            raise ParseError(
                "Float exceeds min value!",
                value,
                self.__min_value,
            )
        
        if (
                self.__max_value is not None
                and clean_value > self.__max_value
        ):
            raise ParseError(
                "Float exceeds max value!",
                value,
                self.__max_value,
            )
        
        return clean_value