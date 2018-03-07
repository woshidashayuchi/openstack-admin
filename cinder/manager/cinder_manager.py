# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
from db.cinder_db import CinderDB
from driver.cinder_driver import CinderDriver
from driver.auth_driver import get_token
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time, parameters_check
from common.connect import connection


class CinderManager(object):
    def __init__(self):
        self.conn = connection()
        self.db = CinderDB()

    # size <size>
    #     Volume size in GB(Required unless –snapshot or –source or
    #     –source - replicated is specified)
    # type <volume-type>
    #     Set the type of volume
    #     Select < volume - type > from the available types as shown
    #     by volume type list.
    # image <image>
    #     Use <image> as source of volume(name or ID)
    #     This is commonly used to create a boot volume for a server.
    # snapshot <snapshot>
    #     Use < snapshot > as source of volume(name or ID)
    # source <volume>
    #     Volume to clone(name or ID)
    # source-replicated <replicated-volume>
    #     Replicated volume to clone(name or ID)
    # description <description>
    #     Volume description
    # user <user>
    #     Specify an alternate user(name or ID)
    # project <project>
    #     Specify an alternate project(name or ID)
    # availability-zone <availability-zone>
    #     Create volume in <availability-zone>
    # consistency - group < consistency - group >
    #     Consistency group where the new volume belongs to
    # property < key = value >
    #     Set a property on this volume(repeat option to set
    #     multiple properties)
    # hint < key = value >
    #     Arbitrary scheduler hint key-value pairs to help boot
    #     an instance(repeat option to set multiple hints)
    # multi-attach
    #     Allow volume to be attached more than once(default to False)
    # bootable
    #     Mark volume as bootable
    # non-bootable
    #     Mark volume as non - bootable(default)
    # read-only
    #     Set volume to read-only access mode
    # read-write Set volume to read-write access mode(default)
    # <name> Volume name
    @use_time
    def create(self, name, size, description, v_type, conn_to=None,
               is_use_domain=None, is_start=0, is_secret=0, user_uuid=None):

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

        try:
            db_result = self.db.volume_create(name=name,
                                              size=size,
                                              description=description,
                                              v_type=v_type,
                                              conn_to=None,
                                              is_start=0,
                                              is_use_domain=None,
                                              is_secret=0,
                                              user_uuid=None,
                                              volume_uuid=op_result.id)
        except Exception, e:
            log.error('create the volume(db) error, reason is: %s' % e)
            return request_result(401)

        log.info('op: %s, db: %s' % (op_result.id, db_result))

        return request_result(200, 'volume is creating')

    def list(self, user_uuid):
        result = []
        try:
            db_result = self.db.volume_list(user_uuid)
        except Exception, e:
            log.error('get the volume list(db) error, reason is: %s' % e)
            return request_result(403)

        if len(db_result) != 0:
            for volume in db_result:
                volume_uuid = volume[0]
                user_uuid = volume[1]
                name = volume[2]
                description = volume[3]
                size = volume[4]
                status = volume[5]
                v_type = volume[6]
                conn_to = volume[7]
                is_use_domain = volume[8]
                is_start = volume[9]
                is_secret = volume[10]
                create_time = time_diff(volume[11])
                result.append({'volume_uuid': volume_uuid,
                               'user_uuid': user_uuid,
                               'name': name, 'description': description,
                               'size': size, 'status': status,
                               'type': v_type, 'conn_to': conn_to,
                               'is_use_domain': is_use_domain,
                               'is_start': is_start, 'is_secret': is_secret,
                               'create_time': create_time})

        return request_result(200, result)


class CinderRouteManager(object):

    def __init__(self):
        self.conn = connection()
        self.db = CinderDB()
        self.cinder = CinderDriver()

    # --force
    #     Attempt forced removal of volume(s), regardless of state(defaults to
    #     False)
    # --purge
    #     Remove any snapshots along with volume(s)(defaults to False)
    #     Volume version 2 only
    # <volume>
    #     Volume(s) to delete(name or ID): this use ID
    def delete(self, volume_uuid):
        # delete the volume from op
        try:
            op_result = self.conn.block_storage.delete_volume(volume_uuid)
        except Exception, e:
            log.error('delete the volume(op) error, reason is: %s' % e)
            return request_result(603)

        # delete the volume from database
        try:
            db_result = self.db.volume_delete(volume_uuid)
        except Exception, e:
            log.error('delete the volume(db) error, reason is: %s' % e)
            return request_result(404)

        log.info('op: %s, db: %s' % (op_result, db_result))
        return request_result(200, 'the volume is deleting...')

    def detail(self, volume_uuid):
        result = dict()
        try:
            db_result = self.db.volume_detail(volume_uuid)
        except Exception, e:
            log.error('get the volume detail(db) error, reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for volume in db_result:
                result['volume_uuid'] = volume[0]
                result['user_uuid'] = volume[1]
                result['name'] = volume[2]
                result['description'] = volume[3]
                result['size'] = volume[4]
                result['status'] = volume[5]
                result['type'] = volume[6]
                result['conn_to'] = volume[7]
                result['is_use_domain'] = volume[8]
                result['is_start'] = volume[9]
                result['is_secret'] = volume[10]
                result['create_time'] = time_diff(volume[11])

        return request_result(200, result)

    def update(self, up_dict, volume_uuid):
        # update volume(op)
        token = get_token('demo', 'qwe123')
        if token.get('status') != 200:
            return request_result(801)
        token = token.get('result')
        up_dict['volume_uuid'] = volume_uuid
        result = self.cinder.update_volume(token, up_dict)
        if result.get('status') != 200:
            return result

        # update volume(db)
        try:
            self.db.volume_update(up_dict, volume_uuid)
        except Exception, e:
            log.error('update the database error, reason is: %s' % e)
            return request_result(402)
