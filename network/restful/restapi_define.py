# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:03
import json
from flask_restful import Resource
from flask import request
from common.token_auth import token_auth
from common.logs import logging as log
from common.request_result import request_result
from common.parameters import context_data
from manager.network_manager import NetworkManager, NetworkRouteManager, \
     RouterManager, RouterRouteManager, PortManager, PortRouteManager


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
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            if page_size is None and page_num is None:
                page_size = 1000
                page_num = 1
            else:
                page_size = int(page_size)
                page_num = int(page_num)
        except Exception, e:
            log.error('page_size or page_num error, reason is: %s' % e)
            return request_result(101)

        parameters = {'page_size': page_size, 'page_num': page_num}
        context = context_data(token, "net_net_usr_com", "read")
        return self.network.network_list_manager(context, parameters)


class NetworkRouteApi(Resource):
    def __init__(self):
        self.network = NetworkRouteManager()

    def get(self, network_uuid):
        # detail
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        context = context_data(token, network_uuid, "read")
        return self.network.network_detail_manager(context, network_uuid)

    def put(self, network_uuid):
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
        context = context_data(token, network_uuid, "update", source_ip)
        return self.network.network_update_manager(context,
                                                   network_uuid,
                                                   parameters)

    def delete(self, network_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        context = context_data(token, network_uuid, "delete", source_ip)
        return self.network.network_delete_manager(context, network_uuid)


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
        context = context_data(token, "net_net_usr_com", "read")

        return self.network.subnet_list_manager(context, parameters)


class SubnetRoutApi(Resource):
    def __init__(self):
        self.subnet = NetworkRouteManager()

    def delete(self, subnet_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        # try:
        #     logic = int(request.args.get('logic'))
        #     if logic != 1 and logic != 0:
        #         raise Exception('parameters(logic) error')
        # except Exception, e:
        #     log.error('get the logic value error, reason is: %s' % e)
        #     return request_result(101)

        context = context_data(token, subnet_uuid, "delete", source_ip)
        return self.subnet.subnet_delete_manager(context, subnet_uuid)

    def put(self):
        pass


class RouterApi(Resource):
    def __init__(self):
        self.router = RouterManager()

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
        return self.router.router_create_manager(context, parameters)

    def get(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            if page_size is None and page_num is None:
                page_size = 1000
                page_num = 1
            else:
                page_size = int(page_size)
                page_num = int(page_num)
        except Exception, e:
            log.error('page_size or page_num error, reason is: %s' % e)
            return request_result(101)

        parameters = {'page_size': page_size, 'page_num': page_num}
        context = context_data(token, "net_net_usr_com", "read")
        return self.router.router_list_manager(context, parameters)


class RouterRouteApi(Resource):
    def __init__(self):
        self.router = RouterRouteManager()

    def get(self, router_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        context = context_data(token, router_uuid, "read")
        return self.router.router_detail_manager(context, router_uuid)

    def put(self, router_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        dict_data = request.get_data()
        up_type = request.args.get('up_type')
        context = context_data(token, router_uuid, "update", source_ip)
        return self.router.router_update_manager(context,
                                                 parameters=dict_data,
                                                 up_type=up_type)

    def delete(self, router_uuid):
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
            logic = int(request.args.get('logic'))
            if logic != 1 and logic != 0:
                raise Exception('parameters(logic) error')
        except Exception, e:
            log.error('get the logic value error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, router_uuid, "delete", source_ip)
        return self.router.router_delete_manager(context,
                                                 router_uuid,
                                                 logic)


class FloatingipApi(Resource):
    def __init__(self):
        self.floating_ip = NetworkManager()

    def get(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        try:
            page_size = request.args.get('page_size')
            page_num = request.args.get('page_num')
            if page_size is None and page_num is None:
                page_size = 1000
                page_num = 1
            else:
                page_size = int(page_size)
                page_num = int(page_num)
        except Exception, e:
            log.error('page_size or page_num error, reason is: %s' % e)
            return request_result(101)

        parameters = {'page_size': page_size, 'page_num': page_num}
        context = context_data(token, "net_net_usr_com", "read")
        return self.floating_ip.floating_ip_list_manager(context, parameters)

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
        return self.floating_ip.floating_ip_create_manager(context, parameters)


class FloatingipRouteApi(Resource):
    def __init__(self):
        self.floating_ip = NetworkRouteManager()

    def get(self, floatingip_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)

        context = context_data(token, floatingip_uuid, "read")
        return self.floating_ip.floating_ip_detail_manager(context,
                                                           floatingip_uuid)

    def delete(self, floatingip_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        logic = request.args.get('logic')
        context = context_data(token, floatingip_uuid, "delete", source_ip)
        return self.floating_ip.floating_ip_del_manager(
                    context=context,
                    floatingip_uuid=floatingip_uuid,
                    logic=logic)

    def put(self, floatingip_uuid):
        pass


class PortApi(Resource):
    def __init__(self):
        self.port = PortManager()

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
        return self.port.port_create(context, parameters)

    def get(self):
        try:
            token = request.headers.get('token')
            token_auth(token)
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        try:
            network_uuid = request.args.get('network_uuid')
            page_num = request.args.get('page_num')
            page_size = request.args.get('page_size')
            if page_size is None and page_num is None:
                page_size = 1000
                page_num = 1
            else:
                page_size = int(page_size)
                page_num = int(page_num)
            if network_uuid is None:
                context = context_data(token, 'net_net_usr_com', 'read')
                return self.port.get_ports(context, page_num, page_size)
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        context = context_data(token, network_uuid, "read")
        return self.port.get_network_ports(context, network_uuid,
                                           page_num, page_size)


class PortRouteApi(Resource):
    def __init__(self):
        self.port = PortRouteManager()

    def delete(self, port_uuid):
        try:
            token = request.headers.get('token')
            token_auth(token)
            source_ip = request.headers.get('X-Real-IP')
            if source_ip is None:
                source_ip = request.remote_addr
        except Exception, e:
            log.error('Token check error, reason=%s' % e)
            return request_result(201)
        context = context_data(token, port_uuid, "delete", source_ip)
        return self.port.port_delete(context, port_uuid)
