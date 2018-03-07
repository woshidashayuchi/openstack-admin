# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

import json

from flask import request
from flask_restful import Resource

from common.logs import logging as log
from common.code import request_result
from common.time_log import time_log
from common.parameters import context_data
from common.token_auth import token_auth

from compute.manager import compute_manager


class CloudHostsApi(Resource):

    def __init__(self):

        self.compute_api = compute_manager.ComputeManagerAPI()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "cmp_cmp_pro_com", "create", source_ip)

        return self.compute_api.cloudhost_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "cmp_cmp_usr_com", "read")

        return self.compute_api.cloudhost_list(context, parameters)


class CloudHostApi(Resource):

    def __init__(self):

        self.compute_api = compute_manager.ComputeManagerAPI()

    @time_log
    def get(self, cloudhost_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, cloudhost_uuid, "read")

        return self.compute_api.cloudhost_info(context)

    @time_log
    def put(self, cloudhost_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            update = request.args.get('update')
            if update in ('cpu', 'mem', 'disk_mount', 'disk_umount',
                          'nic_attach', 'nic_unattach', 'floatip_bind',
                          'password_change'):
                body = request.get_data()
                parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, cloudhost_uuid, "update", source_ip)

        if update == 'power_on':
            return self.compute_api.cloudhost_power_on(context)
        elif update == 'power_off':
            return self.compute_api.cloudhost_power_off(context)
        elif update == 'cpu':
            return self.compute_api.cloudhost_cpu_update(context, parameters)
        elif update == 'mem':
            return self.compute_api.cloudhost_mem_update(context, parameters)
        elif update == 'disk_mount':
            return self.compute_api.cloudhost_disk_mount(context, parameters)
        elif update == 'disk_umount':
            return self.compute_api.cloudhost_disk_umount(context, parameters)
        elif update == 'nic_attach':
            return self.compute_api.cloudhost_nic_attach(context, parameters)
        elif update == 'nic_unattach':
            return self.compute_api.cloudhost_nic_unattach(context, parameters)
        elif update == 'floatip_bind':
            return self.compute_api.cloudhost_floatip_bind(context, parameters)
        elif update == 'floatip_unbind':
            return self.compute_api.cloudhost_floatip_unbind(context)
        elif update == 'password_change':
            return self.compute_api.cloudhost_password_change(context, parameters)
        elif update == 'recovery':
            return self.compute_api.vswitch_reclaim_recovery(context)
        else:
            return request_result(101)

    @time_log
    def delete(self, cloudhost_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, cloudhost_uuid, "delete", source_ip)

        return self.compute_api.cloudhost_delete(context)


class SnapShotsApi(Resource):

    def __init__(self):

        self.compute_api = compute_manager.ComputeManagerAPI()

    @time_log
    def post(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, "cmp_cmp_pro_com", "create", source_ip)

        return self.compute_api.snapshot_create(context, parameters)

    @time_log
    def get(self):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            parameters = {
                             "page_size": page_size,
                             "page_num": page_num
                         }
        except Exception, e:
            log.warning('Parameters error, reason=%s' % (e))

            return request_result(101)

        context = context_data(token, "cmp_cmp_usr_com", "read")

        return self.compute_api.snapshot_list(context, parameters)


class SnapShotApi(Resource):

    def __init__(self):

        self.compute_api = compute_manager.ComputeManagerAPI()

    @time_log
    def get(self, snapshot_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, snapshot_uuid, "read")

        return self.compute_api.snapshot_info(context)

    @time_log
    def put(self, snapshot_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        try:
            body = request.get_data()
            parameters = json.loads(body)
        except Exception, e:
            log.warning('Parameters error, body=%s, reason=%s' % (body, e))

            return request_result(101)

        context = context_data(token, snapshot_uuid, "update", source_ip)

        return self.compute_api.snapshot_restore(context, parameters)

    @time_log
    def delete(self, snapshot_uuid):

        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.warning('Token check error, token=%s, reason=%s' % (token, e))

            return request_result(201)

        context = context_data(token, snapshot_uuid, "delete", source_ip)

        return self.compute_api.snapshot_delete(context)
