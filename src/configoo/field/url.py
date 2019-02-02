from typing import Type, Union

from ipaddress import ip_address, IPv4Address, IPv6Address
from urllib.parse import urlparse, ParseResult as Url

from .base import Field, PT, RT
from ..exception import FieldValueError

from .int_field import IntField

__all__ = [
    'UrlField',
    'RouteField',
    'IpField',
    'PortField',
]


IP = Union[IPv4Address, IPv6Address]


class UrlField(Field[str, Url]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Union[str, Url] = None,
            description: str = None,
    ) -> None:
        if isinstance(default, str):
            default = self.parse(default)

        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=Url,
        )
    
    def parse(self, value: str) -> Url:
        return urlparse(value)


class RouteField(Field[str, str]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Union[str, Url] = None,
            description: str = None,
    ) -> None:
        if isinstance(default, str):
            default = self.parse(default)

        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            parse_type=str,
            return_type=str,
        )

    def parse(self, value: str) -> str:
        return urlparse(value).path


class IpField(Field[str, IP]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Union[str, IP] = None,
            description: str = None,
    ) -> None:
        if isinstance(default, str):
            default = self.parse(default)
        
        super().__init__(
            name=name,
            required=required,
            default=default,
            parse_type=str,
            return_type=IP,
            description=description,
        )
    
    def parse(self, value: str) -> IP:
        try:
            clean_value = ip_address(value)
        
        except (TypeError, ValueError) as err:
            raise FieldValueError(
                "Invalid ip address!",
                value,
            )
        
        return clean_value


class PortField(IntField):
    __MIN_VALUE = 0
    __MAX_VALUE = 2**16 - 1

    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: int = None,
            description: str = None,
            min_value: int = None,
            max_value: int = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
            min_value=max(min_value or self.__MIN_VALUE, self.__MIN_VALUE),
            max_value=min(max_value or self.__MAX_VALUE, self.__MAX_VALUE),
        )
