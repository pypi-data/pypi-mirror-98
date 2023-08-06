#! /usr/bin/env python3


import argparse

from . import tools
from . import pasterfu
from . import constants
from . fileoperator import FileOperator


def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--version', help='show version', action='store_true')
    parser.add_argument('-l', '--link', help='open link')
    parser.add_argument(
        '-c', '--configs', help='show configurations', action='store_true')
    parser.add_argument(
        '-d', '--db', help='show database', action='store_true')
    parser.add_argument(
        '-e', '--edit', help='edit #IDx#ID, user with database or configs')
    parser.add_argument(
        '-i', '--input-value', help='new input value for database or configs')
    args = parser.parse_args()
    return args


def arguments():
    args = argParser()

    if args.version:
        print(constants.__version__)
    elif args.link:
        pasterfu.main(in_val=args.link)
    elif args.configs:
        configs_file = FileOperator(constants.CONFIGS)
        configs = tools.Configuration(configs_file.loadFile())
        if args.edit and args.input_value:
            confs = configs.getConfigs()
            y, x = tools.cordinateTuple(args.edit)
            if y is None:
                y = 0

            row = min(len(confs) - 1, y)
            confs[row].setValue(args.input_value)
            print(str(configs))
            if tools.yesNo(ask='Do you want to save the changes? y/n\n'):
                configs_file.saveFile(configs.returnConfigs())
        else:
            print(str(configs))
    elif args.db:
        db_file = FileOperator(constants.DB)
        db = tools.Database(db_file.loadFile())
        if args.edit:
            y, x = tools.cordinateTuple(args.edit)
            if y is None and x is None:
                return
            elif y is None:
                y = 0

            row = min(len(db.getRules()), y)
            if row == len(db.getRules()) and args.input_value:
                db.addRule(args.input_value)
                rule = db.getRules()[row]
            elif x is not None:
                rule = db.getRules()[row]
                col = min(len(rule.getRules()), x)
                if row < len(db.getRules()) and not args.input_value:
                    command = rule.getRules()[col]
                    print(f'Remove command? {command}')
                    rule.removeRule(command)
                else:
                    rule.setValue(col, args.input_value)
            elif row < len(db.getRules()) and not args.input_value:
                rule = db.getRules()[row]
                print('Remove Rule?')
                db.removeRule(rule)
            elif args.input_value:
                rule = db.getRules()[row]
                rule.setKey(args.input_value)
            else:
                print(str(db))
                return
            print(str(rule))
            if tools.yesNo(ask='Do you want to save the changes? y/n\n'):
                db_file.saveFile(db.returnDb())
        else:
            print(str(db))
    else:
        pasterfu.main()


def main():
    try:
        arguments()
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    main()
