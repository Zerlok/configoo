from typing import Type, Any, Union
from os import getenv

from ..exception import LoaderError, FieldValueError
from ..field import FieldDefinition

from .base import BaseLoader, BaseLoaderDriver, BaseLoaderContext, PT, RT, M

__all__ = [
    'EnvLoaderDriver',
    'EnvLoader',
]


class EnvLoaderDriver(BaseLoaderDriver[str]):
    _PARSING_TYPE = str

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

        config = model(data)

        return config
