from __future__ import absolute_import
from __future__ import print_function

import os
import glob
import json
import time
import pandas
import random
import twstock
import datetime

import pandas as pd

__list__ = ['0050', '0056', '2454']
__data__ = 'data/{id}.json'

class StockBot:
    def __init__(self):
        self.data = {}
        self.load()

    def fetch(self, **kwargs):
        data = {}
        if kwargs['id'] not in self.data.keys():
            self.data[kwargs['id']] = {}

        stock = twstock.stock.Stock(sid=kwargs['id'], initial_fetch=False)
        for x in kwargs['data']:
            print('[fetch] {id}: {year}/{month}'.format(id=kwargs['id'], year=x.year, month=x.month))
            stock.fetch(year=x.year, month=x.month)
            time.sleep(random.randint(30, 50))

            for i in range(0, len(stock.data)):
                data[stock.date[i].strftime('%Y%m%d')] = {
                    'capacity': stock.capacity[i],
                    'turnover': stock.turnover[i],
                    'open': stock.open[i],
                    'high': stock.high[i],
                    'low': stock.low[i],
                    'close': stock.close[i],
                    'change': stock.change[i],
                    'transaction': stock.transaction[i]
                }

            self.data[kwargs['id']].update(data)
            self.dump(id=kwargs['id'])

    def init(self, **kwargs):
        for id in kwargs['id']:
            info = twstock.codes[id]
            start = datetime.datetime.strptime(info.start, '%Y/%m/%d')
            end = datetime.datetime.now()
            period = [start.strftime('%Y/%m'), end.strftime('%Y/%m')]
            data = pd.date_range(*(pd.to_datetime(period) + pd.offsets.MonthEnd()), freq='MS')
            self.fetch(id=id, data=data)

    def update(self, **kwargs):
        today = datetime.datetime.now()
        for id in kwargs['id']:
            if id not in self.data.keys():
                self.init(id=id)
                continue

            '''TODO'''
            exit()

    def load(self):
        files = sorted(glob.glob('data/*.json'))
        for file in files:
            with open(file, 'r') as file:
                self.data.update(json.load(file))

    def dump(self, **kwargs):
        with open(__data__.format(id=kwargs['id']), 'w') as file:
            json.dump({kwargs['id']: self.data[kwargs['id']]}, file)

    def get(self, **kwargs):
        for id in __list__[:1]:
            stock = twstock.stock.Stock(sid=id, initial_fetch=False)
