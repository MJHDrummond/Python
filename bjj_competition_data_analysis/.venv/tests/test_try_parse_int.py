import pytest

from app.utils.try_parse_int import try_parse_int


def test_try_parse_int_returns_int_from_int():
    result = try_parse_int(1)
    assert type(result) is int
    assert result == 1

def test_try_parse_int_returns_int_from_int_as_string():
    result = try_parse_int('1')
    assert type(result) is int
    assert result == 1

def test_try_parse_int_returns_zero_from_string():
    result = try_parse_int('test')
    assert result == 0