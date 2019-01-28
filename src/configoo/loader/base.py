from abc import ABCMeta, abstractmethod
from typing import TypeVar, Type

from ..field import FieldDefinition, PT, RT
from ..model import Model

__all__ = [
    'Loader',
]

M = TypeVar('M', bound=Model)


class Loader(metaclass=ABCMeta):
    def load(
            self,
            model: Type[M],
    ) -> M:
        data = {
            key: self.load_field(field)
            for key, field in model.iter_fields()
        }

        return model(**data)
    
    @abstractmethod
    def load_field(self, field: FieldDefinition[PT, RT]) -> RT:
        pass
