from typing import Type, Union
from os import access, R_OK, W_OK, X_OK
from pathlib import Path as _Path

from .base import Field, PT, RT
from .exception import ParseError

__all__ = [
    'Path',
    'FilePath',
    'DirectoryPath',
]

AnyPath = Union[_Path, str]


class Path(Field[str, _Path]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: AnyPath = None,
            exists: bool = None,
            readable: bool = None,
            writable: bool = None,
            executable: bool = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            parse_type=str,
            return_type=_Path,
        )

        self.__exists = exists
        self.__readable = readable
        self.__writable = writable
        self.__executable = executable
    
    def parse(self, value: str) -> _Path:
        try:
            clean_value = _Path(value)
        
        except TypeError as err:
            raise ParseError(
                "Invalid path value!",
                value,
            )
        
        self.check_exists(clean_value)
        
        if (
                self.__readable is None
                and self.__writable is None
                and self.__executable is None
        ):
            return clean_value
        
        self.check_readable(clean_value)
        self.check_writable(clean_value)
        self.check_executable(clean_value)

        return clean_value
    
    def check_exists(self, path: _Path) -> bool:
        if self.__exists is not None:
            clean_exists = path.exists()
            if self.__exists and not clean_exists:
                raise ParseError(
                    "Path does not exists!",
                    path,
                )
            
            if not self.__exists and clean_exists:
                raise ParseError(
                    "Path does exists!",
                    path,
                )
        
        return True
    
    def check_readable(self, path: _Path) -> None:
        if self.__readable is not None:
            readable = access(path, R_OK)
            if self.__readable and not readable:
                raise ParseError(
                    "Path is not readable!",
                    path,
                )
            
            if not self.__readable and readable:
                raise ParseError(
                    "Path is readable!",
                    path,
                )
        
        return True

    def check_writable(self, path: _Path) -> None:
        if self.__writable is not None:
            writable = access(path, W_OK)
            if self.__writable and not writable:
                raise ParseError(
                    "Path is not writable!",
                    path,
                )
            
            if not self.__writable and writable:
                raise ParseError(
                    "Path is writable!",
                    path,
                )

        return True

    def check_executable(self, path: _Path) -> None:
        if self.__executable is not None:
            executable = access(path, X_OK)
            if self.__executable and not executable:
                raise ParseError(
                    "Path is not executable!",
                    path,
                )
            
            if not self.__executable and executable:
                raise ParseError(
                    "Path is executable!",
                    path,
                )

        return True


class FilePath(Path):
    def parse(self, value: str) -> _Path:
        clean_value = super().parse(value)

        if not clean_value.is_file():
            raise ParseError(
                "Path is not a file!",
                clean_value,
            )

        return clean_value


class DirectoryPath(Path):
    def parse(self, value: str) -> _Path:
        clean_value = super().parse(value)

        if not clean_value.is_dir():
            raise ParseError(
                "Path is not a directory!",
                clean_value,
            )

        return clean_value