import pytest

from .main import check_len, check_param, check_type


def test_check_param():
    assert check_param(12, 60, 1, 2) is True
    assert check_param(16, 100, 6, 8) is True
    assert check_param(-10, -10, -10, -10) is False
    assert check_param(150, 150, 150, 150) is False
    assert check_param(12, 60, -10, -10) is False


def test_check_type():
    assert check_type(('100', '200', '300')) is True
    assert check_type(('100', '200')) is True
    assert check_type(('-100', '-200', '-300')) is False
    assert check_type(('aaa', 'bbb', 'ccc')) is False
    assert check_type(('a', 'b', 'c')) is False
    assert check_type(('10.5', '10.5', '10.5')) is False
    assert check_type(('-100', 'abc', '10.5')) is False
    assert check_type(('100', 'abc', '-10.5')) is False


def test_check_len():
    assert check_len(('100', '200', '300', '400')) is True
    assert check_len(('100', '200')) is False
    assert check_len(('-100', '-200', '-300', '400')) is True
    assert check_len(('-100', '-200')) is False
    assert check_len(('aaa', 'bbb', 'ccc', 'ddd')) is True
    assert check_len(('aaa', 'bbb')) is False
    assert check_len(('a', 'b', 'c', 'd')) is True
    assert check_len(('a', 'b')) is False