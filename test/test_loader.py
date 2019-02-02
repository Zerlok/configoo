import pytest

import logging
from pathlib import Path

from configoo import field, model, loader


@pytest.mark.skip
class TestBaseLoader:
    pass


class TestEnvLoader:
    class Config(model.Model):
        LISTEN_PORT = field.IntField(
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

        PRESET_PATH = field.FilePathField(required=True, exists=True, readable=True)

        LOG_LEVEL = field.LoggingLevelField()
        LOG_PATH = field.DirectoryPathField(required=True, exists=True, writable=True)
    
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
            'LOG_LEVEL': (
                f'info',
                logging.INFO,
            ),
            'LOG_PATH': (
                f'./',
                Path('.'),
            ),
        }

        def getenv(name: str, default=None):
            return envs.get(name, [default])[0]

        monkeypatch.setattr('configoo.loader.env.getenv', getenv)
        
        loader_ = loader.EnvLoader(
            driver=loader.EnvLoaderDriver(),
        )
        
        config = loader_.load_model(self.Config)

        for key, (_, expected_value) in envs.items():
            actual_value = getattr(config, key)
            assert actual_value == expected_value


@pytest.mark.skip
class TestJsonLoader:
    pass
