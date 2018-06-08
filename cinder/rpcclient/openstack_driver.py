# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/23 17:27
import sys
sys.path.append(sys.path[0] + '/..')
sys.path.append(sys.path[0] + '/../..')
from common.logs import logging as log
from common import conf
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

    def vm_create(self, availzone_uuid, image_uuid, vm_name, nic_list,
                  flavor_id="2"):
        """
        :param availzone_uuid: 目前亲测方法用的是可用域的名称，id暂不知可否使用
        :param image_uuid: 镜像id
        :param vm_name: 实例名称
        :param nic_list: 网络列表。[{'uuid':'net01-uuid'},{'uuid': 'net02-uuid'}]
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
            self.conn.compute.change_server_password(
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


if __name__ == '__main__':
    op = OpenstackDriver()
    print op.vm_info('f276cd3f-809f-4431-b803-068960f43afd')
