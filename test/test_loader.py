import pytest
from pathlib import Path

from configlib import field, model, loader


def create_model_with_fields(*args) -> 'MockModel':
    class MockModel(model.Model):
        fields = {
            name: dtype
            for name, dtype in args
        }

        @classmethod
        def iter_fields(cls):
            return cls.fields.items()

        def __init__(self, **kwargs):
            self.data = kwargs

    return MockModel


class MockLoader(loader.Loader):
    def load_field(self, field):
        return field


class TestBaseLoader:
    def test_valid_config(self):
        fields = [
            ('field1', str),
            ('field2', int),
            ('field3', float),
        ]

        Model = create_model_with_fields(*fields)

        loader_ = MockLoader()
        config = loader_.load(Model)

        for name, dtype in fields:
            assert name in config.data
            assert config.data[name] is dtype


class TestEnvLoader:
    class Config(model.Model):
        LISTEN_PORT = field.Integer(
            min_value=1000,
            max_value=10000,
            default=8000,
        )

        LISTEN_ENDPOINT = field.Route(default='/webhook')

        REMOTE_ENDPOINTS = field.ListField(
            dtype=field.Route(),
            not_empty=True,
            separator=';',
            skip_empty_parts=True,
        )

        PRESET_PATH = field.FilePath(required=True, exists=True, readable=True)

        LOG_PATH = field.DirectoryPath(required=True, exists=True, writable=True)
    
    def test_valid_config(self, monkeypatch):
        envs = {
            'LISTEN_PORT': (
                '8001',
                8001,
            ),
            'REMOTE_ENDPOINTS': (
                '/endpoint1;/endpoint2;/endpoint3',
                ['/endpoint1', '/endpoint2', '/endpoint3',],
            ),
            'PRESET_PATH': (
                f'{__file__}',
                Path(__file__),
            ),
            'LOG_PATH': (
                f'./',
                Path('.'),
            ),
        }

        def getenv(name: str, default=None):
            return envs.get(name, [default])[0]
        # monkeypatch.setattr('os.getenv', getenv)

        loader_ = loader.EnvLoader()
        
        # TODO: make monkeypatch work!
        loader_.get_field_value = lambda field: getenv(field.name, default=loader_._EnvLoader__NONE)
        
        config = loader_.load(self.Config)

        for key, (_, expected_value) in envs.items():
            actual_value = getattr(config, key)
            assert actual_value == expected_value
