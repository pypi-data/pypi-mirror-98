#! /usr/bin/env python3


import os
import logging
import subprocess  # noqa: F401
import webbrowser

import pyperclip  # noqa: F401

from . import tools
from . import constants
from . fileoperator import FileOperator


logger = logging.getLogger(__name__)
logger.setLevel(constants.LOG_LEVEL)

file_handler = logging.FileHandler(constants.MAIN_LOG)
formatter = logging.Formatter(constants.MAIN_FORM)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Starter():
    def __init__(self, link):
        self.__link = link

        self.__db = self.__getDb()
        self.__configs = self.__getConfigs()
        self.__commands = self.__getCommands()

    def __getDb(self):
        db_file = FileOperator(constants.DB)
        db = tools.Database(db_file.loadFile())
        return db

    def __getConfigs(self):
        configs_file = FileOperator(constants.CONFIGS)
        configs = tools.Configuration(configs_file.loadFile())
        return configs

    def __getCommands(self):
        commands = tuple(
            c for c in self.__db.returnCommands(self.__link, self.__configs))
        return commands

    def __loopCommands(self):
        for command in self.__commands:
            if command == ['%copy', self.__link]:
                pyperclip.copy(self.__link)
            elif command:
                subprocess.Popen(command, close_fds=True)
            else:
                webbrowser.open(self.__link)
                return

    def start(self):
        if self.__commands:
            self.__loopCommands()
        else:
            webbrowser.open(self.__link)


def main(in_val=None):
    """Pasterfu main function

    input: link
    """

    logger.info('[INIT] pasterfu started')

    # Read stdin
    if not in_val and os.name == 'posix':
        stdin = tools.readStdin()
        if stdin:
            in_val = list(stdin)[0]

    # Check value
    if not in_val:
        logger.info('[IN_VAL] No input values given, exiting')
        return

    link = tools.regexLink(in_val)
    if not link:
        logger.warning('[REGEX] Given value was not recognized as a link')
        return

    # Run the command
    starter = Starter(link)
    starter.start()


if __name__ == '__main__':
    main()
