# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/8 10:20
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
reload(sys)
sys.setdefaultencoding('utf-8')
from common.connect import connection
from common.logs import logging as log
from common.time_log import time_log
from common import conf
from common.skill import use_time
from common.request_result import request_result
import requests
import json
from time import sleep


class OpenstackDriver(object):

    def __init__(self):
        self.conn = connection()

    @staticmethod
    def get_token(user_name, password):
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        user_msg = {"auth": {"tenantName": conf.tenantName,
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
        return request_result(0, result)

    def volume_create(self, name, size, v_type, description, snapshot_uuid,
                      source_volume_uuid, image_uuid):

        if self.conn is False:
            return request_result(701)
        try:

            if snapshot_uuid is not None:
                op_result = self.conn.block_storage. \
                    create_volume(name=name,
                                  type=v_type,
                                  description=description,
                                  snapshot_id=snapshot_uuid)
                return request_result(0, {'id': op_result.id,
                                          'size': op_result.size})
            if source_volume_uuid is not None:
                op_result = self.conn.block_storage. \
                    create_volume(name=name,
                                  type=v_type,
                                  description=description,
                                  source_volume_id=source_volume_uuid)
                return request_result(0, {'id': op_result.id,
                                          'size': op_result.size})

            if image_uuid is not None:
                op_result = self.conn.block_storage.\
                    create_volume(name=name,
                                  type=v_type,
                                  description=description,
                                  image_id=image_uuid,
                                  is_bootable=True)
                return request_result(0, {'id': op_result.id,
                                          'size': op_result.size})


            op_result = self.conn.block_storage.\
                create_volume(size=size,
                              name=name,
                              type=v_type,
                              description=description)

        except Exception, e:
            log.error('create the volume(op) error, reason is: %s' % e)
            return request_result(601)
        log.info('create the volume result is: %s' % op_result)
        return request_result(0, {'id': op_result.id,
                                  'size': op_result.size})

    def volume_delete(self, volume_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.block_storage.delete_volume(volume_uuid)
        except Exception, e:
            log.error('delete the volume(op) error, reason is: %s' % e)
            return request_result(603)

        return request_result(0, op_result)

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
        return request_result(0, op_result.status)

    def volume_list(self):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.block_storage.volumes()
        except Exception, e:
            log.error('SERVICE(clean delete mark):GET VOLUME LIST ERROR, '
                      'REASON IS: %s' % e)
            return request_result(605)
        return request_result(0, op_result)

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

        return request_result(0, {'device': op_result.device,
                                  'attachment_uuid': op_result.id})
    
    # 同步挂载
    @time_log
    def attachment_create_wait(self, server_uuid, volume_uuid):
        result = self.attachment_create(server_uuid, volume_uuid)
        if result.get('status') != 0:
            return result
        timeout = 0
        while True:
            timeout = timeout + 1
            if timeout >= 16:
                # 超时3秒
                return request_result(1010)
            op_status = self.volume_detail(volume_uuid)
            if op_status.get('status') != 0:
                sleep(0.2)
                continue
            else:
                status = op_status.get('result')
                if status == 'in-use':
                    return result
                if status == 'attaching':
                    sleep(0.2)
                    continue
                else:
                    return request_result(1010)

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
        return request_result(0, {"attachment_uuid": attachment_uuid})

    # 同步卸载
    @time_log
    def attachment_delete_wait(self, attachment_uuid, server_uuid):
        result = self.attachment_delete(attachment_uuid, server_uuid)
        if result.get('status') != 0:
            return result
        timeout = 0
        while True:
            timeout = timeout + 1
            if timeout >= 16:
                # 超时3秒
                return request_result(1012)
            log.info('volume detail start execute')
            op_status = self.volume_detail(attachment_uuid)
            log.info('volume detail end execute')
            if op_status.get('status') != 0:
                sleep(0.2)
                continue
            else:
                status = op_status.get('result')
                if status == 'available':
                    return result
                if status == 'detaching':
                    sleep(0.2)
                    continue
                else:
                    return request_result(1012)

    # image about
    def create_image(self, name, file, container_format='bare',
                     disk_format='qcow2'):

        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.image.upload_image(
                container_format=container_format,
                disk_format=disk_format,
                name=name,
                file=file)
        except Exception, e:
            log.error('create the image error, reason is: %s' % e)
            return request_result(1201)

        return request_result(0, op_result)

    def delete_image(self, image_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.image.delete_image(image_uuid)
        except Exception, e:
            log.error('delete the image(op) error, reason is: %s' % e)
            return request_result(1202)

        return request_result(0, op_result)


# test code
if __name__ == '__main__':
    op = OpenstackDriver()
    # try:
    #     dele = op.attachment_delete_wait(
    #             attachment_uuid='3a88bc4a-2464-45a0-af66-a3c4db873fd7',
    #             server_uuid='f276cd3f-809f-4431-b803-068960f43afd')
    # except Exception, e:
    #     log.error('attachment detail error, reason is: %s' % e)
    # op.create_image(name='test1')
