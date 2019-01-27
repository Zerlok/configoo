from typing import Type

from .base import Field, PT, RT
from .exception import ParseError

__all__ = [
    'String',
]


class String(Field[str, str]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: int = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            parse_type=str,
            return_type=int,
        )
    
    def parse(self, value: str) -> str:
        try:
            clean_value = str(value)
        
        except (TypeError, ValueError) as err:
            raise ParseError(
                "Invalid string value!",
                value,
            )

        return clean_value
