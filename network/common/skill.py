# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/22 10:56
import time
from logs import logging as log
import inspect


def use_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        time_log = 'method <'+ func.__name__ + '> use time:'+ \
                   str(end_time-start_time) + 's'
        log.info(time_log)
    return wrapper


def time_diff(create_time):
    dates = time.strftime('%Y-%m-%d %H:%M:%S',
                          time.strptime(str(create_time),
                                        "%Y-%m-%d %H:%M:%S"))
    return dates


def parameters_check(param_type=''):
    def _wrapper(func):
        def __in_wrapper(*args, **kwargs):
            # param will be a dict
            param = inspect.getcallargs(func, *args, **kwargs)
            if param_type == 'test':
                if param.get('a') is not None:
                    print 'bad'
            func(*args, **kwargs)
        return __in_wrapper

    return _wrapper
