#! /usr/bin/env python3

import os
import logging
from pathlib import Path


__version__ = '0.8.0'
__author__ = 'obtusescholar'


def resPath(path):
    p = Path.resolve(Path.expanduser(Path(path)))
    p.mkdir(parents=True, exist_ok=True)
    return p


def genInsert(index, listing, insert):
    """Return generator object with inserted value"""

    if index < 0:
        index = len(listing) + index

    for i, item in enumerate(listing):
        if i == index:
            yield insert
            yield item
        else:
            yield item


BASES = {
    'posix': '~/.config/pasterfu/',
    'nt': '~/Documents/pasterfu/'}

BASE = resPath(BASES[os.name])

LOG_LEVEL = logging.WARNING
LOG_FORM = ['[%(asctime)s]', '[%(levelname)s]', '%(message)s']

FO_LOG = BASE / 'pasterfu.log'
FO_FORM = ' '.join(genInsert(-1, LOG_FORM, '[FO]'))

MAIN_LOG = BASE / 'pasterfu.log'
MAIN_FORM = ' '.join(genInsert(-1, LOG_FORM, '[MAIN_LOG]'))

DB = BASE / 'db.json'
CONFIGS = BASE / 'configs.json'
