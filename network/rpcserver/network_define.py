# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:58
from common.logs import logging as log
from common.time_log import time_log
from common.request_result import request_result
from manager.network_manager import RpcManager, NetworkRouteManager, \
     OsInterfaceManager, OsInterfaceRouterManager


class NetworkRpcAPIs(object):

    def __init__(self):
        self.rpc_manager = RpcManager()
        self.network_manager = NetworkRouteManager()
        self.os_manager = OsInterfaceManager()
        self.os_router_manager = OsInterfaceRouterManager()

    @time_log
    def floatingip_bind(self, context, parameters):
        # context: context_data(token, floatingip_uuid, "update", source_ip)
        try:
            result = self.rpc_manager.floatingip_bind(context, parameters)

        except Exception, e:
            log.error('bind the floatingip to vm(RPC) error, '
                      'reason is: %s' % e)
            return request_result(999)

        return result

    @time_log
    def floatingip_unbind(self, context, parameters):
        # context: context_data(token, floatingip_uuid, "update", source_ip)
        try:
            result = self.rpc_manager.floatingip_unbind(context,
                                                            parameters)
        except Exception, e:
            log.error('unbind the floatingip from vm(RPC) error, '
                      'reason is: %s' % e)
            return request_result(999)

        return result

    @time_log
    def vnic_info(self, context, network_uuid):
        try:
            result = self.network_manager.network_detail_manager(context,
                                                                 network_uuid)
        except Exception, e:
            log.error('get the network detail(RPC) error, reason is: %s' % e)
            return request_result(999)

        return result

    @time_log
    def vnic_attach(self, context, parameters):
        try:
            result = self.os_manager.os_interface_add(context, parameters)
        except Exception, e:
            log.error('attach the os interface error, reason is: %s' % e)
            return request_result(999)

        return result

    @time_log
    def vnic_unattach(self, context, parameters):
        try:
            result = self.os_router_manager.os_interface_remove(context,
                                                                parameters)
        except Exception, e:
            log.error('unattach the os from interface error, '
                      'reason is: %s' % e)
            return request_result(999)

        return result
