#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

import os
import sys
import time


def env_init():

    work_dir = os.path.dirname(
                  os.path.dirname(
                     os.path.dirname(
                        os.path.abspath(__file__))))

    sys.path.insert(0, work_dir)
    reload(sys)
    sys.setdefaultencoding('utf8')


def server_start(service_name):

    from conf import conf
    from common.logs import logging as log
    from api_register import rest_app_run

    api_host = conf.api_server
    port = conf.compute_port
    debug = conf.api_debug

    while True:
        try:
            log.critical('Starting %s Restful API Server' % (service_name))
            rest_app_run(api_host, port, debug)
        except Exception, e:
            log.error('%s RESTful API Server running error, reason=%s'
                      % (service_name, e))
        time.sleep(10)


if __name__ == "__main__":

    service_name = 'Compute'

    env_init()
    server_start(service_name)
