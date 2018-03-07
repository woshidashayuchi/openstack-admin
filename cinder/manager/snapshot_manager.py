# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/7 14:29

from db.cinder_db import CinderDB
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time, parameters_check
from common.connect import connection


class SnapshotManager(object):

    def __init__(self):
        self.conn = connection()
        self.db = CinderDB()

    @use_time
    def create(self, name, description, metadata, volume_uuid):
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
                snapshot_create(snapshot_uuid=snapshot_uuid, name=name,
                                description=description, status=status,
                                metadata=metadata, size=size,
                                volume_uuid=volume_uuid, is_forced=is_forced)
        except Exception, e:
            log.error('create the snapshot(db) error, reason is: %s' % e)
            return request_result(401)

        log.info('op_result:%s, db_result: %s' % (op_result, db_result))

        return request_result(200, 'snapshot creating')

    def list(self):
        result = []
        try:
            db_result = self.db.snapshot_list()
        except Exception, e:
            log.error('get the snapshot(db) error, reason is: %s' % e)
            return request_result(403)

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

        return request_result(200, result)


class SnapshotRouteManager(object):

    def __init__(self):
        self.db = CinderDB()
        self.conn = connection()

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

        return request_result(200, result)

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

        return request_result(200, 'snapshot delete success')

    def update(self):
        pass
