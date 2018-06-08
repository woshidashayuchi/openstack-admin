# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/6/5 11:54
from common.parameters import rpc_data
from common.logs import logging as log
from common.rabbitmq_client import RabbitmqClient


class StatusDriver(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = "status_cast_api"

    def volume_status(self, volume_uuid):
        context = dict()
        parameters = {'volume_uuid': volume_uuid}
        try:
            rpc_body = rpc_data("volume_status", context, parameters)

            self.rbtmq.rpc_cast_client(self.queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)

    def templet_status(self, templet_uuid):
        context = dict()
        parameters = {'templet_uuid': templet_uuid}
        try:
            rpc_body = rpc_data("templet_status", context, parameters)

            self.rbtmq.rpc_cast_client(self.queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)

    def snapshot_status(self, snapshot_uuid):
        context = dict()
        parameters = {'snapshot_uuid': snapshot_uuid}
        try:
            rpc_body = rpc_data("snapshot_status", context, parameters)

            self.rbtmq.rpc_cast_client(self.queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)

    def floatip_status(self, floatip_uuid):
        context = dict()
        parameters = {'floatip_uuid': floatip_uuid}
        try:
            rpc_body = rpc_data("floatip_status", context, parameters)

            self.rbtmq.rpc_cast_client(self.queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)

    def port_status(self, port_uuid):
        context = dict()
        parameters = {'port_uuid': port_uuid}
        try:
            rpc_body = rpc_data("port_status", context, parameters)

            self.rbtmq.rpc_cast_client(self.queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)


if __name__ == '__main__':
    cd = StatusDriver()
    cd.volume_status('670b07b4-5c38-47fc-91cb-0d63c4472e95')
