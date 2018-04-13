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

    def attachment_create(self, server_uuid, volume_uuid, team_uuid,
                          project_uuid, user_uuid):
        log.info('attachment args: server_uuid:%s, volume_uuid: %s' % (
                  server_uuid,
                  volume_uuid))
        op_result = self.op.attachment_create_wait(server_uuid=server_uuid,
                                                   volume_uuid=volume_uuid)
        if op_result.get('status') != 0:
            return op_result

        device = op_result.get('result').get('device')
        attachment_uuid = op_result.get('result').get('attachment_uuid')

        try:
            self.db.attachment_create(attachment_uuid=attachment_uuid,
                                      volume_uuid=volume_uuid,
                                      server_uuid=server_uuid,
                                      device=device,
                                      team_uuid=team_uuid,
                                      project_uuid=project_uuid,
                                      user_uuid=user_uuid)
        except Exception, e:
            log.error('create the attachment(db) error, reason is: %s' % e)
            # rollback
            rollback = self.op.attachment_delete(attachment_uuid, server_uuid)
            log.info('rollback when create attachment failed '
                     'result is: %s' % rollback)
            return request_result(401)

        return request_result(0, {'attachment_uuid': attachment_uuid})

    def attachment_delete(self, volume_uuid):
        try:
            attach_info = self.db.get_attachment_info(volume_uuid)
            if len(attach_info) != 0:
                attachment_uuid = attach_info[0][0]
                server_uuid = attach_info[0][1]
                log.info('get the attachment_uuid from '
                         'db is: %s' % attachment_uuid)
            else:
                log.info('do not need unattach')
                return request_result(0)
        except Exception, e:
            log.error('get the attachment_uuid error, reason is: %s' % e)
            return request_result(403)

        op_result = self.op.attachment_delete_wait(
                         attachment_uuid=attachment_uuid,
                         server_uuid=server_uuid)
        if op_result.get('status') != 0:
            return op_result
        else:
            # 删除数据库记录(需先更新volume conn情况)
            try:
                self.db.attachment_delete(attachment_uuid=attachment_uuid,
                                          conn_to=None)
            except Exception, e:
                log.error('delete the attachment(db) error, reason is: %s' % e)
                rollback = self.op.attachment_create(server_uuid,
                                                     volume_uuid)
                log.info('rollback when delete the attachment error, '
                         'result is: %s' % rollback)
                return request_result(404)

        return request_result(0, {'volume_uuid': volume_uuid})
