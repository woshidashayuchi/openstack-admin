# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:42
import json
from common.logs import logging as log
from common.token_auth import token_auth
from common.acl import acl_check
from common.parameters import parameter_check, allocation_pools_conform
from common.request_result import request_result
from network_operate_manager import NetworkOperateManager


class NetworkManager(object):
    def __init__(self):
        self.network_op_manger = NetworkOperateManager()

    @acl_check('network')
    def network_create_manager(self, context, parameters):
        try:
            parameters = json.loads(parameters)
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            name = parameters.get('name')
            description = parameters.get('description')
            is_admin_state_up = parameters.get('is_admin_state_up')
            is_shared = parameters.get('is_shared')

            parameter_check(name, ptype='pnam')

        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.network_op_manger.\
            network_create(name=name,
                           description=description,
                           is_admin_state_up=is_admin_state_up,
                           is_shared=is_shared,
                           user_uuid=user_uuid,
                           project_uuid=project_uuid,
                           team_uuid=team_uuid)

    def network_list_manager(self, context, parameters):
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)
        return self.network_op_manger.network_list(user_uuid,
                                                   team_uuid,
                                                   team_priv,
                                                   project_uuid,
                                                   project_priv,
                                                   page_size,
                                                   page_num)

    def subnet_create_manager(self, context, parameters):
        try:
            parameters = json.loads(parameters)
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            name = parameters.get('name')
            description = parameters.get('description')
            is_dhcp_enabled = parameters.get('is_dhcp_enabled')
            network_uuid = parameters.get('network_uuid')
            ip_version = parameters.get('ip_version')
            gateway_ip = parameters.get('gateway_ip')
            allocation_pools = \
                allocation_pools_conform(parameters.get('allocation_pools'))
            cidr = parameters.get('cidr')
            dns_nameservers = parameters.get('dns_nameservers')
            host_routes = parameters.get('host_routes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        if allocation_pools is None:
            allocation_pools = []
        if dns_nameservers is None:
            dns_nameservers = []
        if host_routes is None:
            host_routes = []

        return self.network_op_manger.\
            subnet_create(name=name,
                          description=description,
                          is_dhcp_enabled=is_dhcp_enabled,
                          network_uuid=network_uuid,
                          ip_version=ip_version,
                          gateway_ip=gateway_ip,
                          allocation_pools=allocation_pools,
                          cidr=cidr,
                          dns_nameservers=dns_nameservers,
                          host_routes=host_routes,
                          user_uuid=user_uuid,
                          project_uuid=project_uuid,
                          team_uuid=team_uuid)


class NetworkRouteManager(object):
    def __init__(self):
        pass
