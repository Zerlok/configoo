__all__ = [
    'LoaderError',
    'LoaderModelFieldError',
]


class LoaderError(Exception):
    pass


class LoaderModelFieldError(LoaderError):
    pass
