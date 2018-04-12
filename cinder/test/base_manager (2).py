# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)

import json
import requests
from db.cinder_db import CinderDB
from common.conf import token_url
from common.logs import logging as log
from common.request_result import request_result
import openstack


class BaseManager(object):

    def __init__(self):
        self.db = CinderDB()

    @staticmethod
    def get_token(user_name, password):
        header = {"Content-Type": "application/json"}
        user_msg = {"auth": {"passwordCredentials": {"username": user_name,
                                                     "password": password}}}
        try:
            ret = requests.post(url=token_url, json=user_msg, headers=header,
                                timeout=5)
        except Exception, e:
            log.error('get the token error, reason is: %s' % e)
            return request_result(501)

        token = json.loads(ret.text).get('access').get('user').get('id')
        return request_result(200, token)

    @staticmethod
    def connection():
        conn = openstack.connect(cloud='demo')
        return conn

    def db_test(self):
        return self.db.volumes_list_get('aaa-bbb-ccc-ddd')


class CinderManager(object):
    def __init__(self):
        pass

    def create(self):
        pass


class ComputeManager(object):
    def __init__(self):
        pass

    def create(self):
        conn = BaseManager().connection()
        return conn.compute.create_server(name='testaass',
                                   availability_zone='nova',
                                   # instance_num=instance_num,
                                   image_id='aafad1da-b3e8-4384-ae6a-93829cde4d33',
                                   flavor_id='2',
                                   networks=[{'uuid':'65989d42-8827-44c7-a1ed-838321e4941a'}]
                                   #project_id='c5aea850b5f344e5828c103fc9a02b1a',

                                  )
conn = BaseManager().connection()
def images():

    return conn.compute.images()

def flavors():
    return conn.compute.flavors()


# test code
if __name__ == '__main__':
    m = BaseManager()
    # 获取token
    # ret = b.get_token('admin', 'qwe123')
    conn = m.connection()
    # ret = conn.image.images()
    # for image in ret:
    #     print(image.name)

    # print dir(conn)
    # print '\n'
    # print dir(conn.volume)
    # print dir(conn.block_storage)
    print '\n'
    # print conn.volume.create_volume.__doc__

    print '1++++++++++volume list++++++++++++'
    # # volume列表： cinder list
    # volume_list = conn.volume.volumes()
    # for volume in volume_list:
    #     print volume.name, '\n'

    print '2++++++++++++volume details++++++++'
    # 单个volume详情： cinder show a7d85458-3c2f-49db-b64c-0f4f0de97768
    # print conn.block_storage.get_volume('a7d85458-3c2f-49db-b64c-0f4f0de97768')

    print '3++++++++++create volume++++++++++++'
    # print conn.block_storage.create_volume.__doc__
    # print conn.block_storage.create_volume(size=1, name='hello',
    #                                        description='this is also a test')

    # print '4++++++++++++++++++++++'
    # print m.db_test()


    print '4++++++已建虚拟机列表+++++++'
    # servers = conn.compute.servers()
    # for server in servers:
    #     print server

    # print conn.block_storage.delete_volume.__doc__

    print dir(conn.compute)
    compute = ComputeManager()
    try:
        print compute.create()
    except Exception, e:
        log.error('error, reason is: %s' % e)
        raise

    # print result

    # ret = conn.compute.volume_attachments('4faed492-5285-4c97-a6c4-1d19dd42f635')
    # print ret.next()
    # print conn.block_storage.get_volume('4faed492-5285-4c97-a6c4-1d19dd42f635')

    # print conn.compute.create_volume_attachment.__doc__
    # print dir(conn.network)
    # print ComputeManager().create()
    import time
    # image_uuids = []
    # flavor = []
    # for image in images():
    #     image_uuids.append({'image_uuid': image.id,
    #                         'image_name': image.name,
    #                         'image_size': image.size})
    # print image_uuids
    #
    # flavor_uuids = []
    # for flavor in flavors():
    #     flavor_uuids.append({'flavor_uuid': flavor.id,
    #                            'flavor_disk': flavor.disk,
    #                            'flavor_vcpus': flavor.vcpus,
    #                          'is_public': flavor.is_public})
    # print flavor_uuids
    # print conn.compute.get_image('95de2747-b611-408f-bc72-5dbf72efbfb7')
    # print conn.compute.get_flavor(2)
    # for i in conn.network.agents():
    #     print i
    # print conn.network.add_gateway_to_router('25daa256-ae0b-44cd-8fd4-e429e21cef0a',
    #                                          body={'network_id': '5dac4659-8f4d-4982-8a83-1f06df002afd',
    #                                           'sunbnet_id': 'aa66cb2e-ff13-498c-a173-5b94fd386b07'})

    # print conn.network.add_interface_to_router(router_id='25daa256-ae0b-44cd-8fd4-e429e21cef0a', body={})
    # for i in conn.block_storage.volumes():
    #     print i
    # vm_detail = conn.compute.get_server('c63f0085-d2b9-42dc-8a8a-7d2719981415')
    # result = dict()
    # vm_ip_list = []
    # networks = vm_detail.addresses.keys()
    # for network in networks:
    #     for i in vm_detail.addresses.get(network):
    #         vm_ip_list.append(i.get('addr'))
    # print vm_detail
    # result['vm_ip_list'] = vm_ip_list
    # result['vm_disk_list'] = vm_detail.attached_volumes
    # result['vm_nic_list'] = networks
    # result['status'] = vm_detail.status
    #
    # print result

    # try:
    #     # print conn.compute.add_fixed_ip_to_server('c63f0085-d2b9-42dc-8a8a-7d27199815', '5c65e275-0061-4ae2-8b6e-be89d9749670')
    #     print conn.compute.remove_fixed_ip_from_server('c63f0085-d2b9-42dc-8a8a-7d2719981415', '192.168.10.12')
    # except Exception, e:
    #     log.error('vnic attach to vm error, reason is: %s' % e)
    #     raise Exception(e)

    # conn.network.create_ip(name='name',
    #                        desription='description',
    #                        fixed_ip_address='',
    #                        floating_ip_address = '',
    #                        floating_network_id='',
    #                        )

    # try:
    #     port_id = conn.network.create_port(network_id='4b209466-a722-4551-874b-987b3954fdb8').id
    # except Exception, e:
    #     log.error('error, reason is: %s' % e)
    #     raise Exception(e)
    #
    # conn.network.add_ip_to_port(port_id, '192.168.10.13')
    # conn.network.add_interface_to_router(
    #     '25daa256-ae0b-44cd-8fd4-e429e21cef0a',
    #     '365109ff-6a05-4708-ac22-5508bda04608', port_id)