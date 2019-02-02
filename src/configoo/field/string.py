from typing import Type, Optional
import enum

from .base import Field, PT, RT
from .exception import FieldValueError

__all__ = [
    'String',
]


class String(Field[str, str]):
    class Modifyer(enum.Enum):
        NONE = 'none'
        UPPER = 'upper'
        LOWER = 'lower'
        TITLE = 'title'

        def apply(self, value: str) -> str:
            if self is self.NONE:
                return value
            if self is self.UPPER:
                return value.upper()
            elif self is self.LOWER:
                return value.lower()
            elif self is self.TITLE:
                return value.title()
            
            return value

    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: int = None,
            description: str = None,
            modifyer: Modifyer = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=str,
        )

        self.__modifyer = modifyer
    
    @property
    def modifyer(self) -> Optional['Modifyer']:
        return self.__modifyer

    @modifyer.setter
    def modifyer(self, value: Optional[Modifyer]) -> None:
        self.__modifyer = value
    
    def parse(self, value: str) -> str:
        try:
            clean_value = str(value)
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid string value!",
                value,
            )
        
        modifyer = self.modifyer or self.Modifyer.NONE
        return modifyer.apply(clean_value)
