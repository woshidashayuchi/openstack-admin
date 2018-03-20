# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/6 15:30
import openstack
from common.logs import logging as log
from common import conf


def connection():
    try:
        conn = openstack.connect(cloud=conf.conn_cloud)
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn


def connection_admin():
    try:
        conn = openstack.connect(cloud=conf.conn_cloud_admin)
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn
