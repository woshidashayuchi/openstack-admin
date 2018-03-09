# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/8 10:20
from common.connect import connection
from common.logs import logging as log
from common.request_result import request_result


class OpenstackDriver(object):

    def __init__(self):
        self.conn = connection()

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
