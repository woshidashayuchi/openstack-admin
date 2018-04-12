# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/8 15:48

from cinder_db import CinderDB
from common.logs import logging as log


class DataInit(object):
    cinder_db = CinderDB()
    try:
        cinder_db.data_init()
    except Exception, e:
        log.error('data init error ,reason is: %s' % e)
        raise Exception('resources_acl init error')
