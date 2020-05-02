from __future__ import absolute_import
from __future__ import print_function

import numpy

class Statistics:
    def __init__(self):
        pass

    def kd(self, **kwargs):
        N = 9
        A = 1 / 3
        high = [0] * (N - 1)
        low = [0] * (N - 1)
        rsv = [0] * (N - 1)
        k = [0] * (N - 2) + [50]
        d = [0] * (N - 2) + [50]

        for i in range(N - 1, len(kwargs['close'])):
            low.append(numpy.min(kwargs['low'][max(0, i - N + 1):i + 1]))
            high.append(numpy.max(kwargs['high'][max(0, i - N + 1):i + 1]))

        for i in range(N - 1, len(kwargs['close'])):
            rsv.append((kwargs['close'][i] - low[i]) / (high[i] - low[i]) * 100)
            k.append(A * rsv[i] + (1 - A) * k[i - 1])
            d.append(A * k[i] + (1 - A) * d[i - 1])

        return {
            'k': k,
            'd': d
        }

    def moving_avg(self, **kwargs):
        ret = [kwargs['data'][0]]
        for i in range(1, len(kwargs['data'])):
            ret.append(numpy.mean(kwargs['data'][max(0, i - kwargs['period']):i]))
        return ret

    def ema(self, **kwargs):
        ret = [kwargs['data'][0]]
        for i in range(1, len(kwargs['data'])):
            prev = ret[i - 1] * (kwargs['n'] - 1) / (kwargs['n'] + 1)
            current = kwargs['data'][i] * 2 / (kwargs['n'] + 1)
            ret.append(prev + current)
        return ret

    def dif(self, **kwargs):
        ret = []
        short_term = self.ema(data=kwargs['data'], n=12)
        long_term = self.ema(data=kwargs['data'], n=26)
        for i in range(0, len(short_term)):
            ret.append(short_term[i] - long_term[i])
        return ret

    def macd(self, **kwargs):
        return self.ema(data=self.dif(data=kwargs['data']), n=9)
