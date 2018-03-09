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
import json


class CinderDriver(object):

    def __init__(self):
        pass

    def update_volume(self, token, up_dict):
        cinder_url = conf.cinder_url + \
                     'c5aea850b5f344e5828c103fc9a02b1a/volumes/'+up_dict['volume_uuid']
        parameters_dict = {
                            "volume": {}
                          }

        if 'name' in up_dict.keys():
            parameters_dict['volume']['name'] = up_dict['name']
        if 'description' in up_dict.keys():
            parameters_dict['volume']['description'] = up_dict['description']

        headers = {"User-Agent": "python-keystoneclient", "X-Auth-Token": token}
        try:
            print cinder_url
            print parameters_dict
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

        return request_result(200, 'update success')


# test code
if __name__ == '__main__':

    up = CinderDriver()
    param_dict = {'volume_uuid': 'b438b74f-e994-4889-9be3-0fa9f33dbb8c',
                  'name': 'test-test'}
    result = up.update_volume('gAAAAABalRh69LWV_cl2a1zQ946kW27PWu90uDhvOq_AS9o80Cy8JOD8YiN35MjNhwxeksssCuuvBZwXuL81-4cN7dKXdk3y19ho6Ln5wSgFMq9ovxTD4Y2qCSErvVRo1TobIaK8nb5qSJL_HHMLozzvT1OlTBXgag', param_dict)
    # print result
