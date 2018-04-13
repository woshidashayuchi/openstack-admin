# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/4/12 15:30
from driver.openstack_driver import OpenstackDriver
from common.logs import logging as log
from common.request_result import request_result
from db.network_db import NetworkDB


class OsInterfaceOperateManager(object):
    def __init__(self):
        self.driver = OpenstackDriver()
        self.db = NetworkDB()

    def add_os_interface(self, vm_uuid, port_uuid):
        # check the vnic if is used
        try:
            db_check = self.db.db_port_attach_check(port_uuid)
            if db_check[0][0] is not None:
                return request_result(1065)
        except Exception, e:
            log.error('check the vnic if used(db) error, reason is: %s' % e)
            return request_result(403)
        op_result = self.driver.add_os_interface(vm_uuid=vm_uuid,
                                                 port_uuid=port_uuid)
        if op_result.get('status') != 0:
            return op_result
        try:
            self.db.db_port_vm_attach(port_uuid, vm_uuid)
        except Exception, e:
            log.error('add os interface error, reason is: %s' % e)
            # rollback
            self.driver.remove_os_interface(vm_uuid=vm_uuid,
                                            port_uuid=port_uuid)
            return request_result(402)
        return op_result

    def remove_os_interface(self, port_uuid):
        try:
            db_check = self.db.db_port_attach_check(port_uuid)
            if db_check[0][0] is None:
                return request_result(0)
            vm_uuid = db_check[0][0]
        except Exception, e:
            log.error('check the port if need unattach error, '
                      'reason is: %s' % e)
            return request_result(403)
        op_result = self.driver.remove_os_interface(vm_uuid=vm_uuid,
                                                    port_uuid=port_uuid)
        if op_result.get('status') != 0:
            return op_result
        try:
            self.db.db_port_vm_unattach(port_uuid)
        except Exception, e:
            log.error('remove os interface error, reason is: %s' % e)
            # rollback
            self.driver.add_os_interface(vm_uuid=vm_uuid,
                                         port_uuid=port_uuid)
        return op_result
