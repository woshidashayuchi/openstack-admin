# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/27 10:23
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
from common import conf
import requests
from common.logs import logging as log
from common.request_result import request_result
from openstack_driver import OpenstackDriver


class CinderDriver(object):

    def __init__(self):
        pass

    def update_volume(self, token, up_dict):
        cinder_url = conf.cinder_url + \
                     'volumes/' + \
                     up_dict['volume_uuid']
        parameters_dict = {
                            "volume": {}
                          }

        if 'name' in up_dict.keys():
            parameters_dict['volume']['name'] = up_dict['name']
        elif 'description' in up_dict.keys():
            parameters_dict['volume']['description'] = up_dict['description']
        else:
            return request_result(200, 'should not update')
        headers = {"X-Auth-Token": token}
        try:
            result = requests.put(url=cinder_url,
                                  json=parameters_dict,
                                  headers=headers, timeout=10)
            # result = requests.get(cinder_url+'/metadata', headers=headers)

        except Exception, e:
            log.error('update the volume(op) error, reason is: %s' % e)
            return request_result(602)

        if result.status_code != 200:
            log.error('update the volume result(op) is: %s' % result.text)
            return request_result(602)

        return request_result(200, {'resource_uuid': up_dict['volume_uuid']})

    def update_snapshot(self, token, up_dict):
        cinder_url = conf.cinder_url + \
                     'snapshots/' + \
                     up_dict['snapshot_uuid']
        parameters_dict = {
            "snapshot": {}
        }
        if 'name' in up_dict.keys():
            parameters_dict['snapshot']['name'] = up_dict['name']
        if 'description' in up_dict.keys():
            parameters_dict['snapshot']['description'] = up_dict['description']
        headers = {"X-Auth-Token": token}
        try:
            result = requests.put(url=cinder_url,
                                  json=parameters_dict,
                                  headers=headers, timeout=10)
        except Exception, e:
            log.error('update the snapshot(op) error, reason is: %s' % e)
            return request_result(1002)

        if result.status_code != 200:
            log.error('update the volume result(op) is: %s' % result.text)
            return request_result(1002)

        return request_result(200, {'snapshot_uuid': up_dict['snapshot_uuid']})

# test code
if __name__ == '__main__':
    token = OpenstackDriver.get_token(user_name='demo', password='qwe123')
    log.info('---')
    log.info(token)
    up = CinderDriver()
    param_dict = {'volume_uuid': '2db1362d-a4cb-4cf9-97b5-306e8e5424ed',
                  'name': 'test-for1'}
    result = up.update_volume('gAAAAABapfW_zJw_jql68o1SVt4uFjIAqYnxNbH77PGomJo'
                              'WHN1QxPZ8e4LoGt7pJ2pHQuWOQz9rTCBfkDV44Ix82k7NMX'
                              'VtbMZqtATlpFyMQ91P3ldYVeY0oS6wDMy0TdP8Fxe2xGrr7'
                              'qXy_cCImOYn4PRxMENSR1MQSkeTk7RfGOtxRBCI5k0',
                              param_dict)
    # print result
