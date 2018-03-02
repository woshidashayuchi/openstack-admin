# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/26 9:17
import json
from flask import request
from flask_restful import Resource
from common.logs import logging as log
from common.request_result import request_result
from manager.cinder_manager import CinderManager, CinderRouteManager, \
     VolumeType, VolumeRouteType, Snapshot, SnapshotRoute


# volume
class CinderApi(Resource):
    def __init__(self):
        self.cinder = CinderManager()

    # create a new volume
    def post(self):
        try:
            parameters = json.loads(request.get_data())
        except Exception, e:
            log.error('create the volume(param) error, reason is: %s' % e)
            return request_result(101)

        name = parameters.get('name')
        size = parameters.get('size')
        description = parameters.get('description')
        v_type = parameters.get('v_type')
        conn_to = parameters.get('conn_to')
        is_use_domain = parameters.get('is_use_domain')
        is_start = parameters.get('is_start')
        is_secret = parameters.get('is_secret')
        user_uuid = parameters.get('user_uuid')

        result = self.cinder.create(name=name,
                                    size=size,
                                    is_start=is_start,
                                    description=description,
                                    v_type=v_type,
                                    conn_to=conn_to,
                                    is_use_domain=is_use_domain,
                                    is_secret=is_secret,
                                    user_uuid=user_uuid)

        return result

    # get all volumes list
    def get(self):
        user_uuid = request.args.get('user_uuid')
        if user_uuid is None:
            return request_result(101)

        result = self.cinder.list(user_uuid)

        return result


class CinderRouteApi(Resource):
    def __init__(self):
        self.cinder = CinderRouteManager()

    def put(self, volume_uuid):
        try:
            up_dict = json.loads(request.get_data())
        except Exception, e:
            log.error('request parameters(url) error, reason is: %s' % e)
            return request_result(101)

        result = self.cinder.update(up_dict, volume_uuid)
        return result

    def delete(self, volume_uuid):
        result = self.cinder.delete(volume_uuid)
        return result

    def get(self, volume_uuid):
        result = self.cinder.detail(volume_uuid)

        return result


# types
class TypeApi(Resource):
    def __init__(self):
        self.volume_type = VolumeType()

    def post(self):
        try:
            param = json.loads(request.get_data())
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        name = param.get('name')
        description = param.get('description')
        extra_specs = param.get('extra_specs')
        result = self.volume_type.create(name=name, description=description,
                                         extra_specs=extra_specs)
        return result

    def get(self):
        result = self.volume_type.list()
        return result


class TypeRouteApi(Resource):
    def __init__(self):
        self.volume_type = VolumeRouteType()

    def get(self, type_uuid):
        result = self.volume_type.detail(type_uuid)
        return result

    def delete(self, type_uuid):
        result = self.volume_type.delete(type_uuid)
        return result

    def put(self):
        pass


class SnapshotApi(Resource):
    def __init__(self):
        self.snapshot = Snapshot()

    def get(self):
        result = self.snapshot.list()
        return result

    def post(self):
        try:
            param = json.loads(request.get_data())
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        name = param.get('name')
        description = param.get('description')
        metadata = param.get('metadata')
        volume_uuid = param.get('volume_uuid')

        result = self.snapshot.create(name=name, description=description,
                                      metadata=metadata,
                                      volume_uuid=volume_uuid)
        return result


class SnapshotRouteApi(Resource):
    def __init__(self):
        self.snapshot = SnapshotRoute()

    def get(self, snapshot_uuid):
        result = self.snapshot.detail(snapshot_uuid)
        return result

    def delete(self, snapshot_uuid):
        result = self.snapshot.delete(snapshot_uuid)
        return result

    def put(self):
        pass
