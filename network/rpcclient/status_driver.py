# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/6/5 11:54
from common.parameters import rpc_data
from common.logs import logging as log
from common.rabbitmq_client import RabbitmqClient


class StatusDriver(object):

    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = "status_cast_all_api"

    def network_status(self, network_uuid):
        context = dict()
        parameters = {'network_uuid': network_uuid}
        try:
            rpc_body = rpc_data("network_status", context, parameters)

            self.rbtmq.rpc_cast_client(self.queue, rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)

    def router_status(self, router_uuid):
        context = dict()
        parameters = {'router_uuid': router_uuid}
        try:
            rpc_body = rpc_data("router_status", context, parameters)

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
    pass
