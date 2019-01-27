from typing import Type, Any
from os import getenv

from ..field import FieldDefinition, PT, RT, ParseError

from .base import Loader
from .exception import LoaderError

__all__ = [
    'EnvLoader',
    'EnvLoaderError',
    'EnvVariableError',
    'EnvVariableMissedError',
    'EnvVariableValueError',
]


class EnvLoaderError(LoaderError):
    pass


class EnvVariableError(EnvLoaderError):
    pass


class EnvVariableMissedError(EnvVariableError):
    pass


class EnvVariableValueError(EnvVariableMissedError):
    pass


class EnvLoader(Loader):
    __NONE = object()
    __PARSING_TYPE = str
    
    def load_field(self, field: FieldDefinition[str, RT]) -> RT:
        value = self.get_field_value(field)
        if not self.check_field_required_value(value, field):
            return None
        
        return self.parse_field_value(value, field)
    
    def get_field_value(self, field: FieldDefinition[str, RT]) -> Any:
        return getenv(field.name, default=self.__NONE)
    
    def check_field_required_value(self, value: Any, field: FieldDefinition[str, RT]) -> bool:
        if field.required and value is self.__NONE:
            raise EnvVariableMissedError(
                f"Variable '{field.name}' is required!",
                field,
            )

        return True
    
    def parse_field_value(self, value: Any, field: FieldDefinition) -> Any:
        if value is self.__NONE:
            return field.default
        
        if field.parse_type is not self.__PARSING_TYPE:
            raise EnvLoaderError(
                f"Field parser can not parse {self.__PARSING_TYPE} value type!",
                field,
            )

        try:
            clean_value = field.parser(value)
        
        except ParseError as err:
            raise EnvVariableValueError(
                f"Variable value is invalid: {' '.join(str(a) for a in err.args)}",
            ) from err
        
        else:
            return clean_value
