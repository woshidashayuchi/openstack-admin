# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:03
from flask_restful import Resource
from flask import request
from common.token_auth import token_auth
from common.logs import logging as log
from common.request_result import request_result
from common.parameters import context_data
from manager.network_manager import NetworkManager


class NetworkApi(Resource):
    def __init__(self):
        self.network = NetworkManager()

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
        parameters = request.get_data()
        context = context_data(token, 'net_net_pro_com', 'create', source_ip)
        return self.network.network_create_manager(context, parameters)

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

        parameters = {'page_size': page_size, 'page_num': page_num}
        context = context_data(token, "vol_vol_usr_com", "read")
        return self.network.network_list_manager(context, parameters)


class NetworkRouteApi(Resource):
    def __init__(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class SubNetApi(Resource):
    def __init__(self):
        self.network = NetworkManager()

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
        parameters = request.get_data()
        context = context_data(token, 'net_net_pro_com', 'create', source_ip)
        return self.network.subnet_create_manager(context, parameters)
