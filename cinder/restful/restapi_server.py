# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/24 15:29
from __future__ import unicode_literals
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
reload(sys)
sys.setdefaultencoding('utf-8')
from db.db_init import DBInit
from db.data_init import DataInit
from restapi_register import app_run
from common.logs import logging as log
import time


def cinder_server():
    while True:
        try:
            app_run()
        except Exception, e:
            log.error('cinder server start error, reason is: %s' % e)

        time.sleep(7)


if __name__ == '__main__':
    cinder_server()
