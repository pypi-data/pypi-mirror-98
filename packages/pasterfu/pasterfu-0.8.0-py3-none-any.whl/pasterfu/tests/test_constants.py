#! /usr/bin/env python3


import pytest

from .. import constants


def test_genInsert():
    data = [0, 1, 2]

    gen = constants.genInsert
    assert list(gen(0, data, 'a')) == ['a', 0, 1, 2]
    assert list(gen(-1, data, 'a')) == [0, 1, 'a', 2]
    assert list(gen(-2, data, 'a')) == [0, 'a', 1, 2]
    assert list(gen(1, data, 'a')) == [0, 'a', 1, 2]
    assert list(gen(5, data, 'a')) == [0, 1, 2]
