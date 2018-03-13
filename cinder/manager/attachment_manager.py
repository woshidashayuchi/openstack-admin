# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/13 17:58
from common.logs import logging as log
from common.request_result import request_result
from driver.openstack_driver import OpenstackDriver
from db.cinder_db import CinderDB


class AttachmentManager(object):
    def __init__(self):
        self.op = OpenstackDriver()
        self.db = CinderDB()

    def attachment_create(self, server_uuid, volume_uuid):
        op_result = self.op.attachment_create(server_uuid=server_uuid,
                                              volume_uuid=volume_uuid)
        if op_result.get('status') != 200:
            return op_result

        device = op_result.get('result').get('device')
        attachment_uuid = op_result.get('result').get('attachment_uuid')

        try:
            self.db.attachment_create(attachment_uuid=attachment_uuid,
                                      volume_uuid=volume_uuid,
                                      server_uuid=server_uuid,
                                      device=device)
        except Exception, e:
            log.error('create the attachment(db) error, reason is: %s' % e)
            return request_result(401)

        return request_result(200, {'attachment_uuid': attachment_uuid})
