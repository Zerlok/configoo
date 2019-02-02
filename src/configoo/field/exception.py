__all__ = [
    'FieldError',
    'FieldValueError',
]


class FieldError(Exception):
    pass


class FieldValueError(FieldError):
    pass
