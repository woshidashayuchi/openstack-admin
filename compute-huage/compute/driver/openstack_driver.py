#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>
import sys
sys.path.append(sys.path[0] + '/..')
sys.path.append(sys.path[0] + '/../..')
from common.logs import logging as log
from common.code import request_result
from conf import conf
import openstack

def connection():
    try:
        conn = openstack.connect(cloud=conf.conn_cloud)
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn

class OpenstackDriver(object):

    def __init__(self):

        self.conn = connection()

    def create_server(self, availzone_uuid, image_uuid, vm_name, nic_list,
                      security_groups=None, keypair=None):
        '''
        :param availzone_uuid: 目前亲测方法用的是可用域的名称，id暂不知可否使用
        :param image_uuid: 镜像id
        :param vm_name: 实例名称
        :param nic_list: 网络列表。[{'uuid':'net01-uuid'},{'uuid': 'net02-uuid'}]
        :param security_groups [{'name':''},{'name':''}]可选
        :param key_name 可选
        :return: .result为新建实例的object
        '''
        try:
            op_result = self.conn.\
                compute.create_server(name=vm_name,
                                      availability_zone=availzone_uuid,
                                      image_id=image_uuid,
                                      # security_groups=security_groups,
                                      networks=nic_list,
                                      # key_name=keypair,
                                      flavor_id="2"  # str
                                      )
        except Exception, e:
            log.error('create the cloudhost(op) error, reason is: %s' % e)
            return request_result(611)

        return request_result(0, op_result)

    def delete_server(self, vm_uuid):
        '''
        :param cloudhost_uuid: 实例id
        :return: .result是实例id
        '''
        try:
            self.conn.compute.delete_server(vm_uuid)
        except Exception, e:
            log.error('delete the clouhost(op) error, reason is: %s' % e)
            return request_result(613)

        return request_result(0, {'vm_uuid': vm_uuid})


    def vm_boot(self, token, vm_uuid):
        try:
            self.conn.compute.start_server(vm_uuid)
        except Exception, e:
            log.error('boot the cloudhost error, reason is: %s' % e)
            return request_result(612)

        return request_result(0, {'vm_uuid': vm_uuid})

    def vm_shut(self, token, vm_uuid):
        try:
            self.conn.compute.stop_server(vm_uuid)
        except Exception, e:
            log.error('shut the cloudhost error, reason is: %s' % e)
            return request_result(612)
        return request_result(0, {'vm_uuid': vm_uuid})

    def floatip_bind(self, token, vm_uuid, floatip, fixed_address=None):
        try:
           op_result = self.conn.compute.\
                add_floating_ip_to_server(server=vm_uuid,
                                          address=floatip,
                                          fixed_address=fixed_address)
        except Exception, e:
            log.error('add the floating ip to server(op) error, reason is: '
                      '%s' % e)
            return request_result(631)
        return request_result(0, op_result)

    def floatip_unbind(self, token, vm_uuid, floatip):
        try:
            op_result = self.conn.compute.\
                remove_floating_ip_from_server(server=vm_uuid,
                                               address=floatip)
        except Exception, e:
            log.error('remove the floating ip from server(op) error, '
                      'reason is: %s' % e)
            return request_result(632)
        log.debug('unbind floatip result(op) is: %s' % op_result)
        return request_result(0, 'removed')

    def vm_pwd_reset(self, token, server_uuid, new_password):
        try:
            op_result = self.conn.compute.\
                change_server_password(server_uuid, new_password)
        except Exception, e:
            log.error('reset the password of the vm error, reason is: %s' % e)
            return request_result(641)

        log.info('pwd reset the result(op) is %s' % op_result) # None
        return request_result(0, {'server_uuid': server_uuid})


# test-code
if __name__ == '__main__':
    op = OpenstackDriver()
    # 创建vm
    print op.\
        create_server(availzone_uuid='nova',
                      image_uuid='aafad1da-b3e8-4384-ae6a-93829cde4d33',
                      vm_name='test111',
                      nic_list=[{'uuid': '65989d42-8827-44c7-a1ed-838321e4941a'}])

    # 删除vm
    # ret = op.delete_server(vm_uuid='040497a3-7a31-42ad-8d6d-630906a679f2')

    # 修改vm密码
    # op.vm_pwd_reset(token='',
    #                 server_uuid='8db8185a-68d7-4643-ad93-5520bec2ffd4',
    #                 new_password='qwe123')

    # op.vm_boot('', '19a1f791-4c02-4fa9-8d0c-d9f8ad566f55')
    #
    # op.vm_shut('', '19a1f791-4c02-4fa9-8d0c-d9f8ad566f55')
    #
    # op.floatip_bind('', vm_uuid='19a1f791-4c02-4fa9-8d0c-d9f8ad566f55', floatip='172.20.2.8')
    #
    # op.floatip_unbind('', vm_uuid='19a1f791-4c02-4fa9-8d0c-d9f8ad566f55', floatip='172.20.2.8')