#! /usr/bin/env python3


import sys
import pytest
import select
from io import StringIO
from unittest import mock

from .. import tools


@pytest.fixture
def dictData():
    data = {
        'a': [1, 2],
        'b': [3, 4],
        'c': [5, 6]}
    return data


def test_yesNo():
    test_values = {
        'true': ['y', 'ye', 'yes'],
        'false': ['n', 'no']}

    for true in test_values['true']:
        with mock.patch('builtins.input', return_value=true):
            assert tools.yesNo() == True

    for false in test_values['false']:
        with mock.patch('builtins.input', return_value=false):
            assert tools.yesNo() == False

    random_values = [
        '', '8', 0, None, True, False, [], [0, 1, 'test'], {'a': 0}]
    for random in random_values:
        with mock.patch('builtins.input', return_value=random):
            assert tools.yesNo() == False

def test_toInt():
    i = tools.toInt
    assert i(1) == 1
    assert i(0) == 0
    assert i('1') == 1
    assert i('0') == 0
    assert i('a') == None
    assert i(None) == None
    assert i(True) == 1
    assert i(False) == 0


def test_cordinateTuple():
    c = tools.cordinateTuple
    assert c('0x1') == (0, 1)
    assert c('1x') == (1, None)
    assert c('x0') == (None, 0)
    assert c('x') == (None, None)


def test_genObj():
    data = ['a', 'b', ['c', 'd']]
    class Test():
        def __init__(self, data):
            self.data = data

    objs = tuple(tools.genObj(Test, data))

    assert objs[0].data == 'a'
    assert objs[1].data == 'b'
    assert objs[2].data == ['c', 'd']


def test_listFromDict(dictData):
    new_list = list(tools.listFromDict(dictData))

    assert new_list[0] == ['a', [1, 2]]
    assert new_list[1] == ['b', [3, 4]]
    assert new_list[2] == ['c', [5, 6]]

def test_rule():
    rule = tools.Rule(['a', [1, 2]])

    assert rule.getKey() == 'a'
    assert rule.getRules() == [1, 2]

    rule.setValue(0, '3 4')
    assert rule.getRules() == [['3', '4'], 2]

    rule.setKey('test')
    assert rule.getKey() == 'test'

    rule.removeRule(['3', '4'])
    assert rule.getRules() == [2]


def test_database(dictData):
    db = tools.Database(dictData)
    rules = db.getRules()

    assert tuple(db.getKeys()) == tuple(('a', 'b', 'c'))

    assert rules[0].getRules() == [1, 2]
    assert rules[1].getRules() == [3, 4]
    assert rules[2].getRules() == [5, 6]

    assert db.returnDb() == dictData


def test_database_add_remove(dictData):
    db = tools.Database(dictData)

    new_dict = dict(dictData)
    new_dict.update({'key': []})

    db.addRule('key')
    assert db.returnDb() == new_dict

    db.removeRule('key')
    assert db.returnDb() == dictData


def test_database_commands(dictData):
    data = {
        'a': [['1'], ['2']],
        'b': [['d'], ['e']],
        'c': [['0'], ['e']]}
    db = tools.Database(data)

    defdata = {'default': ['firefox']}
    configs = tools.Configuration(defdata)

    r = db.returnCommands('a', configs)
    assert list(db.returnCommands('a', configs)) == [['1', 'a'], ['2', 'a']]
    assert (
        list(db.returnCommands('not_found', configs)) ==
        [['firefox', 'not_found']])


def test_Config():
    data = ['Name', 'name', 'setting']
    config = tools.Config(data)

    assert config.getPretty() == 'name'
    assert config.getName() == 'Name'
    assert config.getValue() == 'setting'

    config.setValue('1')
    
    assert config.getValue() == ['1']


def test_Configuration():
    data = {'default': 'firefox'}
    configs = tools.Configuration(data)
    config = configs.getConfigs()

    assert list(configs.getValue('default')) == ['firefox']

    assert config[0].getName() == 'default'
    assert config[0].getPretty() == 'Default'
    assert config[0].getValue() == 'firefox'

    assert configs.returnConfigs() == data


def test_readStdin():
    """Yeah this one goes a bit over my head..."""

    with mock.patch('select.select', lambda v, x, y, z: v):
        with mock.patch('sys.stdin', StringIO('n n \n')):
            assert list(tools.readStdin()) == ['nn']


def test_fuzzyFromList():
    youtube = 'https://www.youtube.com'
    datalist = [
        'https://www.twitch.com',
        'https://www.youtube.com']

    program = tools.fuzzyFromList('https://www.youtube.com?v=', datalist)
    
    assert program == youtube


def test_regexLink():
    https = 'https://www.youtube.com'
    http = 'http://www.youtube.com'
    nonsense = 'qwerty'

    test0 = tools.regexLink(https)
    assert test0 == https

    test1 = tools.regexLink(http)
    assert test1 == http

    test2 = tools.regexLink(nonsense)
    assert test2 == None
