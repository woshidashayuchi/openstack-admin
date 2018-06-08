# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:58
from common.logs import logging as log
from common.time_log import time_log
from common.request_result import request_result
from manager.network_manager import RpcManager, PortRouteManager, \
     OsInterfaceManager, OsInterfaceRouterManager, PortManager


class NetworkRpcAPIs(object):

    def __init__(self):
        self.rpc_manager = RpcManager()
        self.port_manager = PortRouteManager()
        self.os_manager = OsInterfaceManager()
        self.os_router_manager = OsInterfaceRouterManager()
        self.port = PortManager()

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
    def vnic_info(self, context, port_uuid):
        try:
            result = self.port_manager.port_detail(context,
                                                   port_uuid)
            log.info('>>>>>result is: %s' % result)
            result = result.get('result')
            mac_address = result.get('mac_address')
            ip_address = result.get('ip_address')
            result.pop('mac_address')
            result.pop('port_uuid')
            result.pop('ip_address')
            result['vnic_mac'] = mac_address
            result['vnic_uuid'] = port_uuid
            result['vnic_ip'] = ip_address
            log.info('>>>>>>>result1 is: %s' % result)
        except Exception, e:
            log.error('get the network detail(RPC) error, reason is: %s' % e)
            return request_result(999)

        return request_result(0, result)

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

    @time_log
    def os_port_add(self, context, parameters):
        try:
            result = self.port.os_port_create(context, parameters)
        except Exception, e:
            log.error('add the port to network error, reason is: %s' % e)
            return request_result(999)

        return result

    @time_log
    def os_port_delete(self, context, parameters):
        try:
            result = self.port_manager.os_port_delete(context, parameters)
        except Exception, e:
            log.error('delete the port error, reason is: %s' % e)
            return request_result(999)
        return result
