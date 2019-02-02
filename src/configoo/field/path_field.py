from typing import Type, Union
from os import access, R_OK, W_OK, X_OK
from pathlib import Path as _Path

from .base import Field, PT, RT
from ..exception import FieldValueError

__all__ = [
    'PathField',
    'FilePathField',
    'DirectoryPathField',
]

AnyPath = Union[_Path, str]


class PathField(Field[str, _Path]):
    def __init__(
            self,
            name: str = None,
            required: bool = False,
            default: AnyPath = None,
            description: str = None,
            exists: bool = None,
            readable: bool = None,
            writable: bool = None,
            executable: bool = None,
    ) -> None:
        super().__init__(
            name=name,
            required=required,
            default=default,
            description=description,
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
            raise FieldValueError(
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
                raise FieldValueError(
                    "Path does not exists!",
                    path,
                )
            
            if not self.__exists and clean_exists:
                raise FieldValueError(
                    "Path does exists!",
                    path,
                )
        
        return True
    
    def check_readable(self, path: _Path) -> None:
        if self.__readable is not None:
            readable = access(path, R_OK)
            if self.__readable and not readable:
                raise FieldValueError(
                    "Path is not readable!",
                    path,
                )
            
            if not self.__readable and readable:
                raise FieldValueError(
                    "Path is readable!",
                    path,
                )
        
        return True

    def check_writable(self, path: _Path) -> None:
        if self.__writable is not None:
            writable = access(path, W_OK)
            if self.__writable and not writable:
                raise FieldValueError(
                    "Path is not writable!",
                    path,
                )
            
            if not self.__writable and writable:
                raise FieldValueError(
                    "Path is writable!",
                    path,
                )

        return True

    def check_executable(self, path: _Path) -> None:
        if self.__executable is not None:
            executable = access(path, X_OK)
            if self.__executable and not executable:
                raise FieldValueError(
                    "Path is not executable!",
                    path,
                )
            
            if not self.__executable and executable:
                raise FieldValueError(
                    "Path is executable!",
                    path,
                )

        return True


class FilePathField(PathField):
    def parse(self, value: str) -> _Path:
        clean_value = super().parse(value)

        if not clean_value.is_file():
            raise FieldValueError(
                "Path is not a file!",
                clean_value,
            )

        return clean_value


class DirectoryPathField(PathField):
    def parse(self, value: str) -> _Path:
        clean_value = super().parse(value)

        if not clean_value.is_dir():
            raise FieldValueError(
                "Path is not a directory!",
                clean_value,
            )

        return clean_value
