from typing import Any

import pytest

import logging
import enum
from pathlib import Path as _Path

from configoo.field import *


class TestIntegerField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            IntField(),
            123,
            123,
        ),
        (
            IntField(),
            -123,
            -123,
        ),
        (
            IntField(),
            0,
            0,
        ),
        (
            IntField(max_value=100),
            -123,
            -123,
        ),
        (
            IntField(min_value=-100),
            123,
            123,
        ),
        (
            IntField(min_value=10, max_value=20),
            15,
            15,
        ),
        (
            IntField(min_value=-20, max_value=-10),
            -15,
            -15,
        ),
        (
            IntField(min_value=0, max_value=0),
            0,
            0,
        ),
        (
            IntField(min_value=-123, max_value=321),
            '213',
            213,
        ),
    ])
    def test_valid_parse(self, field: IntField, value: Any, expected: int):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            IntField(),
            'foo',
        ),
        (
            IntField(),
            None,
        ),
        (
            IntField(),
            '1.321',
        ),
        (
            IntField(),
            '[0]',
        ),
        (
            IntField(min_value=10, max_value=20),
            50,
        ),
        (
            IntField(min_value=10, max_value=20),
            5,
        ),
        (
            IntField(min_value=-20, max_value=-10),
            -4,
        ),
        (
            IntField(min_value=-20, max_value=-10),
            -40,
        ),
        (
            IntField(min_value=1, max_value=-1),
            0,
        ),
        (
            IntField(min_value=-123, max_value=321),
            '321123',
        ),
    ])
    def test_invalid_parse(self, field: IntField, value: Any):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestFloatField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            FloatField(),
            123.456,
            123.456,
        ),
        (
            FloatField(),
            -123.456,
            -123.456,
        ),
        (
            FloatField(),
            0.123,
            0.123,
        ),
        (
            FloatField(max_value=100),
            -123,
            -123.0,
        ),
        (
            FloatField(min_value=-100),
            123,
            123.0,
        ),
        (
            FloatField(min_value=10, max_value=20),
            15,
            15.0,
        ),
        (
            FloatField(min_value=-20, max_value=-10),
            -15,
            -15.0,
        ),
        (
            FloatField(min_value=0, max_value=0),
            0,
            0.0,
        ),
        (
            FloatField(min_value=-123, max_value=321),
            '213.321',
            213.321,
        ),
        (
            FloatField(min_value=0.1, max_value=0.2),
            '0.15',
            0.15,
        ),
    ])
    def test_valid_parse(self, field: FloatField, value: Any, expected: float):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == pytest.approx(expected)

    @pytest.mark.parametrize('field,value', [
        (
            FloatField(),
            'foo',
        ),
        (
            FloatField(),
            None,
        ),
        (
            FloatField(),
            'e1.321123',
        ),
        (
            FloatField(),
            '[0.0]',
        ),
        (
            FloatField(min_value=10, max_value=20),
            50.0,
        ),
        (
            FloatField(min_value=10, max_value=20),
            5.5,
        ),
        (
            FloatField(min_value=-20, max_value=-10),
            -4.4,
        ),
        (
            FloatField(min_value=-20, max_value=-10),
            -40.123,
        ),
        (
            FloatField(min_value=1, max_value=-1),
            0.0,
        ),
        (
            FloatField(min_value=-123, max_value=321),
            '3211.23',
        ),
        (
            FloatField(min_value=0.1, max_value=0.2),
            '0.085',
        ),
        (
            FloatField(min_value=0.1, max_value=0.2),
            '0.215',
        ),
    ])
    def test_invalid_parse(self, field: FloatField, value: Any):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestNumberField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            NumField(),
            123,
            123,
        ),
        (
            NumField(),
            -123,
            -123,
        ),
        (
            NumField(),
            0,
            0,
        ),
        (
            NumField(max_value=100),
            -123,
            -123,
        ),
        (
            NumField(min_value=-100),
            123,
            123,
        ),
        (
            NumField(min_value=10, max_value=20),
            15,
            15,
        ),
        (
            NumField(min_value=-20, max_value=-10),
            -15,
            -15,
        ),
        (
            NumField(min_value=0, max_value=0),
            0,
            0,
        ),
        (
            NumField(min_value=-123, max_value=321),
            '213',
            213,
        ),
        (
            NumField(min_value=1.9, max_value=2.1),
            '2',
            2,
        ),
    ])
    def test_valid_parse_int(self, field: NumField, value: Any, expected: int):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value,expected', [
        (
            NumField(),
            123.456,
            123.456,
        ),
        (
            NumField(),
            -123.456,
            -123.456,
        ),
        (
            NumField(),
            0.123,
            0.123,
        ),
        (
            NumField(max_value=100),
            -123,
            -123,
        ),
        (
            NumField(min_value=-100),
            123,
            123,
        ),
        (
            NumField(min_value=10, max_value=20),
            15.5,
            15.5,
        ),
        (
            NumField(min_value=-20, max_value=-10),
            -15.9,
            -15.9,
        ),
        (
            NumField(min_value=0, max_value=0),
            0,
            0,
        ),
        (
            NumField(min_value=-123, max_value=321),
            '213.321',
            213.321,
        ),
        (
            NumField(min_value=0.1, max_value=0.2),
            '0.15',
            0.15,
        ),
        (
            NumField(min_value=1.9, max_value=2.1),
            '2.01',
            2.01,
        ),
    ])
    def test_valid_parse_floatField(self, field: NumField, value: Any, expected: float):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == pytest.approx(expected)

    @pytest.mark.parametrize('field,value', [
        (
            NumField(),
            'foo',
        ),
        (
            NumField(),
            None,
        ),
        (
            NumField(),
            'e1.321123',
        ),
        (
            NumField(),
            '[0.0]',
        ),
        (
            NumField(min_value=10, max_value=20),
            50,
        ),
        (
            NumField(min_value=10, max_value=20),
            5,
        ),
        (
            NumField(min_value=-20, max_value=-10),
            -4,
        ),
        (
            NumField(min_value=10, max_value=20),
            50.0,
        ),
        (
            NumField(min_value=10, max_value=20),
            5.5,
        ),
        (
            NumField(min_value=-20, max_value=-10),
            -4.4,
        ),
        (
            NumField(min_value=-20, max_value=-10),
            -40.123,
        ),
        (
            NumField(min_value=1, max_value=-1),
            0.0,
        ),
        (
            NumField(min_value=-123, max_value=321),
            '3211.23',
        ),
        (
            NumField(min_value=0.1, max_value=0.2),
            '0.085',
        ),
        (
            NumField(min_value=0.1, max_value=0.2),
            '0.215',
        ),
    ])
    def test_invalid_parse(self, field: NumField, value: Any):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestStringField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            StrField(),
            'foo',
            'foo',
        ),
        (
            StrField(),
            '',
            '',
        ),
        (
            StrField(),
            None,
            'None',
        ),
        (
            StrField(),
            '1234',
            '1234',
        ),
        (
            StrField(),
            1234,
            '1234',
        ),
        (
            StrField(),
            123.456,
            '123.456',
        ),
        (
            StrField(),
            [0],
            '[0]',
        ),
        (
            StrField(modifyer=StrField.Modifyer.NONE),
            'bar',
            'bar',
        ),
        (
            StrField(modifyer=StrField.Modifyer.NONE),
            'BAR',
            'BAR',
        ),
        (
            StrField(modifyer=StrField.Modifyer.LOWER),
            'bar',
            'bar',
        ),
        (
            StrField(modifyer=StrField.Modifyer.LOWER),
            'BAR',
            'bar',
        ),
        (
            StrField(modifyer=StrField.Modifyer.UPPER),
            'BAR',
            'BAR',
        ),
        (
            StrField(modifyer=StrField.Modifyer.UPPER),
            'bar',
            'BAR',
        ),
        (
            StrField(modifyer=StrField.Modifyer.TITLE),
            'bar',
            'Bar',
        ),
        (
            StrField(modifyer=StrField.Modifyer.TITLE),
            'BAR',
            'Bar',
        ),
    ])
    def test_valid_parse(self, field: StrField, value: Any, expected: str):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected


class TestPathField:
    FILE = _Path(__file__)
    DIR = FILE.parent
    RESOURCES = DIR / 'resources' / 'field' / 'path'

    @pytest.mark.parametrize('field,value,expected', [
        (
            PathField(),
            str(FILE),
            FILE,
        ),
        (
            PathField(),
            str(DIR),
            DIR,
        ),
        (
            PathField(),
            str(FILE.absolute()),
            FILE,
        ),
        (
            PathField(exists=None, readable=None, writable=None, executable=None),
            _Path('/'),
            _Path('/'),
        ),
        (
            PathField(exists=False),
            str(RESOURCES / 'foo'),
            RESOURCES / 'foo',
        ),
        (
            PathField(exists=True),
            str(RESOURCES / 'file'),
            RESOURCES / 'file',
        ),
        (
            PathField(readable=True, writable=False, executable=False),
            RESOURCES / 'readable.txt',
            RESOURCES / 'readable.txt',
        ),
        (
            PathField(writable=True, readable=False, executable=False),
            RESOURCES / 'writable.txt',
            RESOURCES / 'writable.txt',
        ),
        (
            PathField(executable=True, readable=None, writable=False),
            RESOURCES / 'executable.txt',
            RESOURCES / 'executable.txt',
        ),
    ])
    def tets_valid_parse(self, field: PathField, value, expected: _Path):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            PathField(),
            1234,
        ),
        (
            PathField(),
            ['/root'],
        ),
        (
            PathField(),
            None,
        ),
        (
            PathField(exists=False),
            str(FILE.absolute()),
        ),
        (
            PathField(readable=False),
            RESOURCES / 'readable.txt',
        ),
        (
            PathField(writable=True),
            RESOURCES / 'readable.txt',
        ),
        (
            PathField(executable=True),
            RESOURCES / 'readable.txt',
        ),
        (
            PathField(executable=True),
            RESOURCES / 'writable.txt',
        ),
        (
            PathField(writable=True),
            RESOURCES / 'executable.txt',
        ),
        (
            PathField(executable=False),
            RESOURCES / 'executable.txt',
        ),
        (
            PathField(exists=False),
            str(RESOURCES / 'file'),
        ),
    ])
    def tets_invalid_parse(self, field: PathField, value):
        with pytest.raises(FieldValueError):
            field.parse(value)
    
    @pytest.mark.parametrize('field,value,expected', [
        (
            FilePathField(),
            str((RESOURCES / 'file').absolute()),
            RESOURCES / 'file',
        ),
        (
            FilePathField(readable=True, exists=True),
            str(RESOURCES / 'readable.txt'),
            RESOURCES / 'readable.txt',
        ),
    ])
    def test_file_valid_parse(self, field: FilePathField, value, expected: _Path):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            FilePathField(),
            str((RESOURCES / 'foo').absolute()),
        ),
        (
            FilePathField(exists=False),
            str(RESOURCES / 'bar.txt'),
        ),
    ])
    def test_file_invalid_parse(self, field: FilePathField, value):
        with pytest.raises(FieldValueError):
            field.parse(value)

    @pytest.mark.parametrize('field,value,expected', [
        (
            DirectoryPathField(exists=True, readable=True),
            str((RESOURCES / 'dir').absolute()),
            RESOURCES / 'dir',
        ),
    ])
    def test_dir_valid_parse(self, field: DirectoryPathField, value, expected: _Path):
        actual = field.parse(value)
        assert isinstance(actual, type(expected))
        assert actual == expected

    @pytest.mark.parametrize('field,value', [
        (
            DirectoryPathField(exists=False),
            str((RESOURCES / 'invalid-dir').absolute()),
        ),
    ])
    def test_dir_invalid_parse(self, field: DirectoryPathField, value):
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
        field = EnumField(None)
        assert field.dtype is None

        field.dtype = self.Enum1
        assert field.dtype is self.Enum1

    @pytest.mark.parametrize('dtype', [
        Enum1,
        Enum2,
    ])
    def test_valid_parse(self, dtype):
        field = EnumField(dtype)

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
        field = EnumField(dtype)
        
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestLoggingLevelField:
    @pytest.mark.parametrize('field,value,expected', [
        (
            LoggingLevelField(),
            'debug',
            logging.DEBUG,
        ),
        (
            LoggingLevelField(),
            'INFO',
            logging.INFO,
        ),
        (
            LoggingLevelField(),
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
            LoggingLevelField(),
            10,
        ),
        (
            LoggingLevelField(),
            logging.INFO,
        ),
        (
            LoggingLevelField(),
            'foo',
        ),
        (
            LoggingLevelField(),
            'BAR',
        ),
        (
            LoggingLevelField(),
            'DUBEG',
        ),
        (
            LoggingLevelField(),
            'warm',
        ),
        (
            LoggingLevelField(),
            'ifno',
        ),
    ])
    def test_invalid_parse(self, field, value):
        with pytest.raises(FieldValueError):
            field.parse(value)


class TestLoggingRecordFormatField:
    pass


class TestUrlField:
    pass


class TestRouteField:
    pass


class TestIpAddressField:
    pass


class TestListField:
    class Enum1(enum.Enum):
        FOO = 'foo'
        BAR = 'bar'
        SPAM = 'spam'
        EGGS = 'eggs'

    def test_attrs(self):
        field1 = ListField(None)
        assert field1.dtype is None

        s = StrField()
        field1.dtype = s
        assert field1.dtype is s

        i = IntField()
        field2 = ListField(dtype=i)
        assert field2.dtype is not field1.dtype
        assert field2.dtype is i

        n = field2.dtype = NumField()
        assert field1.dtype is not field2.dtype
        assert field1.dtype is s
        assert field2.dtype is n

    @pytest.mark.parametrize('field,value,expected', [
        (
            ListField(IntField()),
            '0,1,2,3,4,5,6,7,8,9',
            list(range(10)),
        ),
        (
            ListField(IntField()),
            '2,3,1,4',
            [2, 3, 1, 4],
        ),
        (
            ListField(IntField(), separator='/'),
            '10/100/1000/10000',
            [10, 100, 1000, 10000],
        ),
        (
            ListField(StrField(), separator=';'),
            '10;100;1000;10000',
            ['10', '100', '1000', '10000'],
        ),
        (
            ListField(StrField(), separator=';', skip_empty_parts=True),
            ';10;100;;;1000;10000;;',
            ['10', '100', '1000', '10000'],
        ),
        (
            ListField(NumField(), separator=';', not_empty=True),
            '1',
            [1],
        ),
        (
            ListField(PathField(), separator=';', length=2),
            ';'.join(str(p) for p in (_Path(__file__), '.')),
            [_Path(__file__), _Path('.')],
        ),
        (
            ListField(EnumField(Enum1), separator='.'),
            '.'.join((Enum1.FOO.value, Enum1.EGGS.value)),
            [Enum1.FOO, Enum1.EGGS],
        )
    ])
    def test_valid_parse(self, field: ListField, value, expected):
        actual = field.parse(value)

        assert isinstance(actual, type(expected))
        
        assert len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert isinstance(a, type(e))
            assert a == e


class TestDictField:
    class Enum1(enum.Enum):
        FOO = 'foo'
        BAR = 'bar'
        SPAM = 'spam'
        EGGS = 'eggs'

    def test_attrs(self):
        field1 = DictField(None, None)
        assert field1.key_dtype is None
        assert field1.value_dtype is None

        s = StrField()
        field1.key_dtype = s
        assert field1.key_dtype is s
        assert field1.value_dtype is None

        i1 = IntField()
        i2 = IntField()
        field2 = DictField(key_dtype=i1, value_dtype=i2)
        assert field2.key_dtype is not field1.key_dtype
        assert field2.key_dtype is i1
        assert field2.value_dtype is not field1.value_dtype
        assert field2.value_dtype is i2

        n1 = field2.key_dtype = NumField()
        assert field1.key_dtype is not field2.key_dtype
        assert field1.key_dtype is s
        assert field2.key_dtype is n1
        
        n2 = field2.value_dtype = NumField()
        assert field1.value_dtype is not field2.value_dtype
        assert field1.value_dtype is None
        assert field2.value_dtype is n2

    @pytest.mark.parametrize('field,value,expected', [
        (
            DictField(IntField(), IntField()),
            '0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10',
            {
                i: i + 1
                for i in range(10)
            },
        ),
        (
            DictField(StrField(), IntField()),
            'foo:2,bar:3,egg:1,spam:4',
            {
                'egg': 1,
                'foo': 2,
                'bar': 3,
                'spam': 4,
            },
        ),
        (
            DictField(StrField(), StrField(), separator=('-', '|')),
            'a-10|b-100|c-1000|d-10000',
            {
                'a': '10',
                'b': '100',
                'c': '1000',
                'd': '10000',
            },
        ),
        (
            DictField(StrField(), EnumField(Enum1), separator=('.', ';'), not_empty=True),
            f"foo.{Enum1.FOO.value};bar.{Enum1.BAR.value};spam.{Enum1.SPAM.value}",
            {
                'foo': Enum1.FOO,
                'spam': Enum1.SPAM,
                'bar': Enum1.BAR,
            },
        ),
        (
            DictField(
                key_dtype=StrField(),
                value_dtype=ListField(
                    dtype=IntField(min_value=0, max_value=100),
                    separator=',',
                ),
                separator=(':', ';'),
            ),
            "x:9,8,7;y:65,43;z:1,2,0,1,3;w:0",
            {
                'x': [9, 8, 7],
                'y': [65, 43],
                'z': [1, 2, 0, 1, 3],
                'w': [0],
            },
        ),
    ])
    def test_valid_parse(self, field: DictField, value, expected):
        actual = field.parse(value)

        assert isinstance(actual, type(expected))
        
        assert len(actual) == len(expected)
        for key, expected_value in expected.items():
            actual_value = actual[key]
            assert isinstance(actual_value, type(expected_value))
            assert actual_value == expected_value
