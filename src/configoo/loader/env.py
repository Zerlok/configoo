from typing import Type, Any, Union
from os import getenv

from ..field import FieldDefinition, FieldValueError

from .base import BaseLoader, BaseLoaderDriver, BaseLoaderContext, PT, RT, M
from .exception import LoaderError

__all__ = [
    'EnvLoaderDriver',
    'EnvLoader',
    'EnvLoaderError',
    'EnvVariableError',
    'EnvRequiredVariableError',
    'EnvVariableValueError',
]


class EnvLoaderError(LoaderError):
    pass


class EnvVariableError(EnvLoaderError):
    pass


class EnvRequiredVariableError(EnvVariableError):
    pass


class EnvVariableValueError(EnvVariableError):
    pass


class EnvLoaderDriver(BaseLoaderDriver[str]):
    _PARSING_TYPE = str

    _LOADER_ERROR = EnvLoaderError
    _REQUIRED_FIELD_VALUE_ERROR = EnvRequiredVariableError
    _FIELD_VALUE_ERROR = EnvVariableValueError

    def get_field_value(self, context: BaseLoaderContext[str, M]) -> Union[int, str]:
        return getenv(context.field.name, default=self._NONE)


class EnvLoader(BaseLoader[str]):
    _DRIVER = EnvLoaderDriver()

    def __init__(
        self,
        driver: EnvLoaderDriver = None,
    ) -> None:
        super().__init__(
            driver=driver,
        )
    
    @property
    def driver(self) -> EnvLoaderDriver:
        return self._driver
    
    def load_model(
            self,
            model: Type[M],
    ) -> M:
        context = self.driver.create_context(model)
        
        data = self.load(context)

        config = model(**data)

        return config
