#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>
import os
import sys
sys.path.append(sys.path[0] + '/..')
sys.path.append(sys.path[0] + '/../..')

from common.logs import logging as log
from openstacksdk.openstack import profile
from openstacksdk.openstack import connection
from common.logs import logging as log
from common.code import request_result

class OpenstackDriver(object):

    def __init__(self, auth_url, region, project_name,
                 username, password):

        prof = profile.Profile()
        prof.set_region(profile.Profile.ALL, region)

        self.conn = connection.Connection(
                               profile=prof,
                               user_agent='examples',
                               auth_url=auth_url,
                               project_name=project_name,
                               username=username,
                               password=password)

    # def create_server(self, image_name,
    #                   flavor_name, network_name):

        # image = self.conn.compute.find_image(IMAGE_NAME)
        # flavor = self.conn.compute.find_flavor(FLAVOR_NAME)
        # network = self.conn.network.find_network(NETWORK_NAME)
        # keypair = create_keypair(self.conn)
        #
        # server = self.conn.compute.create_server(
        #               name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,
        #               networks=[{"uuid": network.id}], key_name=keypair.name)
        #
        # result = self.conn.compute.wait_for_server(server)
        #
        # return result

    def create(self, availzone_uuid, image_uuid, vm_name, nic_list,
               security_groups=None, keypair=None, flavor_id='2'):
        '''

        :param availzone_uuid: 目前亲测方法用的是可用域的名称，id暂不知可否使用
        :param image_uuid: 镜像id
        :param vm_name: 实例名称
        :param nic_list: 网络列表。[{'uuid':'net01-uuid'},{'uuid': 'net02-uuid'}]
        :param security_groups [{'name':''},{'name':''}]可选
        :param key_name 可选
        :flavor_id: 规格
        :return: .result为新建实例的object
        '''
        try:
            op_result = self.conn.\
                compute.create_server(name=vm_name,
                                      availability_zone=availzone_uuid,
                                      image_id=image_uuid,  # id
                                      # security_groups=security_groups,
                                      networks=nic_list,
                                      # key_name=keypair,
                                      flavor_id=flavor_id  # str
                                      )
        except Exception, e:
            log.error('create the cloudhost(op) error, reason is: %s' % e)
            return request_result(611)

        return request_result(0, op_result)

    def delete(self, vm_uuid):
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

        return request_result(0, 'removed')


# test-code
if __name__ == '__main__':
    c = OpenstackDriver()
    a = c.create(availzone_uuid='nova',
                 image_uuid='aafad1da-b3e8-4384-ae6a-93829cde4d33',
                 vm_name='test',
                 nic_list=[{'uuid': '65989d42-8827-44c7-a1ed-838321e4941a'}])
    print a
