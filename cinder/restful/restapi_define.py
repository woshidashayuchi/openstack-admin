# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/26 9:17
import json
from flask import request
from flask_restful import Resource
from common.logs import logging as log
from common.request_result import request_result
from common.token_auth import token_auth
from common.parameters import context_data
from manager.cinder_manager import CinderManager, CinderRouteManager
from manager.type_manager import VolumeTypeManager, VolumeRouteTypeManager


# volume
class CinderApi(Resource):
    def __init__(self):
        self.cinder = CinderManager()

    # create a new volume
    def post(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)

            return request_result(201)

        try:
            parameters = json.loads(request.get_data())
        except Exception, e:
            log.error('create the volume(param) error, reason is: %s' % e)
            return request_result(101)
        # context:
        # 在进行manager的相关调度与操作时候，提供权限判断，token提取等功能
        context = context_data(token, "vol_vol_pro_com", "create", source_ip)

        name = parameters.get('name')
        size = parameters.get('size')
        description = parameters.get('description')
        v_type = parameters.get('v_type')
        conn_to = parameters.get('conn_to')
        snapshot_uuid = parameters.get('snapshot_uuid')
        is_use_domain = parameters.get('is_use_domain')
        source_volume_uuid = parameters.get('source_volume_uuid')
        # is_start = parameters.get('is_start')
        # is_secret = parameters.get('is_secret')
        # user_uuid = parameters.get('user_uuid')

        result = self.cinder.\
            volume_create(context=context,
                          name=name,
                          size=size,
                          description=description,
                          v_type=v_type,
                          conn_to=conn_to,
                          snapshot_uuid=snapshot_uuid,
                          is_use_domain=is_use_domain,
                          source_volume_uuid=source_volume_uuid)

        return result

    # get all volumes list
    def get(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        try:
            page_size = int(request.args.get('page_size'))
            page_num = int(request.args.get('page_num'))
        except Exception, e:
            log.error('page_size or page_num error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, "vol_vol_usr_com", "read")
        result = self.cinder.volume_list(context, page_size, page_num)

        return result

    # 批量删除
    # def delete(self):
    #     try:
    #         token = request.headers.get('token')
    #         token_auth(token)
    #         source_ip = request.headers.get('X-Real-IP')
    #         if source_ip is None:
    #             source_ip = request.remote_addr
    #     except Exception, e:
    #         log.error('Token check error, reason=%s' % e)
    #         return request_result(201)
    #     try:
    #         req_logic = int(request.args.get('logic'))
    #         logic = req_logic
    #     except Exception, e:
    #         log.error('get the logic value error')
    #         return request_result(101)
    #     volume_uuid_list = request.get_data().get('volumes_uuid')
    #
    #     context = context_data(token, volume_uuid_list, "update", source_ip)
    #     result = self.cinder.volumes_delete(context, volume_uuid_list,
    #                                         logic=logic)
    #     return result


class CinderRouteApi(Resource):
    def __init__(self):
        self.cinder = CinderRouteManager()

    def put(self, volume_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)

            return request_result(201)

        context = context_data(token, volume_uuid, "update", source_ip)

        try:
            up_dict = json.loads(request.get_data())
        except Exception, e:
            log.error('request parameters(url) error, reason is: %s' % e)
            return request_result(101)

        return self.cinder.volume_update(context, up_dict, volume_uuid)

    def delete(self, volume_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        try:
            req_logic = int(request.args.get('logic'))
            logic = req_logic
        except Exception, e:
            log.error('get the logic value error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, volume_uuid, "delete", source_ip)

        result = self.cinder.volume_delete(context, volume_uuid, logic=logic)
        return result

    def get(self, volume_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        context = context_data(token, volume_uuid, "read")
        result = self.cinder.volume_detail(context, volume_uuid)

        return result


# types
class TypeApi(Resource):
    def __init__(self):
        self.volume_type = VolumeTypeManager()

    def post(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)

            return request_result(201)

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
        try:
            page_size = int(request.args.get('page_size'))
            page_num = int(request.args.get('page_num'))
        except Exception, e:
            log.error('page_size or page_num error, reason is: %s' % e)
            return request_result(101)

        result = self.volume_type.list()
        return result


class TypeRouteApi(Resource):
    def __init__(self):
        self.volume_type = VolumeRouteTypeManager()

    def get(self, type_uuid):
        result = self.volume_type.detail(type_uuid)
        return result

    def delete(self, type_uuid):
        result = self.volume_type.delete(type_uuid)
        return result

    def put(self):
        pass


# snapshot
class SnapshotApi(Resource):
    def __init__(self):
        self.snapshot = CinderManager()

    # snapshot list
    def get(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        try:
            page_size = int(request.args.get('page_size'))
            page_num = int(request.args.get('page_num'))
        except Exception, e:
            log.error('page_size or page_num error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, "vol_snap_usr_com", "read")
        result = self.snapshot.snap_list(context,
                                         page_num=page_num,
                                         page_size=page_size)
        return result

    # create a new snapshot by a volume
    def post(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)

            return request_result(201)

        try:
            param = json.loads(request.get_data())
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        name = param.get('name')
        description = param.get('description')
        metadata = param.get('metadata')
        volume_uuid = param.get('volume_uuid')

        context = context_data(token, 'vol_snap_pro_com', 'create', source_ip)
        result = self.snapshot.snap_create(context=context,
                                           name=name,
                                           description=description,
                                           metadata=metadata,
                                           volume_uuid=volume_uuid)
        return result


class SnapshotRouteApi(Resource):
    def __init__(self):
        self.snapshot = CinderRouteManager()

    # detail
    def get(self, snapshot_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        context = context_data(token, snapshot_uuid, "read")
        result = self.snapshot.snap_detail(context, snapshot_uuid)
        return result

    def delete(self, snapshot_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        context = context_data(token, snapshot_uuid, "delete", source_ip)
        result = self.snapshot.snap_delete(context, snapshot_uuid)
        return result

    def put(self, snapshot_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        try:
            up_dict = json.loads(request.get_data())
        except Exception, e:
            log.error('get the body parameters error, reason is: %s' % e)
            return request_result(101)
        context = context_data(token, snapshot_uuid, "update", source_ip)
        return self.snapshot.snap_update(context, up_dict, snapshot_uuid)


class AttachmentApi(Resource):

    def __init__(self):
        self.attach = CinderManager()

    def post(self):
        try:
            param = json.loads(request.get_data())

        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        server_uuid = param.get('server_uuid')
        volume_uuid = param.get('volume_uuid')
        return self.attach.attachment_create(server_uuid=server_uuid,
                                             volume_uuid=volume_uuid)
