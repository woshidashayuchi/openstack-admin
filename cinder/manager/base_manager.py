# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
from __future__ import unicode_literals
import sys
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
'''
    curl -i 'http://127.0.0.1:5000/v2.0/tokens' -X POST -H "Content-Type: application/json" -H "Accept: application/json"  -d '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "demo", "password": "qwe123"}}}'
'''
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
        conn.compute.create_server(name='testhello',
                                   availability_zone='nova',
                                   # instance_num=instance_num,
                                   image_id='aafad1da-b3e8-4384-ae6a-93829cde4d33',
                                   security_groups=[{"name": "default"}],
                                   key_name='testkey',
                                   flavor_id='2',
                                   #project_id='c5aea850b5f344e5828c103fc9a02b1a',
                                  )
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

    # print dir(conn.compute)
    compute = ComputeManager()
    try:
        result = compute.create()
    except Exception, e:
        log.error('error, reason is: %s' % e)
        raise

    print result
