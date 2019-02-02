from typing import TypeVar, Type, Iterable, Tuple, Any, Union, List, Dict

from pathlib import Path

from .loader import (
    Loader,
    LoaderDriver,
    EnvLoader,
    EnvLoaderDriver,
    JsonLoader,
    JsonLoaderDriver,
)

__all__ = [
    'load_from_env',
    'load_from_json',
    'load_rewriting',
    'load_appending',
]


T = TypeVar('T')
LoaderItem = Union[Loader, Tuple[Loader], Tuple[Loader, Any], Tuple[Loader, Any, Any]]


def load_from_env(
        model: Type[T],
        loader: Type[EnvLoader] = None,
        driver: EnvLoaderDriver = None,
) -> T:
    loader = (loader or EnvLoader)(
        driver=driver,
    )

    return loader.load_model(
        model=model,
    )


def load_from_json(
        model: Type[T],
        path: Path,
        loader: Type[JsonLoader] = None,
        driver: JsonLoaderDriver = None,
) -> T:
    loader = (loader or JsonLoader)(
        driver=driver,
    )

    return loader.load_model(
        model=model,
        path=path,
    )


def __get_loader_args_kwargs(
        item: LoaderItem,
        default_args: Any = None,
        default_kwargs: Any = None,
) -> Tuple[Loader, List[Any], Dict[str, Any]]:
    return (
        item[0] if isinstance(item, tuple) else item,
        item[1] if isinstance(item, tuple) else default_args or [],
        item[2] if isinstance(item, tuple) else default_kwargs or {},
    )


def load_rewriting(
        model: Type[T],
        loaders: Iterable[LoaderItem],
) -> T:
    data = {}

    for item in loaders:
        loader, args, kwargs = __get_loader_args_kwargs(item)

        context = loader.driver.create_context(
            model=model,
            *args,
            **kwargs,
        )

        context_data = loader.load(context)
        data.update(context_data)
    
    return model(**data)


def load_appending(
        model: Type[T],
        loaders: Iterable[LoaderItem],
) -> T:
    data = {}

    for item in loaders:
        loader, args, kwargs = __get_loader_args_kwargs(item)
        
        context = loader.driver.create_context(
            model=model,
            *args,
            **kwargs,
        )

        context_data = loader.load(context)
        for key, value in context_data.items():
            data.setdefault(key, value)
    
    return model(**data)
