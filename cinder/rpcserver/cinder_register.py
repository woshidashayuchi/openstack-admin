# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:56
import cinder_define
from common.logs import logging as log
from common.request_result import request_result
from common.rpc_api import RpcAPI


class RabbitmqResponse(object):

    def __init__(self):
        self.rpc_api = RpcAPI()
        self.rpcapi_define = cinder_define.CinderRpcAPIs()
        self.rpc_add_resource()

    def rpc_add_resource(self):
        self.rpc_api.add_resource('osdisk_cre',
                                  self.rpcapi_define.osdisk_create)

        self.rpc_api.add_resource('clouddisk_cre',
                                  self.rpcapi_define.clouddisk_create)

        self.rpc_api.add_resource('clouddisk_del',
                                  self.rpcapi_define.clouddisk_delete)

        self.rpc_api.add_resource('clouddisk_lis',
                                  self.rpcapi_define.clouddisk_list)

        self.rpc_api.add_resource('clouddisk_inf',
                                  self.rpcapi_define.clouddisk_info)

        self.rpc_api.add_resource('clouddisk_rec',
                                  self.rpcapi_define.clouddisk_recovery)

        self.rpc_api.add_resource('snap_cre',
                                  self.rpcapi_define.disk_snapshot_create)

        self.rpc_api.add_resource('snap_del',
                                  self.rpcapi_define.disk_snapshot_delete)

        self.rpc_api.add_resource('snap_rev',
                                  self.rpcapi_define.disk_snapshot_revert)

        self.rpc_api.add_resource('snap_rev_wait',
                                  self.rpcapi_define.disk_snapshot_revert_wait)

        self.rpc_api.add_resource('attach_cre',
                                  self.rpcapi_define.attachment_create)

        self.rpc_api.add_resource('attach_del',
                                  self.rpcapi_define.attachment_delete)

    def rpc_exec(self, rpc_body):
        try:
            return self.rpc_api.rpcapp_run(rpc_body)
        except Exception, e:
            log.error('RPC Server exec error: %s' % e)
            return request_result(599)
