# -*- coding: utf8 -*-


import time


def time_stat(func):
    def inner(*args, **kvargs):
        begin = time.time()
        print('Begin: {}'.format(func.__name__))
        res = func(*args, **kvargs)
        print('End: {}, {:.3f}'.format(func.__name__, time.time()-begin))

        return res

    return inner
