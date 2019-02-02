from typing import Type, Any, Union, Optional, Dict

import json
from pathlib import Path

from ..field import FieldDefinition, FieldValueError

from .base import BaseLoader, BaseLoaderDriver, BaseLoaderContext, PT, RT, M
from .exception import LoaderError

__all__ = [
    'JsonLoader',
    'JsonLoaderError',
    'JsonVariableError',
    'JsonRequiredVariableError',
    'JsonVariableValueError',
]


class JsonLoaderError(LoaderError):
    pass


class JsonVariableError(JsonLoaderError):
    pass


class JsonRequiredVariableError(JsonVariableError):
    pass


class JsonVariableValueError(JsonVariableError):
    pass


class JsonLoaderContext(BaseLoaderContext[Any, M]):
    def __init__(
            self,
            driver: 'LoaderDriver[PT]',
            model: Type[M],
            field: FieldDefinition[PT, RT] = None,
            path: Path = None,
            data: Dict = None,
    ) -> None:
        super(
            driver=driver,
            model=model,
            field=field,
        )

        self.__path = path
        self.__data = data
    
    @property
    def path(self) -> Optional[Path]:
        return self.__path
    
    @path.setter
    def path(self, value: Path) -> None:
        self.__path = value


class JsonLoaderDriver(BaseLoaderDriver[Any]):
    _PARSING_TYPE = Any

    _LOADER_ERROR = JsonLoaderError
    _REQUIRED_FIELD_VALUE_ERROR = JsonRequiredVariableError
    _FIELD_VALUE_ERROR = JsonVariableValueError

    def create_context(
            self,
            model: Type[M],
            path: Path = None,
    ) -> JsonLoaderContext[M]:
        return JsonLoaderContext(
            driver=self,
            model=model,
            path=path,
        )
    
    def start_loading(self, context: JsonLoaderContext[M]) -> None:
        with context.path.open('r') as fd:
            context.data = json.load(fd)

    def get_field_value(self, context: JsonLoaderContext[M]) -> Union[int, str]:
        return context.data.get(context.field.name, default=self._NONE)


class JsonLoader(BaseLoader[Any]):
    _DRIVER = JsonLoaderDriver()

    def __init__(
            self,
            driver: JsonLoaderDriver = None,
    ) -> None:
        super().__init__(
            driver=driver,
        )

    @property
    def driver(self) -> JsonLoaderDriver:
        return self._driver
    
    def load_model(
            self,
            model: Type[M],
            path: Path,
    ) -> M:
        context = self.driver.create_context(model, path)
        
        data = self.load(context)

        config = model(**data)

        return config
