# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/7 14:24
from db.cinder_db import CinderDB
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time, parameters_check
from common.connect import connection_admin


class VolumeTypeManager(object):

    def __init__(self):
        self.conn = connection_admin()
        self.db = CinderDB()

    @use_time
    def create(self, name, description, extra_specs):
        try:
            op_result = self.conn.block_storage.\
                create_type(name=name, description=description)
        except Exception, e:
            log.error('create the volume type(op) error, reason is: %s' % e)
            return request_result(901)

        try:
            type_uuid = op_result.id
            db_result = self.db.volume_type_create(type_uuid=type_uuid,
                                                   name=name,
                                                   description=description,
                                                   extra_specs=extra_specs)
        except Exception, e:
            log.error('create the volume type(db) error, reason is: %s' % e)
            return request_result(401)

        log.info('op_result: %s, db_result: %s' % (op_result, db_result))

        return request_result(0, 'type is creating')

    def list(self):
        result = []
        try:
            db_result = self.db.volume_type_list()
        except Exception, e:
            log.error('get the volume_type list(db) error, reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for v_type in db_result:
                type_uuid = v_type[0]
                name = v_type[1]
                description = v_type[2]
                extra_specs = v_type[3]
                is_public = v_type[4]
                create_time = time_diff(v_type[5])
                result.append({'type_uuid': type_uuid,
                               'name': name,
                               'description': description,
                               'extra_specs': extra_specs,
                               'is_public': is_public,
                               'create_time': create_time})

        return request_result(0, result)


class VolumeRouteTypeManager(object):

    def __init__(self):
        self.db = CinderDB()
        self.conn = connection_admin()

    def update(self):
        pass

    def delete(self, type_uuid):
        # op delete
        try:
            op_result = self.conn.block_storage.delete_type(type_uuid)
        except Exception, e:
            log.error('delete the type(op) error, reason is: %s' % e)
            return request_result(903)

        # db delete
        try:
            db_result = self.db.volume_type_delete(type_uuid)
        except Exception, e:
            log.error('delete the type(db) error, reason is: %s' % e)
            return request_result(404)

        log.info('op_result(delete) is: %s, '
                 'db_result(delete) is: %s' % (op_result, db_result))
        return request_result(0, 'delete success')

    def detail(self, type_uuid):
        result = dict()
        try:
            db_result = self.db.volume_type_detail(type_uuid)
        except Exception, e:
            log.error('get the type detail(db) error, reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for v_type in db_result:
                result['type_uuid'] = v_type[0]
                result['name'] = v_type[1]
                result['description'] = v_type[2]
                result['extra_specs'] = v_type[3]
                result['is_public'] = v_type[4]
                result['create_time'] = time_diff(v_type[5])

        return request_result(0, result)
