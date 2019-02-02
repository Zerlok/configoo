from typing import Type, List
import logging

from .base import Field, PT, RT
from .exception import FieldValueError

from .string import String
from .list import ListField

__all__ = [
    'LoggingLevel',
    'LoggingRecordFormat',
    'LoggingBracketRecordFormat',
]


class LoggingLevel(Field[str, str]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: str = None,
            description: str = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=str,
        )
    
    def parse(self, value: str) -> str:
        clean_value = logging._nameToLevel.get(str(value).upper())

        if clean_value is None:
            raise FieldValueError(
                "Invalid logging level value!",
                value,
            )

        return clean_value


class LoggingRecordFormat(Field[str, str]):
    __ALLOWED_RECORD_FIELDS = {
        'name': 'name',
        'levelno': 'levelno',
        'levelname': 'levelname',
        'level': 'levelname',
        'pathname': 'pathname',
        'path': 'pathname',
        'filename': 'filename',
        'file': 'filename',
        'module': 'module',
        'lineno': 'lineno',
        'funcName': 'funcName',
        'func': 'funcName',
        'created': 'created',
        'at': 'created',
        'asctime': 'asctime',
        'msecs': 'msecs',
        'relativeCreated': 'relativeCreated',
        'thread': 'thread',
        'threadName': 'threadName',
        'process': 'process',
        'message': 'message',
    }

    __DEFAULT_RECORD_FIELDS = (
        'at',
        'level',
        'name',
        'message',
    )

    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: List[str] = None,
            description: str = None,
            parse_field_separator: str = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=str,
        )

        self.__dtype = ListField(
            dtype=String(
                required=True,
                default=None,
                modifyer=String.Modifyer.NONE,
            ),
            required=False,
            default=self.default or self.__DEFAULT_RECORD_FIELDS,
            separator=parse_field_separator,
            not_empty=True,
            skip_empty_parts=True,
            length=None,
        )

    @property
    def dtype(self) -> ListField[str]:
        return self.__dtype
    
    @dtype.setter
    def dtype(self, value: ListField[str]) -> None:
        self.__dtype = value
    
    def parse(self, value: str) -> str:
        names = self.dtype.parse(value) if value else self.dtype.default
        formatted_fields = []

        for name in names:
            field_name = self.__ALLOWED_RECORD_FIELDS.get(name)
            if not field_name:
                raise FieldValueError(
                    "Invalid log record field name!",
                    field_name,
                )
            
            field_format = self.apply_field_format(field_name)
            formatted_fields.append(field_format)

        clean_value = self.join_field_formats(formatted_fields)
        return clean_value
    
    def apply_field_format(self, name: str) -> str:
        return f"%({name})s"
    
    def join_field_formats(self, fields: List[str]) -> str:
        return ' '.join(fields)


class LoggingBracketRecordFormat(LoggingRecordFormat):
    def apply_field_format(self, name: str) -> str:
        if name == 'message':
            return f"%({name})s"
        
        return f"[%({name})s]"
    
    def join_field_formats(self, fields: List[str]) -> str:
        return ' '.join(fields)
