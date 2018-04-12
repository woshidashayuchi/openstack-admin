# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/23 17:27
import sys
sys.path.append(sys.path[0] + '/..')
sys.path.append(sys.path[0] + '/../..')
from common.logs import logging as log
from common import conf
import openstack
import requests
import json


def connection(user):
    try:
        conn = openstack.connect(cloud=user)
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn


class OpenstackDriver(object):

    def __init__(self):
        self.admin_conn = connection(conf.conn_cloud_admin)
        self.conn = connection(conf.conn_cloud)

    @staticmethod
    def get_token(user_name, password, tenantname):
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        user_msg = {"auth": {"tenantName": tenantname,
                             "passwordCredentials": {"username": user_name,
                                                     "password": password}}}
        try:
            ret = requests.post(url=conf.token_url, json=user_msg,
                                headers=header,
                                timeout=5)
        except Exception, e:
            log.error('get the token error, reason is: %s' % e)
            raise Exception(e)
        if ret.status_code != 200:
            log.error(
                'get token error, reason is status: %s' % ret.status_code)
            raise Exception('get the token status error')
        log.debug('get the projectID and token(op) result is: %s' % ret.text)
        try:
            token = json.loads(ret.text).get('access').get('token').get('id')
            # user_uuid = json.loads(ret.text).get('access').get('user').get(
            #     'id')
        except Exception, e:
            log.error('get the token from openstack error, reason is: %s' % e)
            raise Exception(e)

        return token

    def vm_create(self, availzone_uuid, image_uuid, vm_name, nic_list,
                  flavor_id="2"):
        """
        :param availzone_uuid: 目前亲测方法用的是可用域的名称，id暂不知可否使用
        :param image_uuid: 镜像id
        :param vm_name: 实例名称
        :param nic_list: 网络列表。[{'uuid':'net01-uuid'},{'uuid': 'net02-uuid'}]
                                  [{'port': ''},{'port': ''}]
        :param flavor_id:
        :return: 为新建实例的object

        """
        try:
            op_result = self.conn.compute.create_server(
                name=vm_name,
                availability_zone=availzone_uuid,
                image_id=image_uuid,
                networks=nic_list,
                flavor_id=flavor_id  # str
            )
        except Exception, e:
            log.error('create the cloudhost(op) error, reason is: %s' % e)
            raise Exception(e)

        return op_result

    def vm_info(self, vm_uuid):
        result = dict()
        vm_ip_list = []
        try:
            vm_detail = self.conn.compute.get_server(vm_uuid)
            networks = vm_detail.addresses.keys()
            for network in networks:
                for i in vm_detail.addresses.get(network):
                    vm_ip_list.append(i.get('addr'))
            result['vm_ip_list'] = vm_ip_list
            result['vm_disk_list'] = vm_detail.attached_volumes
            result['vm_nic_list'] = networks
            result['status'] = vm_detail.status
        except Exception, e:
            log.error('get the vm info error, reason is: %s' % e)
            raise Exception(e)

        return result

    def vm_delete(self, vm_uuid):
        """
        :param vm_uuid: 实例id
        :return: None
        """
        try:
            self.conn.compute.delete_server(vm_uuid)
        except Exception, e:
            log.error('delete the clouhost(op) error, reason is: %s' % e)
            raise Exception(e)

    def vm_boot(self, vm_uuid):
        """
        :param vm_uuid:
        :return: None
        """
        try:
            self.conn.compute.start_server(vm_uuid)
        except Exception, e:
            log.error('boot the cloudhost error, reason is: %s' % e)
            raise Exception(e)

    def vm_shut(self, vm_uuid):
        """

        :param vm_uuid:
        :return: None
        """
        try:
            self.conn.compute.stop_server(vm_uuid)
        except Exception, e:
            log.error('shut the cloudhost error, reason is: %s' % e)
            raise Exception(e)

    def add_fixed_ip_to_vm(self, vm_uuid, network_uuid):
        """
        :param vm_uuid:
        :param network_uuid: a network uuid or a port uuid
        :return: None
        """
        try:
            self.conn.compute.add_fixed_ip_to_server(vm_uuid, network_uuid)
        except Exception, e:
            log.error('add fixed ip to vm error, reason is: %s' % e)
            raise Exception(e)

    def remove_fixed_ip_from_vm(self, vm_uuid, ip_address):
        try:
            self.conn.compute.remove_fixed_ip_from_server(vm_uuid, ip_address)
        except Exception, e:
            log.error('remove the fixed ip from vm error, reason is: %s' % e)
            raise Exception(e)

    def floatip_bind(self, vm_uuid, floatip, fixed_address=None):
        """
        :param vm_uuid:
        :param floatip:
        :param fixed_address:
        :return: None
        """
        try:
            self.conn.compute.add_floating_ip_to_server(
                server=vm_uuid,
                address=floatip,
                fixed_address=fixed_address
            )
        except Exception, e:
            log.error('add the floating ip to server(op) error, reason is: '
                      '%s' % e)
            raise Exception(e)

    def floatip_unbind(self, vm_uuid, floatip):
        try:
            self.conn.compute.remove_floating_ip_from_server(
                server=vm_uuid,
                address=floatip
            )
        except Exception, e:
            log.error('remove the floating ip from server(op) error, '
                      'reason is: %s' % e)
            raise Exception(e)

    def vm_pwd_reset(self, vm_uuid, new_password):
        try:
            return self.conn.compute.change_server_password(
                vm_uuid,
                new_password
            )
        except Exception, e:
            log.error('reset the password of the vm error, reason is: %s' % e)
            raise Exception(e)

    def images_list(self):
        result = []
        try:
            images = self.conn.compute.images()
            for image in images:
                result.append({'image_uuid': image.id,
                               'image_name': image.name,
                               'image_size': image.size,
                               'image_status': image.status})
        except Exception, e:
            log.error('get the images list error, reason is: %s' % e)
            raise Exception(e)
        return result

    def image_info(self, image_uuid):
        result = dict()
        try:
            image = self.conn.compute.get_image(image_uuid)
            result['image_uuid'] = image_uuid
            result['image_name'] = image.name
            result['image_size'] = image.size
            result['image_status'] = image.status
        except Exception, e:
            log.error('get the image() info error, reason is: %s' % e)
            raise Exception(e)
        return result

    def flavors_list(self):
        result = []
        try:
            flavors = self.conn.compute.flavors()
            for flavor in flavors:
                result.append({'flavor_uuid': flavor.id,
                               'flavor_disk': flavor.disk,
                               'flavor_vcpus': flavor.vcpus})
        except Exception, e:
            log.error('get the flavors list error, reason is: %s' % e)
            raise Exception(e)

        return result

    def flavor_info(self, flavor_uuid):
        result = dict()
        try:
            flavor = self.conn.compute.get_flavor(flavor_uuid)
            result['flavor_uuid'] = flavor.id
            result['flavor_name'] = flavor.name
            result['flavor_is_public'] = flavor.is_public
            result['flavor_vcpus'] = flavor.vcpus
            result['flavor_ram'] = flavor.ram
            result['flavor_disk'] = flavor.disk
        except Exception, e:
            log.error('get the flavor detail error, reason is: %s' % e)
            raise Exception(e)

        return result

    def vnic_attach(self, vm_uuid, network_uuid):
        try:
            self.conn.compute.add_fixed_ip_to_server(vm_uuid, network_uuid)
        except Exception, e:
            log.error('vnic attach to vm error, reason is: %s' % e)
            raise Exception(e)

    def vnic_unattach(self, vm_uuid, address):
        """
        :param vm_uuid:
        :param address: The fixed IP address to be disassociated
            from the server.
        :return:
        """
        try:
            self.conn.compute.remove_fixed_ip_from_server(vm_uuid, address)
        except Exception, e:
            log.error('un attach the network from vm error, reason is: %s' % e)
            raise Exception(e)

    def flavor_delete(self, flavor_uuid, ignore_missing=True):
        """

        :param flavor_uuid: The value can be either the ID of a flavor
                            or a Flavor instance.
        :param ignore_missing: When set to False ResourceNotFound will be
                               raised when the flavor does not exist. When
                               set to True, no exception will be set when
                               attempting to delete a nonexistent flavor.
        :return: None
        """
        try:
            self.admin_conn.compute.delete_flavor(
                 flavor_uuid,
                 ignore_missing=ignore_missing)
        except Exception, e:
            log.error('delete the flavor(op) error, reason is: %s' % e)
            raise Exception(e)

    def flavor_create(self, name, disk, ram, vcpus, swap=0, is_public=True,
                      ephemeral=0, flavor_uuid=None):
        """
        :param name: The name of this flavor.
        :param disk: Size of the disk this flavor offers. Type: int/GB
        :param ram: The amount of RAM (in MB) this flavor offers. Type: int/MB
        :param vcpus: The number of virtual CPUs this flavor offers. Type: int
        :param swap: Size of the swap partitions./MB
        :param is_public: True if this is a publicly visible flavor.
                          False if this is a private image. Type: bool
        :param ephemeral: Size of the ephemeral data disk attached to
                          this server. Type: int/GB
        :param flavor_uuid:
        :return: flavor object

        """
        if flavor_uuid is None:
            flavor_dict = {
                'flavor': {
                       'name': name,
                       'disk': disk,
                       'ram': ram,
                       'vcpus': vcpus,
                       'swap': swap,
                       'os-flavor-access:is_public': is_public,
                       'OS-FLV-EXT-DATA:ephemeral': ephemeral
                    }
            }
        else:
            flavor_dict = {
                'flavor': {
                    'id': flavor_uuid,
                    'name': name,
                    'disk': disk,
                    'ram': ram,
                    'vcpus': vcpus,
                    'swap': swap,
                    'os-flavor-access:is_public': is_public,
                    'OS-FLV-EXT-DATA:ephemeral': ephemeral
                }
            }
        try:
            token = self.get_token(
                user_name=conf.op_admin,
                password=conf.op_admin_pass,
                tenantname=conf.admin_tenantName)
            log.info('admin token: %s' % token)
        except Exception, e:
            log.error('get the admin token error, reason is: %s' % e)
            raise Exception(e)

        url = conf.compute_url + 'flavors'
        headers = {"X-Auth-Token": token}
        try:
            op_result = requests.post(url,
                                      json=flavor_dict,
                                      headers=headers,
                                      timeout=30)
        except Exception, e:
            log.error('create the flavor error, reason is: %s' % e)
            raise Exception(e)

        if op_result.status_code != 200:
            log.error('create the flavor result is: %s' % op_result.text)
            raise Exception('error: the http request status is not 200')

        return op_result.text

    def flavor_update(self, flavor_uuid, name=None, disk=None, ram=None,
                      vcpus=None, swap=0, is_public=True, ephemeral=0):
        """

        :param flavor_uuid:
        :param name:
        :param disk:
        :param ram:
        :param vcpus:
        :param swap:
        :param is_public:
        :param ephemeral:
        :return:
        """

        new_flavor = dict()
        if name is not None:
            new_flavor['name'] = name
        if disk is not None:
            new_flavor['disk'] = disk
        if ram is not None:
            new_flavor['ram'] = ram
        if vcpus is not None:
            new_flavor['vcpus'] = vcpus
        if swap is not None:
            new_flavor['swap'] = swap
        if is_public is not None:
            new_flavor['os-flavor-access:is_public'] = is_public
        if ephemeral is not None:
            new_flavor['OS-FLV-EXT-DATA:ephemeral'] = ephemeral

        # get the old detail
        try:
            flavor_detail = self.conn.compute.get_flavor(flavor_uuid)
            old_flavor = {
                'name': flavor_detail.name,
                'disk': flavor_detail.disk,
                'ram': flavor_detail.ram,
                'vcpus': flavor_detail.vcpus,
                'swap': flavor_detail.swap,
                'os-flavor-access:is_public': flavor_detail.is_public,
                'OS-FLV-EXT-DATA:ephemeral': flavor_detail.ephemeral
            }
        except Exception, e:
            log.error('get the detail of flavor error, reason is: %s' % e)
            raise Exception(e)

        if name == flavor_detail.name and disk == flavor_detail.disk and \
           ram == flavor_detail.ram and vcpus == flavor_detail.vcpus and \
           swap == flavor_detail.swap and \
           is_public == flavor_detail.is_public and \
           ephemeral == flavor_detail.ephemeral:

            return

        old_flavor.update(new_flavor)
        old_flavor['id'] = flavor_uuid

        # get the request token
        try:
            token = self.get_token(
                user_name=conf.op_admin,
                password=conf.op_admin_pass,
                tenantname=conf.admin_tenantName)
            log.info('admin token: %s' % token)
        except Exception, e:
            log.error('get the admin token error, reason is: %s' % e)

            raise Exception(e)

        # delete the old flavor
        try:
            self.flavor_delete(flavor_uuid, ignore_missing=False)
        except Exception, e:
            log.error('delete the old flavor error, reason is: %s' % e)
            raise Exception(e)

        flavor_dict = {
            'flavor':
                old_flavor
        }

        url = conf.compute_url + 'flavors'
        headers = {"X-Auth-Token": token}
        # create the new flavor
        try:
            op_result = requests.post(url,
                                      json=flavor_dict,
                                      headers=headers,
                                      timeout=20)
        except Exception, e:
            log.error('update the flavor error, reason is: %s' % e)
            # rollback
            self.flavor_create(flavor_uuid=flavor_uuid,
                               name=flavor_detail.name,
                               disk=flavor_detail.disk,
                               ram=flavor_detail.ram,
                               vcpus=flavor_detail.vcpus,
                               swap=flavor_detail.swap,
                               is_public=flavor_detail.is_public,
                               ephemeral=flavor_detail.ephemeral)
            raise Exception(e)

        if op_result.status_code != 200:
            log.error('update the flavor(op) error, '
                      'update result is: %s' % op_result)
            # rollback
            self.flavor_create(flavor_uuid=flavor_uuid,
                               name=flavor_detail.name,
                               disk=flavor_detail.disk,
                               ram=flavor_detail.ram,
                               vcpus=flavor_detail.vcpus,
                               swap=flavor_detail.swap,
                               is_public=flavor_detail.is_public,
                               ephemeral=flavor_detail.ephemeral)
            raise Exception('update status code is not 200')


if __name__ == '__main__':
    op = OpenstackDriver()
    print op.flavor_update('0b1e6496-7fa9-4edd-95fb-9137f9ce6ec3', disk=50)
