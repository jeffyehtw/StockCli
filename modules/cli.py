from __future__ import absolute_import
from __future__ import print_function

import sys
import argparse
import datetime

from matplotlib import pyplot
from datetime import timedelta

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

    def plot(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'id',
            nargs='+',
            help=''
        )
        parser.add_argument(
            '-p', '--period',
            nargs='+',
            required=True,
            help=''
        )
        parser.add_argument(
            '-t', '--type',
            choices={'trend', 'cdf'},
            required=True,
            help=''
        )
        parser.add_argument(
            '-f', '--file',
            help='file'
        )
        args = parser.parse_args(sys.argv[2:])
        stockbot.plot(
            id=args.id,
            start=args.period[0],
            end=args.period[1],
            type=args.type,
            file=args.file
        )

    def dump(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'id',
            nargs='+',
            help=''
        )
        parser.add_argument(
            '-p', '--period',
            nargs='+',
            required=True,
            help=''
        )
        parser.add_argument(
            '-o',
            '--output',
            default='dump.txt',
            help='file'
        )
        parser.add_argument(
            '-t',
            '--type',
            default='json',
            choices={ 'json', 'array' },
            help=''
        )
        args = parser.parse_args(sys.argv[2:])
        stockbot.dump(
            id=args.id,
            start=args.period[0],
            end=args.period[1],
            output=args.output,
            type=args.type
        )
