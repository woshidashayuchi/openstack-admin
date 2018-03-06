# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 9:55
from __future__ import unicode_literals
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
from db.db_init import DBInit
from restapi_register import app_run
from common.logs import logging as log
import time


def compute_server():
    while True:
        try:
            app_run()
        except Exception, e:
            log.error('compute server start error, reason is: %s' % e)

        time.sleep(5)


if __name__ == '__main__':
    compute_server()
