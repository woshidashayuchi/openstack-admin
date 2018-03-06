# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/6 15:28
from db.compute_db import KeypairDB
from common.connect import connection
from common.logs import logging as log
from common.request_result import request_result
from common.skill import use_time, time_diff


class KeypairManager(object):

    def __init__(self):
        self.db = KeypairDB()
        self.conn = connection()

    def list(self):
        result = []
        try:
            db_result = self.db.keypair_list()
        except Exception, e:
            log.error('get the keypair list(db) error, reason is: %s' % e)
            return request_result(403)

        log.info('get the keypair list(db) result is: %s' % db_result)
        if len(db_result) != 0:
            for keypair in db_result:
                keypair_uuid = keypair[0]
                fingerprint = keypair[1]
                keypair_name = keypair[2]
                private_key = keypair[3]
                public_key = keypair[4]
                create_name = time_diff(keypair[5])
                result.append({'keypair_uuid': keypair_uuid,
                               'fingerprint': fingerprint,
                               'keypair_name': keypair_name,
                               'private_key': private_key,
                               'public_key': public_key,
                               'create_time': create_name})

        return request_result(200, result)

    def create(self, **keypair):
        try:
            op_result = self.conn.compute.create_keypair(**keypair)
        except Exception, e:
            log.error('create the keypair(op) error, reason is: %s' % e)
            return request_result(621)

        log.info('create the keypair result(op) is: %s' % op_result)

        keypair_uuid = op_result.id
        fingerprint = op_result.fingerprint
        keypair_name = op_result.name
        private_key = op_result.private_key
        public_key = op_result.public_key

        try:
            db_result = self.db.keypair_create(keypair_uuid=keypair_uuid,
                                               fingerprint=fingerprint,
                                               keypair_name=keypair_name,
                                               private_key=private_key,
                                               public_key=public_key)
        except Exception, e:
            log.error('create the keypair(db) error, reason is: %s' % e)
            return request_result(401)
        log.info('create the keypair result(db) is: %s' % db_result)

        return request_result(200, op_result.id)


class KeypairRouteManager(object):

    def __init__(self):
        self.db = KeypairDB()
        self.conn = connection()

    def detail(self, keypair_uuid):
        result = dict()
        try:
            db_result = self.db.keypair_detail(keypair_uuid)
        except Exception, e:
            log.error('get the keypair detail(db) error, reason is: %s' % e)
            return request_result(403)

        if len(db_result) != 0:
            for keypair in db_result:
                result['keypair_uuid'] = keypair[0]
                result['fingerprint'] = keypair[1]
                result['keypair_name'] = keypair[2]
                result['private_key'] = keypair[3]
                result['public_key'] = keypair[4]
                result['create_time'] = time_diff(keypair[5])

        return request_result(200, result)

    def delete(self, keypair_uuid):
        try:
            op_result = self.conn.compute.delete_keypair(keypair_uuid)
        except Exception, e:
            log.error('delete the keypair(op) error, reason is: %s' % e)
            return request_result(624)
        log.info('delete the keypair(op) result is: %s' % op_result)
        try:
            db_result = self.db.keypair_delete(keypair_uuid)
        except Exception, e:
            log.error('delete the keypair(db) error, reason is: %s' % e)
            return request_result(404)
        log.info('delete the keypair(db) result is: %s' % db_result)

        return request_result(200, keypair_uuid)

    def update(self, keypair_uuid):
        pass
