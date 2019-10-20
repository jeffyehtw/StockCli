from __future__ import absolute_import
from __future__ import print_function

import sys
import argparse
import datetime

from datetime import timedelta
from tabulate import tabulate
from matplotlib import pyplot

from modules.stockbot import StockBot

stockbot = StockBot()

# constant
__version__ = '1.0'
__description__ = 'A command line tool for stock'
__epilog__ = 'Report bugs to <yehcj.tw@gmail.com>'

class Cli:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=__description__,
            epilog=__epilog__
        )
        parser.add_argument('command', help='command help')
        parser.add_argument(
            '-v', '-V', '--version',
            action='version',
            help='show version of program',
            version='v{}'.format(__version__)
        )
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecongnized command')
            parser.print_help()
            exit()

        getattr(self, args.command)()

    def init(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'id',
            nargs='+',
            help=''
        )
        args = parser.parse_args(sys.argv[2:])
        stockbot.init(id=args.id)

    def update(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'id',
            nargs='+',
            help=''
        )
        args = parser.parse_args(sys.argv[2:])
        stockbot.update(id=args.id)