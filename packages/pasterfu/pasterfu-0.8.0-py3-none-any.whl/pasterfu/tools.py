#! /usr/bin/env python3


import re
import sys
import select
from itertools import chain


def yesNo(ask='', retry=2):
    """Ask user input yes/no"""

    if retry < 1:
        return False

    check = str(input(ask))
    if check.lower() in ('y', 'ye', 'yes'):
        return True
    elif check.lower() in ('n', 'no'):
        return False

    retry = retry - 1
    return yesNo(ask=ask, retry=retry)


def toInt(value):
    """Safely change value to int or None

    input: str | boolean
    output: int
    """

    try:
        i = int(value)
        return i
    except ValueError:
        return None
    except TypeError:
        return None


def cordinateTuple(value):
    """Return given str as y,x cordinates

    input: str
    output: tuple
    """

    y, x, *_ = chain(map(toInt, value.split('x')), (None, None))
    return (y, x)


def fuzzyFromList(search, datalist):
    """Perform fuzzy search from given list"""

    for fuzzy in datalist:
        if fuzzy in search:
            return fuzzy


def genObj(obj, data_list):
    """List of data into given object types.

    Returns objects as generator
    """

    obj_gen = (obj(data) for data in data_list)
    return obj_gen


def listFromDict(diction):
    """Dictionary into generator object

    (key, values)
    """

    gen = ([k, diction[k]] for k in diction)
    return gen


def regexLink(link):
    """Check that given link matches link regex"""

    r = re.compile(r'(https?://)([a-z]{1,3}\.)?(.*)')
    match = r.match(link)
    if match:
        return match.group()


def readStdin():
    """Read inputs from stdin and strip whitespaces"""

    if select.select([sys.stdin, ], [], [], 0)[0]:
        line = (''.join(i.split()) for i in sys.stdin)
        return line


class Config():
    """Single configuration value"""

    def __init__(self, data):
        self.__name = data[0]
        self.__pretty = data[1]
        self.__value = data[2]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.getName() == other
        else:
            return NotImplemented

    def __repr__(self):
        txt = (
            f'Config({self.getName()}: {{' +
            f"pretty: '{self.getPretty()}', value: '{self.getValue()}}})'")
        return txt

    def __str__(self):
        return f'{self.getPretty}: {self.getValue()}'

    def getName(self):
        """Return configuration name"""

        return self.__name

    def getPretty(self):
        """Return configuration name in pretty format"""

        return self.__pretty

    def getValue(self):
        """Return configuration value"""

        return self.__value

    def setValue(self, value):
        """Allow setting configuration value"""

        self.__value = value.split()


class Configuration():
    """All configurations"""

    __names = {
        'default': {
            'pretty': 'Default',
            'value': ''}}

    def __init__(self, data):
        if data:
            conf = (
                (d[0], self.__names[d[0]]['pretty'], d[1])
                for d in listFromDict(data))
        else:
            conf = (
                (d, self.__names[d]['pretty'], self.__names[d]['value'])
                for d in self.__names)

        configs = tuple(genObj(Config, conf))
        self.__configs = configs

    def __str__(self):
        lines = ''
        for i, c in enumerate(self.__configs):
            if i != 0:
                lines += '\n'
            lines += f'#{i} {c.getPretty()}: {c.getValue()}'
        return lines

    def getConfigs(self):
        """Return all configurations"""

        return self.__configs

    def getConfig(self, key):
        """Return specific config object"""

        config = (c for c in self.__configs if c == key)
        return config

    def getValue(self, config):
        """Return value of specifig config

        input: str
        """

        value = (c.getValue() for c in self.__configs if c == config)
        return value

    def returnConfigs(self):
        """Returns the configuration dictionary

        output: dict
        """

        return {c.getName(): c.getValue() for c in self.getConfigs()}


class Rule():
    """Single key: rule pair"""

    def __init__(self, data):
        self.__key = data[0]
        self.__rules = data[1] or []

    def __repr__(self):
        return f'Rule({self.__key}: {self.__rules})'

    def __str__(self):
        lines = f'{self.__key}\n'
        for i, rule in enumerate(self.__rules):
            if i != 0:
                lines += '\n'
            lines += f'\t#{i} {rule}'
        return lines

    def __eq__(self, other):
        """Allow comparing rule key into string"""

        if isinstance(other, str):
            return self.__key == other
        else:
            return NotImplemented

    def getKey(self):
        """Return key only from data"""

        return self.__key

    def getRules(self):
        """Return the whole rule data"""

        return self.__rules

    def setValue(self, index, value):
        """Change command values

        input: int
        input: str
        """

        if index <= len(self.__rules) - 1:
            self.__rules[index] = value.split()
        else:
            self.__rules.append(value.split())

    def setKey(self, value):
        """Change rule key value

        input: str
        """

        self.__key = value

    def removeRule(self, rule):
        """Remove command value from rule

        input: str | lst
        """

        self.__rules.remove(rule)


class Database():
    """All key: rule pairs"""

    def __init__(self, data):
        self.__rules = list(genObj(Rule, listFromDict(data)))

    def __str__(self):
        lines = ''
        for i, rule in enumerate(self.__rules):
            if i != 0:
                lines += '\n'
            lines += f'#{i} {rule.getKey()}'
            rule = rule.getRules()
            for m, r in enumerate(rule):
                lines += f'\n\t#{m} {r}'
        return lines

    def getKeys(self):
        """Returns all key values from rule objects in database"""

        return (r.getKey() for r in self.__rules)

    def getRules(self):
        """Returns all rule objects from database"""

        return self.__rules

    def returnCommands(self, link, configs):
        """Return matching rules commands with link iserted"""

        keys = tuple(self.getKeys())

        for f in self.__rules:
            if f == fuzzyFromList(link, keys):
                rules = (
                    r.replace('%link', link).split()
                    if '%link' in r else r + [link]
                    for r in f.getRules())
                return rules
        else:
            rule = (
                [r] + [link]
                for c in configs.getValue('default')
                for r in c)
            return rule

    def returnDb(self):
        """Returns input data back as dict

        output: dict
        """

        dictionary = dict(
            zip(self.getKeys(), (r.getRules() for r in self.getRules())))
        return dictionary

    def addRule(self, value):
        """Adds a new empty rule with key value

        input: str
        """

        self.__rules = self.__rules + [Rule([value, ''])]

    def removeRule(self, rule):
        """Removes rule that matches given key value

        input: str
        """

        self.__rules.remove(rule)
