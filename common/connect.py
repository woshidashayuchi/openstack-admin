# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/6 15:30
import openstack
from common.logs import logging as log


def connection():
    try:
        conn = openstack.connect(cloud='demo')
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn