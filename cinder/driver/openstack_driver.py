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

    @staticmethod
    def get_token(user_name, password):
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

    def volume_create(self, name, size, v_type, description, snapshot_uuid,
                      source_volume_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            if snapshot_uuid is None and source_volume_uuid is None:
                op_result = self.conn.block_storage.\
                    create_volume(size=size,
                                  name=name,
                                  type=v_type,
                                  description=description)
            elif snapshot_uuid is not None:
                op_result = self.conn.block_storage. \
                    create_volume(name=name,
                                  type=v_type,
                                  description=description,
                                  snapshot_id=snapshot_uuid)
            else:
                op_result = self.conn.block_storage. \
                    create_volume(name=name,
                                  type=v_type,
                                  description=description,
                                  source_volume_id=source_volume_uuid)
        except Exception, e:
            log.error('create the volume(op) error, reason is: %s' % e)
            return request_result(601)
        log.info('create the volume result is: %s' % op_result)
        return request_result(200, {'id': op_result.id,
                                    'size': op_result.size})

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

    def volume_detail(self, volume_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.block_storage.get_volume(volume_uuid)
        except Exception, e:
            log.error('get the volume detail(op) error, reason is: %s' % e)
            return request_result(605)

        log.debug('get the detail of the volume result(op) is: %s' % op_result)
        return request_result(200, op_result.status)

    # 动态挂卷到云机
    def attachment_create(self, server_uuid, volume_uuid):
        if self.conn is False:
            return request_result(701)

        try:
            op_result = self.conn.compute.\
                create_volume_attachment(server=server_uuid,
                                         volume_id=volume_uuid)
        except Exception, e:
            log.error('create the attachment(op) error, reason is: %s' % e)
            return request_result(1010)

        log.info('create the attachment(op) result is: %s' % op_result)

        return request_result(200, {'device': op_result.device,
                                    'attachment_uuid': op_result.id})

    # 卸载卷
    def attachment_delete(self, attachment_uuid, server_uuid):
        if self.conn is False:
            return request_result(701)

        try:
            op_result = self.conn.compute.\
                delete_volume_attachment(volume_attachment=attachment_uuid,
                                         server=server_uuid)
        except Exception, e:
            log.error('delete the attachment(op) error, reason is: %s' % e)
            return request_result(1012)
        log.info('delete the attachment result(op) is: %s' % op_result)
        return request_result(200, {"attachment_uuid": attachment_uuid})


# test code
if __name__ == '__main__':
    op = OpenstackDriver()
    op.attachment_create(server_uuid='8db8185a-68d7-4643-ad93-5520bec2ffd4',
                         volume_uuid='948082a1-f340-4856-823e-621b7cef3af5')
