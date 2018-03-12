# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/8 10:20
from common.connect import connection
from common.logs import logging as log
from common import conf
from common.request_result import request_result
import requests
import json


class OpenstackDriver(object):

    def __init__(self):
        self.conn = connection()

    def get_token(self, user_name, password):
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        user_msg = {"auth": {"tenantName": "demo",
                             "passwordCredentials": {"username": user_name,
                                                     "password": password}}}
        try:
            ret = requests.post(url=conf.token_url, json=user_msg,
                                headers=header,
                                timeout=5)
        except Exception, e:
            log.error('get the token error, reason is: %s' % e)
            return request_result(501)
        if ret.status_code != 200:
            return request_result(501)
        log.debug('get the projectID and token(op) result is: %s' % ret.text)
        try:
            token = json.loads(ret.text).get('access').get('token').get('id')
            user_uuid = json.loads(ret.text).get('access').get('user').get(
                'id')
        except Exception, e:
            log.error('get the token from openstack error, reason is: %s' % e)
            return request_result(203)

        result = {'token': token, 'user_uuid': user_uuid}
        return request_result(200, result)

    def volume_create(self, name, size, v_type, description):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.block_storage.\
                create_volume(size=size,
                              name=name,
                              type=v_type,
                              description=description)
        except Exception, e:
            log.error('create the volume(op) error, reason is: %s' % e)
            return request_result(601)

        return request_result(200, op_result.id)

    def volume_delete(self, volume_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.block_storage.delete_volume(volume_uuid)
        except Exception, e:
            log.error('delete the volume(op) error, reason is: %s' % e)
            return request_result(603)

        return request_result(200, op_result)

    def volume_update(self):
        pass
