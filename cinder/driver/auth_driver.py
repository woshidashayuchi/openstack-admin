# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/27 10:54
# import sys
# path1 = sys.path[0] + '/..'
# path2 = sys.path[0] + '/../..'
# sys.path.append(path1)
# sys.path.append(path2)
from common import conf
from common.logs import logging as log
from common.request_result import request_result
import requests
import json


def get_token(user_name, password):
    header = {"Content-Type": "application/json",
              "Accept": "application/json"}
    user_msg = {"auth": {"tenantName": "demo",
                         "passwordCredentials": {"username": user_name,
                                                 "password": password}}}
    try:
        ret = requests.post(url=conf.token_url, json=user_msg, headers=header,
                            timeout=5)
    except Exception, e:
        log.error('get the token error, reason is: %s' % e)
        return request_result(501)
    if ret.status_code != 200:
        return request_result(501)
    log.debug('get the projectID and token(op) result is: %s' % ret.text)
    try:
        token = json.loads(ret.text).get('access').get('token').get('id')
        user_uuid = json.loads(ret.text).get('access').get('user').get('id')
    except Exception, e:
        log.error('get the token from openstack error, reason is: %s' % e)
        return request_result(203)

    result = {'token': token, 'user_uuid': user_uuid}
    return request_result(0, result)


# test code
if __name__ == '__main__':
    result = get_token('demo', 'qwe123')
    print result
