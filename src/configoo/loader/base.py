from abc import ABCMeta, abstractmethod
from typing import TypeVar, Type, Generic, Optional, Iterable, Tuple, ClassVar, Any, Dict

from ..field import FieldDefinition, PT, RT, FieldValueError
from ..model import Model

from .exception import LoaderError

__all__ = [
    'LoaderContext',
    'LoaderDriver',
    'Loader',
    'BaseLoaderContext',
    'BaseLoaderDriver',
    'BaseLoader',
]

M = TypeVar('M', bound=Model)
RT = TypeVar('RT')


class LoaderContext(Generic[PT, M]):
    def __init__(
            self,
            driver: 'LoaderDriver[PT]',
            model: Type[M],
            field: FieldDefinition[PT, RT] = None,
    ) -> None:
        self.__driver = driver
        self.__model = model
        self.__field = field
    
    def __enter__(self) -> 'LoaderContext[PT, M]':
        return self
    
    def __exit__(self, *err) -> None:
        pass
    
    @property
    def driver(self) -> 'LoaderDirver[PT]':
        return self.__driver
    
    @property
    def model(self) -> Type[M]:
        return self.__model
    
    @property
    def field(self) -> Optional[FieldDefinition[PT, RT]]:
        return self.__field
    
    @field.setter
    def field(self, value: FieldDefinition[PT, RT]) -> None:
        self.__field = value


class LoaderDriver(Generic[PT]):
    def create_context(self, model: Type[M]) -> LoaderContext[PT, M]:
        raise NotImplementedError

    def start_loading(self, context: LoaderContext[PT, M]) -> None:
        raise NotImplementedError
    
    def check_field_parsing_type(self, context: LoaderContext[PT, M]) -> bool:
        raise NotImplementedError
    
    def check_field_required_value(self, context: LoaderContext[PT, M]) -> bool:
        raise NotImplementedError
    
    def get_field_value(self, context: LoaderContext[PT, M]) -> PT:
        raise NotImplementedError
    
    def parse_field_value(self, context: LoaderContext[PT, M]) -> RT:
        raise NotImplementedError
    
    def raise_invalid_field_parsing_type(self, context: LoaderContext[PT, M]) -> None:
        raise NotImplementedError
    
    def raise_required_field_value_error(self, context: LoaderContext[PT, M]) -> None:
        raise NotImplementedError
    
    def handle_loader_error(self, context: LoaderContext[PT, M], *err) -> None:
        raise NotImplementedError
    
    def finalize_loading(self, context: LoaderContext[PT, M]) -> None:
        raise NotImplementedError


class Loader(Generic[PT]):
    def load(
            self,
            context: LoaderContext[PT, M],
    ) -> Dict[str, Any]:
        raise NotImplementedError


class BaseLoaderContext(LoaderContext[PT, M]):
    def __init__(
            self,
            driver: 'LoaderDriver[PT]',
            model: Type[M],
            field: FieldDefinition[PT, RT] = None,
    ) -> None:
        super().__init__(
            driver=driver,
            model=model,
            field=field,
        )

        self.__value = None
        self.__clean_value = None
    
    def __enter__(self) -> 'LoaderContext[PT, M]':
        self.driver.start_loading(self)
        return self
    
    def __exit__(self, exc_type: Optional[Type[Exception]], exc_value: Optional[Exception], exc_stack: Any) -> None:
        if exc_type or exc_value or exc_stack:
            return self.driver.handle_loader_error(self, exc_type, exc_value, exc_stack)
        
        self.driver.finalize_loading(self)
    
    @property
    def value(self) -> PT:
        return self.__value
    
    @value.setter
    def value(self, value: PT) -> None:
        self.__value = value

    @property
    def clean_value(self) -> RT:
        return self.__clean_value
    
    @clean_value.setter
    def clean_value(self, value: RT) -> None:
        self.__clean_value = value


class BaseLoaderDriver(LoaderDriver[PT]):
    _NONE: ClassVar[Any] = object()
    _PARSING_TYPE: ClassVar[Any] = None     # PT
    
    _LOADER_ERROR: ClassVar[Type[LoaderError]] = None
    _INVALID_FIELD_PARSING_TYPE_ERROR: ClassVar[Type[LoaderError]] = None
    _REQUIRED_FIELD_VALUE_ERROR: ClassVar[Type[LoaderError]] = None
    _FIELD_VALUE_ERROR: ClassVar[Type[LoaderError]] = None

    def __init_subclass__(cls) -> None:
        assert cls._PARSING_TYPE, "Invalid loader driver!"

        cls._LOADER_ERROR = cls._LOADER_ERROR or LoaderError
        cls._INVALID_FIELD_PARSING_TYPE_ERROR = cls._INVALID_FIELD_PARSING_TYPE_ERROR or cls._LOADER_ERROR
        cls._REQUIRED_FIELD_VALUE_ERROR = cls._REQUIRED_FIELD_VALUE_ERROR or cls._LOADER_ERROR
        cls._FIELD_VALUE_ERROR = cls._FIELD_VALUE_ERROR or cls._LOADER_ERROR
    
    def create_context(self, model: Type[M]) -> BaseLoaderContext[PT, M]:
        return BaseLoaderContext(
            driver=self,
            model=model,
            field=None,
        )

    def start_loading(self, context: BaseLoaderContext[PT, M]) -> None:
        pass
    
    def check_field_parsing_type(self, context: BaseLoaderContext[PT, M]) -> bool:
        return context.field.parse_type is self._PARSING_TYPE
    
    def check_field_required_value(self, context: BaseLoaderContext[PT, M]) -> bool:
        return not context.field.required or context.value is not self._NONE
    
    def get_field_value(self, context: BaseLoaderContext[PT, M]) -> PT:
        raise NotImplementedError
    
    def parse_field_value(self, context: BaseLoaderContext[PT, M]) -> RT:
        if context.value is self._NONE:
            return context.field.default

        clean_value = context.field.parser(context.value)

        return clean_value
    
    def raise_invalid_field_parsing_type(self, context: BaseLoaderContext[PT, M]) -> None:
        raise self._INVALID_FIELD_PARSING_TYPE_ERROR(
            f"Field '{context.field}' parser can not be used with {self._PARSING_TYPE} type!",
            context.field,
        )
    
    def raise_required_field_value_error(self, context: BaseLoaderContext[PT, M]) -> None:
        raise self._REQUIRED_FIELD_VALUE_ERROR(
            f"Field '{context.field}' value is required!",
            context.field,
        )
    
    def handle_loader_error(
            self,
            context: BaseLoaderContext[PT, M],
            exc_type: Optional[Type[Exception]],
            exc_value: Optional[Exception],
            exc_stack: Any,
    ) -> bool:
        if isinstance(exc_value, FieldValueError):
            message, value = exc_value.args
            raise self._FIELD_VALUE_ERROR(
                f"Field '{context.field}' has invalid value!",
                context.field,
                value,
            ) from exc_value
        
        elif isinstance(exc_value, self._LOADER_ERROR):
            return False
    
    def finalize_loading(self, context: BaseLoaderContext[PT, M]) -> None:
        pass


class BaseLoader(Loader[PT]):
    _DRIVER: ClassVar[Optional[LoaderDriver[PT]]] = None

    def __init__(
            self,
            driver: LoaderDriver[PT] = None,
    ) -> None:
        self._driver = driver or self._DRIVER

        if not self._driver:
            raise LoaderError("A driver object is required!")
    
    @property
    def driver(self) -> LoaderDriver[PT]:
        return self._driver

    def load(
            self,
            context: BaseLoaderContext[PT, M],
    ) -> Dict[str, Any]:
        with context:
            data = {
                key: self.load_field(context)
                for key, field in self._iter_model_fields(context)
            }
        
        return data
    
    def load_field(self, context: BaseLoaderContext[PT, M]) -> RT:
        if not self.driver.check_field_parsing_type(context):
            self.driver.raise_invalid_field_parsing_type(context)

        context.value = self.driver.get_field_value(context)
        
        if not self.driver.check_field_required_value(context):
            self.driver.raise_required_field_value_error(context)
        
        context.clean_value = self.driver.parse_field_value(context)

        return context.clean_value
    
    def _iter_model_fields(self, context: BaseLoaderContext[PT, M]) -> Iterable[Tuple[str, FieldDefinition[PT, RT]]]:
        for key, field in context.model.iter_fields():
            context.field = field
            yield key, field
