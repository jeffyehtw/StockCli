from __future__ import absolute_import
from __future__ import print_function

import os
import glob
import json
import time
import numpy
import random
import twstock

import pandas as pd
import matplotlib.pyplot as pyplot

from datetime import datetime
from datetime import timedelta
from matplotlib import dates as mdates
from mpl_finance import candlestick_ohlc

from modules.statistics import Statistics

statistics = Statistics()

__data__ = 'data/{id}.json'
__earliest__ = datetime(year=2010, month=1, day=1)

class StockBot:
    def __init__(self):
        self.data = {}
        self.load()

    def fetch(self, **kwargs):
        if kwargs['id'] not in self.data.keys():
            self.data[kwargs['id']] = {}

        data = {}
        stock = twstock.stock.Stock(sid=kwargs['id'], initial_fetch=False)
        for x in kwargs['data']:
            print('[fetch] {id}: {year}/{month}'.format(
                id=kwargs['id'],
                year=x.year,
                month=x.month
            ))

            try:
                stock.fetch(year=x.year, month=x.month)
                time.sleep(random.randint(15, 30))
            except:
                print('[fetch] Connect error')
                exit()

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
            start = datetime.strptime(info.start, '%Y/%m/%d')
            start = max(__earliest__, start)
            end = datetime.now()
            period = [start.strftime('%Y/%m'), end.strftime('%Y/%m')]
            data = pd.date_range(*(pd.to_datetime(period) + pd.offsets.MonthEnd()), freq='MS')
            self.fetch(id=id, data=data)

    def update(self, **kwargs):
        for id in kwargs['id']:
            if id not in self.data.keys():
                self.init(id=[id])
                continue

            fetched = self.data[id].keys()
            fetched = list(set([x[:6] for x in fetched]))

            info = twstock.codes[id]
            start = datetime.strptime(info.start, '%Y/%m/%d')
            start = max(__earliest__, start)
            end = datetime.now()
            period = [start.strftime('%Y/%m'), end.strftime('%Y/%m')]
            data = pd.date_range(*(pd.to_datetime(period) + pd.offsets.MonthEnd()), freq='MS')
            data = [x.strftime('%Y%m') for x in data]

            data = [datetime.strptime(x, '%Y%m') for x in data if x not in fetched]
            data.append(datetime(year=end.year, month=end.month, day=1))

            self.fetch(id=id, data=data)

    def load(self):
        files = sorted(glob.glob('data/*.json'))
        for file in files:
            with open(file, 'r') as file:
                self.data.update(json.load(file))

    def dump(self, **kwargs):
        with open(__data__.format(id=kwargs['id']), 'w') as file:
            json.dump({kwargs['id']: self.data[kwargs['id']]}, file)

    def get(self, **kwargs):
        ret = {}
        history = self.data[kwargs['id']].keys()
        days = pd.date_range(start=kwargs['start'], end=kwargs['end'])
        days = [day.strftime('%Y%m%d') for day in days]
        days = [day for day in days if day in history]
        for day in days:
            if None in self.data[kwargs['id']][day].values():
                continue
            ret[day] = self.data[kwargs['id']][day]
        return ret

    def plot(self, **kwargs):
        for id in kwargs['id']:
            info = twstock.codes[id]
            data = self.get(id=id, start=kwargs['start'], end=kwargs['end'])

            if 'trend' == kwargs['type']:
                history = data.keys()
                dates = [mdates.date2num(datetime.strptime(day, '%Y%m%d')) for day in history]
                opens = [data[day]['open'] for day in history]
                closes = [data[day]['close'] for day in history]
                highs = [data[day]['high'] for day in history]
                lows = [data[day]['low'] for day in history]
                capacities = [data[day]['capacity']/1000 for day in history]

                candles = list(map(list, zip(dates, opens, highs, lows, closes)))
                volumes = list(map(list, zip(dates, opens, highs, lows, closes, capacities)))

                ma_short = statistics.moving_avg(data=closes, period=5)
                ma_medium = statistics.moving_avg(data=closes, period=20)
                ma_long = statistics.moving_avg(data=closes, period=60)

                kd = statistics.kd(data=closes)

                fig = pyplot.figure()
                pyplot.title(id)

                # figure1: candlestick + moving average
                ax1 = pyplot.subplot(3, 1, (1, 2))
                ax1.plot(dates, ma_short, label='Short', color='navy', linewidth=0.8)
                ax1.plot(dates, ma_medium, label='Medium', color='goldenrod', linewidth=0.8)
                ax1.plot(dates, ma_long, label='Long', color='green', linewidth=0.8)
                candlestick_ohlc(
                    ax1,
                    candles,
                    width=1,
                    colorup='r',
                    colordown='g',
                    alpha=0.6
                )
                ax1.get_xaxis().set_visible(False)
                ax1.set_ylabel('Price (TWD)')
                ax1.legend(loc='upper left')
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m'))

                # figure2: capacity + kd
                ax2 = pyplot.subplot(3, 1, 3, sharex=ax1)
                ax2.plot(dates, kd['k'], label='K', color='navy', linewidth=1)
                ax2.plot(dates, kd['d'], label='D', color='goldenrod', linewidth=1)
                ax2.legend(loc='upper left')
                ax2.set_ylabel('Percentage (%)')
                ax3 = ax2.twinx()
                ax3.bar(dates, capacities, width=1)
                ax3.get_yaxis().set_visible(False)

                pyplot.gcf().autofmt_xdate()

                if kwargs['file'] == None:
                    pyplot.show()
                else:
                    pyplot.savefig(kwargs['file'], dpi=300)

            elif 'cdf' == kwargs['type']:
                history = self.data[id].keys()
                period = pd.date_range(start=kwargs['start'], end=kwargs['end'])
                period = [day.strftime('%Y%m%d') for day in period]
                closes = [self.data[id][day]['close'] for day in period if day in history]

                accumulation = [numpy.percentile(closes, i) for i in range(0, 100)]
                pyplot.plot(accumulation, range(0, 100))
                pyplot.title(id)
                pyplot.ylabel('Percentage (%)')
                pyplot.xlabel('Price (TWD)')

                if kwargs['file'] == None:
                    pyplot.show()
                else:
                    pyplot.savefig(kwargs['file'], dpi=300)