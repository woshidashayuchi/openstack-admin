# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/7 14:29

from db.cinder_db import CinderDB
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time, parameters_check
from common.connect import connection
from driver.openstack_driver import OpenstackDriver
from driver.cinder_driver import CinderDriver


class SnapshotManager(object):

    def __init__(self):
        self.conn = connection()
        self.db = CinderDB()

    def create(self, name, description, metadata, volume_uuid, team_uuid,
               project_uuid, user_uuid):

        """:param name:
        :param description:
        :param metadata: object
        :param volume_uuid:
        :param team_uuid:
        :param project_uuid:
        :param user_uuid:
        :return:"""
        try:
            op_result = self.conn.block_storage.\
                create_snapshot(name=name, description=description,
                                metadata=metadata, volume_id=volume_uuid)
            snapshot_uuid = op_result.id
            status = op_result.status
            metadata = op_result.metadata
            size = op_result.size
            is_forced = op_result.is_forced

        except Exception, e:
            log.error('create the snapshot(op) error, reason is: %s' % e)
            return request_result(1001)

        try:
            db_result = self.db.\
                snapshot_create(snapshot_uuid=snapshot_uuid,
                                name=name,
                                description=description,
                                status=status,
                                metadata=metadata,
                                size=size,
                                volume_uuid=volume_uuid,
                                is_forced=is_forced,
                                user_uuid=user_uuid,
                                project_uuid=project_uuid,
                                team_uuid=team_uuid)
        except Exception, e:
            log.error('create the snapshot(db) error, reason is: %s' % e)
            # rollback
            return request_result(401)

        log.info('op_result:%s, db_result: %s' % (op_result, db_result))

        return request_result(0, {'resource_uuid': snapshot_uuid})

    def list(self, user_uuid, team_uuid, team_priv,
             project_uuid, project_priv, page_size, page_num):
        result = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.snap_list_project(team_uuid,
                                                      project_uuid,
                                                      page_size,
                                                      page_num)
            else:
                db_result = self.db.snap_list(team_uuid,
                                              project_uuid,
                                              user_uuid,
                                              page_size,
                                              page_num)

        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        # try:
        #     db_result = self.db.snapshot_list()
        # except Exception, e:
        #     log.error('get the snapshot(db) error, reason is: %s' % e)
        #     return request_result(403)

        if len(db_result) != 0:
            for snapshot in db_result:
                snapshot_uuid = snapshot[0]
                name = snapshot[1]
                description = snapshot[2]
                status = snapshot[3]
                metadata = snapshot[4]
                size = snapshot[5]
                volume_uuid = snapshot[6]
                is_forced = snapshot[7]
                create_time = time_diff(snapshot[8])
                result.append({'snapshot_uuid': snapshot_uuid,
                               'name': name,
                               'description': description,
                               'status': status,
                               'metadata': metadata,
                               'size': size,
                               'volume_uuid': volume_uuid,
                               'is_forced': is_forced,
                               'create_time': create_time})

        return request_result(0, result)


class SnapshotRouteManager(object):

    def __init__(self):
        self.db = CinderDB()
        self.conn = connection()
        self.op_driver = OpenstackDriver()
        self.cinder = CinderDriver()
        self.snapshot_manager = SnapshotManager()

    def detail(self, snapshot_uuid):
        result = dict()
        try:
            db_result = self.db.snapshot_detail(snapshot_uuid)
        except Exception, e:
            log.error('get the snapshot detail(db) error, reason is: %s' % e)
            return request_result(403)

        if len(db_result) != 0:
            for snapshot in db_result:
                result['snapshot_uuid'] = snapshot[0]
                result['name'] = snapshot[1]
                result['description'] = snapshot[2]
                result['status'] = snapshot[3]
                result['metadata'] = snapshot[4]
                result['size'] = snapshot[5]
                result['volume_uuid'] = snapshot[6]
                result['is_forced'] = snapshot[7]
                result['create_time'] = time_diff(snapshot[8])

        return request_result(0, result)

    def delete(self, snapshot_uuid):
        # op delete
        try:
            op_result = self.conn.block_storage.\
                delete_snapshot(snapshot_uuid)
        except Exception, e:
            log.error('delete the snapshot(op) error, reason is: %s' % e)
            return request_result(1003)

        # db delete
        try:
            db_result = self.db.snapshot_delete(snapshot_uuid)
        except Exception, e:
            log.error('delete the snapshot(db) error, reason is: %s' % e)
            return request_result(404)
        log.info('op_result is: %s, db_result is: %s' % (op_result, db_result))

        return request_result(0, {'resource_uuid': snapshot_uuid})

    def logic_delete(self, snapshot_uuid):
        # op delete
        try:
            op_result = self.conn.block_storage. \
                delete_snapshot(snapshot_uuid)
        except Exception, e:
            log.error('delete the snapshot(op) error, reason is: %s' % e)
            return request_result(1003)

        try:
            db_result = self.db.snapshot_logic_delete(snapshot_uuid)
        except Exception, e:
            log.error('logic delete the snapshot(db) error, reason is: %s' % e)
            return request_result(404)
        log.info('logic delete the snapshot op_result is: %s, '
                 'db_result is: %s' % (op_result, db_result))
        return request_result(0, {'resource_uuid': snapshot_uuid})

    def recovery_msg_ready(self, snapshot_uuid):
        # 数据库查询信息
        result = dict()
        try:
            snapshot_db_detail = self.db.\
                snapshot_recovery_msg_get(snapshot_uuid)
            if len(snapshot_db_detail) == 0:
                log.error('have no message in database of '
                          '%s' % snapshot_uuid)
                return request_result(1001)
            result['name'] = snapshot_db_detail[0][0]
            result['description'] = snapshot_db_detail[0][1]
            result['metadata'] = snapshot_db_detail[0][2]
            result['size'] = snapshot_db_detail[0][3]
            result['volume_uuid'] = snapshot_db_detail[0][4]
            result['user_uuid'] = snapshot_db_detail[0][5]
            result['project_uuid'] = snapshot_db_detail[0][6]
            result['team_uuid'] = snapshot_db_detail[0][7]
        except Exception, e:
            log.error('get the message of snapshot(%s) '
                      'from db error, reason is: %s' % snapshot_uuid)
            raise Exception(e)
        return result

    def update(self, up_dict, snapshot_uuid):

        if up_dict.get('up_type') == 'recovery':
            # 获取信息
            try:
                param = self.recovery_msg_ready(snapshot_uuid)
            except Exception, e:
                log.error('get the message from db error, reason is: %s' % e)
                return request_result(403)

            name = param.get('name')
            description = param.get('description')
            # metadata = param.get('metadata')
            # if metadata == 'None':
            #     metadata = None
            volume_uuid = param.get('volume_uuid')
            user_uuid = param.get('user_uuid')
            project_uuid = param.get('project_uuid')
            team_uuid = param.get('team_uuid')

            # 恢复snapshot
            op_result = self.snapshot_manager.create(name=name,
                                                     description=description,
                                                     volume_uuid=volume_uuid,
                                                     metadata=None,
                                                     team_uuid=team_uuid,
                                                     project_uuid=project_uuid,
                                                     user_uuid=user_uuid)
            if op_result.get('status') != 0:
                return request_result(1001)

            # 删除原来的snapshot及权限信息
            del_snap = self.delete(snapshot_uuid)
            if del_snap.get('status') != 0:
                return del_snap

            return op_result

        else:
            op_token = self.op_driver.get_token('demo', 'qwe123')
            if op_token.get('status') != 0:
                return op_token

            token = op_token.get('result').get('token')
            up_dict['snapshot_uuid'] = snapshot_uuid
            result = self.cinder.update_snapshot(token, up_dict)
            if result.get('status') != 0:
                return result

            # update db
            try:
                db_result = self.db.snapshot_update(up_dict, snapshot_uuid)
            except Exception, e:
                log.error('update the snapshot(db) error, reason is: %s' % e)
                return request_result(402)
            log.debug('update the snapshot(db) result is: %s' % db_result)
            return request_result(0, {'resource_uuid': snapshot_uuid})