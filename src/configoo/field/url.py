from typing import Type, Union
from ipaddress import ip_address, IPv4Address, IPv6Address

from .base import Field, PT, RT
from .exception import FieldValueError

__all__ = [
    'Url',
    'IpAddress',
    'Route',
]


IP = Union[IPv4Address, IPv6Address]


class Url(Field[str, str]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Union[IP, str] = None,
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
        return value


class Route(Field[str, str]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Union[IP, str] = None,
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
        return value


class IpAddress(Field[str, IP]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: Union[IP, str] = None,
            description: str = None,
    ) -> None:
        if default is not None and not isinstance(default, IP):
            default = ip_address(default)
        
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
