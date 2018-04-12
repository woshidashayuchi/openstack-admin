# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
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


def jisuan():
    a = []
    for i in range(999):
        a.append(str(i))
    # for j in a:
    #     if '1' in j:
    #         a.remove(j)
    # for m in a:
    #     if '2' in m:
    #         a.remove(m)
    #
    # for n in a:
    #     if '3' in n:
    #         a.remove(n)
    #
    # for k in a:
    #     if '4' in k:
    #         a.remove(k)

    # for x in a:
    #     if '5' in x:
    #         a.remove(x)

    """
    5: 324
    6: 421
    7: 534
    8: 673
    """
    print len(a)

def test_v():
    headers = {'token': '68f50519-39b9-46e4-8568-1e090d547440'}
    for i in range(31):

        import requests
        print requests.get(url='http://localhost:9999/api/v1.0/cinder/volumes?page_size=1&page_num=1',
                     headers=headers).text

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



# test code
if __name__ == '__main__':
    m = BaseManager()
    # # 获取token
    # # ret = b.get_token('admin', 'qwe123')
    # conn = m.connection()
    # # ret = conn.image.images()
    # # for image in ret:
    # #     print(image.name)
    #
    # # print dir(conn)
    # # print '\n'
    # # print dir(conn.volume)
    # print dir(conn.block_storage)
    # print '\n'
    # # print conn.volume.create_volume.__doc__
    #
    # print '1++++++++++++++++++++++'
    # # volume列表： cinder list
    # volume_list = conn.volume.volumes()
    # for volume in volume_list:
    #     print volume.name, '\n'
    #
    # print '2++++++++++++++++++++++'
    # # 单个volume详情： cinder show a7d85458-3c2f-49db-b64c-0f4f0de97768
    # print conn.block_storage.get_volume('a7d85458-3c2f-49db-b64c-0f4f0de97768')
    #
    # print '3++++++++++++++++++++++'
    # print conn.block_storage.create_volume(size=1, name='hello',
    #                                        description='this is also a test')

    print '4++++++++++++++++++++++'
    # print m.db_test()
    test_v()
