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


# test code
@use_time
def test():
    time.sleep(3)



@parameters_check(param_type='test')
def parameters_check_test(b=22, a='ccc',param_dict={}):
    print 'aaa'
    time.sleep(3)

if __name__ == '__main__':
    parameters_check_test(b=33, a='a', param_dict={'c':'c', 'd':'d'})
