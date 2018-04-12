# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:56
import network_define
from common.logs import logging as log
from common.request_result import request_result
from common.rpc_api import RpcAPI


class RabbitmqResponse(object):

    def __init__(self):
        self.rpc_api = RpcAPI()
        self.rpcapi_define = network_define.NetworkRpcAPIs()
        self.rpc_add_resource()

    def rpc_add_resource(self):
        self.rpc_api.add_resource('floatip_bind',
                                  self.rpcapi_define.floatingip_bind)
        self.rpc_api.add_resource('floatip_unbind',
                                  self.rpcapi_define.floatingip_unbind)
        self.rpc_api.add_resource('vnic_info',
                                  self.rpcapi_define.vnic_info)
        self.rpc_api.add_resource('vnic_attach',
                                  self.rpcapi_define.vnic_attach)
        self.rpc_api.add_resource('vnic_unattach',
                                  self.rpcapi_define.vnic_unattach)

    def rpc_exec(self, rpc_body):
        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % e)
            return request_result(599)
