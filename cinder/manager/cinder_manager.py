# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
from db.cinder_db import CinderDB
from driver.cinder_driver import CinderDriver
from driver.auth_driver import get_token
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time, parameters_check
import openstack


def connection_admin():
    try:
        conn = openstack.connect(cloud='admin')
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn


def connection():
    try:
        conn = openstack.connect(cloud='demo')
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn


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


class VolumeType(object):

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

        return request_result(200, 'type is creating')

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

        return request_result(200, result)


class VolumeRouteType(object):

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
        return request_result(200, 'delete success')

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

        return request_result(200, result)


class Snapshot(object):

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


class SnapshotRoute(object):

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
