from typing import Any

import pytest

import logging
import enum
from pathlib import Path as _Path

from configoo.field import *


class TestIntegerField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            Integer(),
            123,
            123,
        ),
        (
            Integer(),
            -123,
            -123,
        ),
        (
            Integer(),
            0,
            0,
        ),
        (
            Integer(max_value=100),
            -123,
            -123,
        ),
        (
            Integer(min_value=-100),
            123,
            123,
        ),
        (
            Integer(min_value=10, max_value=20),
            15,
            15,
        ),
        (
            Integer(min_value=-20, max_value=-10),
            -15,
            -15,
        ),
        (
            Integer(min_value=0, max_value=0),
            0,
            0,
        ),
        (
            Integer(min_value=-123, max_value=321),
            '213',
            213,
        ),
    ])
    def test_valid_parse(self, field: Integer, value: Any, expected: int):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            Integer(),
            'foo',
        ),
        (
            Integer(),
            None,
        ),
        (
            Integer(),
            '1.321',
        ),
        (
            Integer(),
            '[0]',
        ),
        (
            Integer(min_value=10, max_value=20),
            50,
        ),
        (
            Integer(min_value=10, max_value=20),
            5,
        ),
        (
            Integer(min_value=-20, max_value=-10),
            -4,
        ),
        (
            Integer(min_value=-20, max_value=-10),
            -40,
        ),
        (
            Integer(min_value=1, max_value=-1),
            0,
        ),
        (
            Integer(min_value=-123, max_value=321),
            '321123',
        ),
    ])
    def test_invalid_parse(self, field: Integer, value: Any):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestFloatField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            Float(),
            123.456,
            123.456,
        ),
        (
            Float(),
            -123.456,
            -123.456,
        ),
        (
            Float(),
            0.123,
            0.123,
        ),
        (
            Float(max_value=100),
            -123,
            -123.0,
        ),
        (
            Float(min_value=-100),
            123,
            123.0,
        ),
        (
            Float(min_value=10, max_value=20),
            15,
            15.0,
        ),
        (
            Float(min_value=-20, max_value=-10),
            -15,
            -15.0,
        ),
        (
            Float(min_value=0, max_value=0),
            0,
            0.0,
        ),
        (
            Float(min_value=-123, max_value=321),
            '213.321',
            213.321,
        ),
        (
            Float(min_value=0.1, max_value=0.2),
            '0.15',
            0.15,
        ),
    ])
    def test_valid_parse(self, field: Float, value: Any, expected: float):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == pytest.approx(expected)

    @pytest.mark.parametrize('field,value', [
        (
            Float(),
            'foo',
        ),
        (
            Float(),
            None,
        ),
        (
            Float(),
            'e1.321123',
        ),
        (
            Float(),
            '[0.0]',
        ),
        (
            Float(min_value=10, max_value=20),
            50.0,
        ),
        (
            Float(min_value=10, max_value=20),
            5.5,
        ),
        (
            Float(min_value=-20, max_value=-10),
            -4.4,
        ),
        (
            Float(min_value=-20, max_value=-10),
            -40.123,
        ),
        (
            Float(min_value=1, max_value=-1),
            0.0,
        ),
        (
            Float(min_value=-123, max_value=321),
            '3211.23',
        ),
        (
            Float(min_value=0.1, max_value=0.2),
            '0.085',
        ),
        (
            Float(min_value=0.1, max_value=0.2),
            '0.215',
        ),
    ])
    def test_invalid_parse(self, field: Float, value: Any):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestNumberField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            Number(),
            123,
            123,
        ),
        (
            Number(),
            -123,
            -123,
        ),
        (
            Number(),
            0,
            0,
        ),
        (
            Number(max_value=100),
            -123,
            -123,
        ),
        (
            Number(min_value=-100),
            123,
            123,
        ),
        (
            Number(min_value=10, max_value=20),
            15,
            15,
        ),
        (
            Number(min_value=-20, max_value=-10),
            -15,
            -15,
        ),
        (
            Number(min_value=0, max_value=0),
            0,
            0,
        ),
        (
            Number(min_value=-123, max_value=321),
            '213',
            213,
        ),
        (
            Number(min_value=1.9, max_value=2.1),
            '2',
            2,
        ),
    ])
    def test_valid_parse_int(self, field: Number, value: Any, expected: int):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value,expected', [
        (
            Number(),
            123.456,
            123.456,
        ),
        (
            Number(),
            -123.456,
            -123.456,
        ),
        (
            Number(),
            0.123,
            0.123,
        ),
        (
            Number(max_value=100),
            -123,
            -123,
        ),
        (
            Number(min_value=-100),
            123,
            123,
        ),
        (
            Number(min_value=10, max_value=20),
            15.5,
            15.5,
        ),
        (
            Number(min_value=-20, max_value=-10),
            -15.9,
            -15.9,
        ),
        (
            Number(min_value=0, max_value=0),
            0,
            0,
        ),
        (
            Number(min_value=-123, max_value=321),
            '213.321',
            213.321,
        ),
        (
            Number(min_value=0.1, max_value=0.2),
            '0.15',
            0.15,
        ),
        (
            Number(min_value=1.9, max_value=2.1),
            '2.01',
            2.01,
        ),
    ])
    def test_valid_parse_float(self, field: Number, value: Any, expected: float):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == pytest.approx(expected)

    @pytest.mark.parametrize('field,value', [
        (
            Number(),
            'foo',
        ),
        (
            Number(),
            None,
        ),
        (
            Number(),
            'e1.321123',
        ),
        (
            Number(),
            '[0.0]',
        ),
        (
            Number(min_value=10, max_value=20),
            50,
        ),
        (
            Number(min_value=10, max_value=20),
            5,
        ),
        (
            Number(min_value=-20, max_value=-10),
            -4,
        ),
        (
            Number(min_value=10, max_value=20),
            50.0,
        ),
        (
            Number(min_value=10, max_value=20),
            5.5,
        ),
        (
            Number(min_value=-20, max_value=-10),
            -4.4,
        ),
        (
            Number(min_value=-20, max_value=-10),
            -40.123,
        ),
        (
            Number(min_value=1, max_value=-1),
            0.0,
        ),
        (
            Number(min_value=-123, max_value=321),
            '3211.23',
        ),
        (
            Number(min_value=0.1, max_value=0.2),
            '0.085',
        ),
        (
            Number(min_value=0.1, max_value=0.2),
            '0.215',
        ),
    ])
    def test_invalid_parse(self, field: Number, value: Any):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestStringField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            String(),
            'foo',
            'foo',
        ),
        (
            String(),
            '',
            '',
        ),
        (
            String(),
            None,
            'None',
        ),
        (
            String(),
            '1234',
            '1234',
        ),
        (
            String(),
            1234,
            '1234',
        ),
        (
            String(),
            123.456,
            '123.456',
        ),
        (
            String(),
            [0],
            '[0]',
        ),
        (
            String(modifyer=String.Modifyer.NONE),
            'bar',
            'bar',
        ),
        (
            String(modifyer=String.Modifyer.NONE),
            'BAR',
            'BAR',
        ),
        (
            String(modifyer=String.Modifyer.LOWER),
            'bar',
            'bar',
        ),
        (
            String(modifyer=String.Modifyer.LOWER),
            'BAR',
            'bar',
        ),
        (
            String(modifyer=String.Modifyer.UPPER),
            'BAR',
            'BAR',
        ),
        (
            String(modifyer=String.Modifyer.UPPER),
            'bar',
            'BAR',
        ),
        (
            String(modifyer=String.Modifyer.TITLE),
            'bar',
            'Bar',
        ),
        (
            String(modifyer=String.Modifyer.TITLE),
            'BAR',
            'Bar',
        ),
    ])
    def test_valid_parse(self, field: String, value: Any, expected: str):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected


class TestPathField:
    FILE = _Path(__file__)
    DIR = FILE.parent
    RESOURCES = DIR / 'resources' / 'field' / 'path'

    @pytest.mark.parametrize('field,value,expected', [
        (
            Path(),
            str(FILE),
            FILE,
        ),
        (
            Path(),
            str(DIR),
            DIR,
        ),
        (
            Path(),
            str(FILE.absolute()),
            FILE,
        ),
        (
            Path(exists=None, readable=None, writable=None, executable=None),
            _Path('/'),
            _Path('/'),
        ),
        (
            Path(exists=False),
            str(RESOURCES / 'foo'),
            RESOURCES / 'foo',
        ),
        (
            Path(exists=True),
            str(RESOURCES / 'file'),
            RESOURCES / 'file',
        ),
        (
            Path(readable=True, writable=False, executable=False),
            RESOURCES / 'readable.txt',
            RESOURCES / 'readable.txt',
        ),
        (
            Path(writable=True, readable=False, executable=False),
            RESOURCES / 'writable.txt',
            RESOURCES / 'writable.txt',
        ),
        (
            Path(executable=True, readable=None, writable=False),
            RESOURCES / 'executable.txt',
            RESOURCES / 'executable.txt',
        ),
    ])
    def tets_valid_parse(self, field: Path, value, expected: _Path):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            Path(),
            1234,
        ),
        (
            Path(),
            ['/root'],
        ),
        (
            Path(),
            None,
        ),
        (
            Path(exists=False),
            str(FILE.absolute()),
        ),
        (
            Path(readable=False),
            RESOURCES / 'readable.txt',
        ),
        (
            Path(writable=True),
            RESOURCES / 'readable.txt',
        ),
        (
            Path(executable=True),
            RESOURCES / 'readable.txt',
        ),
        (
            Path(executable=True),
            RESOURCES / 'writable.txt',
        ),
        (
            Path(writable=True),
            RESOURCES / 'executable.txt',
        ),
        (
            Path(executable=False),
            RESOURCES / 'executable.txt',
        ),
        (
            Path(exists=False),
            str(RESOURCES / 'file'),
        ),
    ])
    def tets_invalid_parse(self, field: Path, value):
        with pytest.raises(FieldValueError):
            field.parse(value)
    
    @pytest.mark.parametrize('field,value,expected', [
        (
            FilePath(),
            str((RESOURCES / 'file').absolute()),
            RESOURCES / 'file',
        ),
        (
            FilePath(readable=True, exists=True),
            str(RESOURCES / 'readable.txt'),
            RESOURCES / 'readable.txt',
        ),
    ])
    def test_file_valid_parse(self, field: FilePath, value, expected: _Path):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            FilePath(),
            str((RESOURCES / 'foo').absolute()),
        ),
        (
            FilePath(exists=False),
            str(RESOURCES / 'bar.txt'),
        ),
    ])
    def test_file_invalid_parse(self, field: FilePath, value):
        with pytest.raises(FieldValueError):
            field.parse(value)

    @pytest.mark.parametrize('field,value,expected', [
        (
            DirectoryPath(exists=True, readable=True),
            str((RESOURCES / 'dir').absolute()),
            RESOURCES / 'dir',
        ),
    ])
    def test_dir_valid_parse(self, field: FilePath, value, expected: _Path):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            DirectoryPath(exists=False),
            str((RESOURCES / 'invalid-dir').absolute()),
        ),
    ])
    def test_dir_invalid_parse(self, field: FilePath, value):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestEnumField:
    class Enum1(enum.Enum):
        FOO = 'foo'
        BAR = 'bar'

    class Enum2(enum.Enum):
        VAL1 = 1
        VAL2 = 2
        VAL3 = 3
    
    def test_attrs(self):
        field = Enum(None)
        assert field.dtype is None

        field.dtype = self.Enum1
        assert field.dtype is self.Enum1

    @pytest.mark.parametrize('dtype', [
        Enum1,
        Enum2,
    ])
    def test_valid_parse(self, dtype):
        field = Enum(dtype)

        for expected in dtype:
            actual = field.parse(expected.value)
            assert actual is expected

    @pytest.mark.parametrize('dtype,value', [
        (
            Enum1,
            'foo-bar-xyz',
        ),
        (
            Enum1,
            1,
        ),
        (
            Enum1,
            None,
        ),
        (
            Enum2,
            None,
        ),
        (
            Enum2,
            '1',
        ),
        (
            Enum2,
            '2',
        ),
    ])
    def test_invalid_parse(self, dtype, value):
        field = Enum(dtype)
        
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestLoggingLevelField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            LoggingLevel(),
            'debug',
            logging.DEBUG,
        ),
        (
            LoggingLevel(),
            'INFO',
            logging.INFO,
        ),
        (
            LoggingLevel(),
            'wArninG',
            logging.WARNING,
        ),
    ])
    def test_valid_parse(self, field, value, expected):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            LoggingLevel(),
            10,
        ),
        (
            LoggingLevel(),
            logging.INFO,
        ),
        (
            LoggingLevel(),
            'foo',
        ),
        (
            LoggingLevel(),
            'BAR',
        ),
        (
            LoggingLevel(),
            'DUBEG',
        ),
        (
            LoggingLevel(),
            'warm',
        ),
        (
            LoggingLevel(),
            'ifno',
        ),
    ])
    def test_invalid_parse(self, field, value):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestLoggingRecordFormatField:
    pass
