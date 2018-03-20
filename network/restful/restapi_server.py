# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:03
from __future__ import unicode_literals
import sys
path1 = sys.path[0] + '/..'
sys.path.append(path1)
from restapi_register import app_run
from common.logs import logging as log
from db.db_init import DBInit
import time


def network_server():
    while True:
        try:
            app_run()
        except Exception, e:
            log.error('cinder server start error, reason is: %s' % e)

        time.sleep(7)


if __name__ == '__main__':
    network_server()
