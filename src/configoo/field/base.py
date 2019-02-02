from typing import Optional, Any, TypeVar, Type, Generic, Callable

__all__ = [
    'Field',
    'FieldDefinition',
    'PT',
    'RT',
]


T = TypeVar('T')
PT = TypeVar('PT')
RT = TypeVar('RT')


class Field(Generic[PT, RT]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Any = None,
            description: str = None,
            parse_type: Type[PT] = None,
            return_type: Type[RT] = None,
    ) -> None:
        self.__name = name
        self.__required = required
        self.__default = default
        self.__description = description
        self.__parse_type = parse_type
        self.__return_type = return_type
    
    @property
    def name(self) -> Optional[str]:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        self.__name = value
    
    @property
    def required(self) -> bool:
        return self.__required
    
    @required.setter
    def required(self, value: bool) -> None:
        self.__required = value
    
    @property
    def default(self) -> Any:
        return self.__default
    
    @default.setter
    def default(self, value: Any) -> None:
        self.__default = value
    
    @property
    def description(self) -> Optional[str]:
        return self.__description
    
    @description.setter
    def description(self, value: Optional[str]) -> None:
        self.__description = value
    
    @property
    def parse_type(self) -> Type[PT]:
        return self.__parse_type
    
    @parse_type.setter
    def parse_type(self, value: Type[PT]) -> None:
        self.__parse_type = value
    
    @property
    def return_type(self) -> Type[RT]:
        return self.__return_type
    
    @return_type.setter
    def return_type(self, value: Type[RT]) -> None:
        self.__return_type = value
    
    def parse(self, value: PT) -> RT:
        raise NotImplementedError
    
    def define(
            self,
            model: 'Model',
    ) -> 'FieldDefinition[PT, RT]':
        return FieldDefinition.create_from_model_field(model, self)

    def _not_none_or_default(
            self,
            key: str,
            value: Optional[T],
            default: T,
    ) -> T:
        return value if value is not None else default


class FieldDefinition(Generic[PT, RT]):
    @classmethod
    def create_from_model_field(
            cls,
            model: 'Model',
            field: Field[PT, RT],
    ) -> 'FieldDefinition[PT, RT]':
        return cls(
            model=model,
            name=field.name,
            required=field.required,
            default=field.default,
            description=field.description,
            parse_type=field.parse_type,
            return_type=field.return_type,
            parser=field.parse,
        )

    def __init__(
            self,
            *,
            model: 'Model',
            name: str,
            required: bool,
            default: Any,
            description: Optional[str],
            parse_type: Type[PT],
            return_type: Type[RT],
            parser: Callable[[PT], RT],
    ) -> None:
        if required and default is not None:
            raise ValueError(
                "Field must be either required or has a default value!",
            )

        self.__model = model
        self.__name = name
        self.__required = required
        self.__default = default
        self.__description = description
        
        self.__parse_type = parse_type
        self.__return_type = return_type
        self.__parser = parser
    
    def __str__(self) -> str:
        return f"{self.model.__name__}.{self.name}"
    
    __repr__ = __str__
    
    @property
    def model(self) -> 'Model':
        return self.__model
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def required(self) -> bool:
        return self.__required
    
    @property
    def default(self) -> Any:
        return self.__default
    
    @property
    def description(self) -> Optional[str]:
        return self.__description
    
    @property
    def parse_type(self) -> Type[PT]:
        return self.__parse_type
    
    @property
    def return_type(self) -> Type[RT]:
        return self.__return_type
    
    @property
    def parser(self) -> Callable[[PT], RT]:
        return self.__parser
