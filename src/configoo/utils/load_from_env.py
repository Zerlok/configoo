from typing import TypeVar, Type
from ..loader import EnvLoader

__all__ = [
    'load_from_env',
]


T = TypeVar('T')

def load_from_env(model: Type[T]) -> T:
    loader = EnvLoader()
    return loader.load(model)
