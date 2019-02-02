import pytest

import logging
from enum import Enum
from pathlib import Path

from configoo import field, model, loader


class Config(model.Model):
    class Mode(Enum):
        A = 'a'
        B = 'b'
        C = 'c'
    
    RUNNING_MODE = field.EnumField(Mode, default=Mode.A)

    LISTEN_PORT = field.PortField(
        min_value=1000,
        max_value=10000,
        default=8000,
    )

    LISTEN_ENDPOINT = field.RouteField(default='/webhook')

    REMOTE_ENDPOINTS = field.ListField(
        dtype=field.RouteField(),
        not_empty=True,
        separator=';',
        skip_empty_parts=True,
    )

    PRESET_PATH: Path = field.FilePathField(required=True, exists=True, readable=True)

    LOG_LEVEL = field.LoggingLevelField()
    LOG_PATH: Path = field.DirectoryPathField(required=True, exists=True, writable=True)

    SCHEMA = field.DictField(
        field.StrField(modifyer=field.StrField.Modifyer.UPPER),
        field.StrField(modifyer=field.StrField.Modifyer.LOWER),
        required=True,
    )


@pytest.mark.skip
class TestBaseLoader:
    pass


class TestEnvLoader:
    def test_valid_config(self, monkeypatch):
        envs = {
            'RUNNING_MODE': 'b',
            # LISTEN_PORT missed
            # LISTEN_ENDPOINT missed
            'REMOTE_ENDPOINTS': '/endpoint1;/endpoint2;/endpoint3',
            'PRESET_PATH': f'{__file__}',
            'LOG_LEVEL': 'info',
            'LOG_PATH': './',
            'SCHEMA': {
                'FOO': 'BAR',
                'spam': 'eggs',
            },
        }

        def getenv(name: str, default=None):
            return envs.get(name, default)

        monkeypatch.setattr('configoo.loader.env.getenv', getenv)
        
        l = loader.EnvLoader(
            driver=loader.EnvLoaderDriver(),
        )
        
        config = l.load_model(Config)

        assert config.RUNNING_MODE is config.Mode.B
        assert config.LISTEN_PORT == 8000
        assert config.LISTEN_ENDPOINT == '/webhook'
        assert config.REMOTE_ENDPOINTS == ['/endpoint1', '/endpoint2', '/endpoint3']
        assert config.PRESET_PATH == Path(__file__)
        assert config.LOG_LEVEL == logging.INFO
        assert config.LOG_PATH == Path('.')
        assert config.SCHEMA == {'FOO': 'bar', 'SPAM': 'eggs'}


class TestJsonLoader:
    RESOURCES = Path(__file__).parent / 'resources'
    VALID_CONFIG_PATH = RESOURCES / 'json_config1.json'

    def test_valid_config(self):
        l = loader.JsonLoader(
            driver=loader.JsonLoaderDriver(),
        )

        config = l.load_model(Config, path=self.VALID_CONFIG_PATH)

        assert config.RUNNING_MODE is config.Mode.B
        assert config.LISTEN_PORT == 8000
        assert config.LISTEN_ENDPOINT == '/webhook'
        assert config.REMOTE_ENDPOINTS == ['/endpoint1', '/endpoint2', '/endpoint3']
        assert config.PRESET_PATH.absolute() == self.VALID_CONFIG_PATH
        assert config.LOG_LEVEL == logging.INFO
        assert config.LOG_PATH.absolute() == self.RESOURCES
        assert config.SCHEMA == {'FOO': 'bar', 'SPAM': 'eggs'}
