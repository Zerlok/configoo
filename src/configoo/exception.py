__all__ = [
    'BaseError',
    'LoaderError',
    'ModelError',
    'FieldError',
    'UndefinedFieldError',
    'FieldValueError',
]


class BaseError(Exception):
    pass


class LoaderError(BaseError):
    pass


class ModelError(BaseError):
    pass


class FieldError(BaseError):
    pass


class UndefinedFieldError(FieldError):
    pass


class FieldValueError(FieldError):
    pass
