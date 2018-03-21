# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:42
import json
from common.logs import logging as log
from common.token_auth import token_auth
from common.acl import acl_check
from common.parameters import parameter_check, allocation_pools_conform
from common.request_result import request_result
from network_operate_manager import NetworkOperateManager, \
    NetworkOperateRouteManager


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
            log.debug('token: %s, source_ip: %s' % (token, source_ip))

            name = parameters.get('name')
            description = parameters.get('description')
            is_admin_state_up = parameters.get('is_admin_state_up')
            is_shared = parameters.get('is_shared')

            parameter_check(name, ptype='nname')
            parameter_check(is_admin_state_up, ptype='n01', exist='no')
            parameter_check(is_shared, ptype='n01', exist='no')
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
            parameter_check(page_size, ptype='nnum', exist='yes')
            parameter_check(page_num, ptype='nnum', exist='yes')
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

            log.debug('token: %s, source_ip: %s' % (token, source_ip))

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

            parameter_check(name, ptype='nname', exist='yes')
            parameter_check(is_dhcp_enabled, ptype='n01', exist='yes')
            parameter_check(network_uuid, exist='yes')
            parameter_check(ip_version, ptype='n04', exist='yes')
            parameter_check(gateway_ip, ptype='nip', exist='no')

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
        self.network_op_manger = NetworkOperateRouteManager()

    @acl_check('network')
    def network_detail_manager(self, context, network_uuid):
        log.debug('get the network detail, the context is: %s' % context)
        return self.network_op_manger.network_detail(network_uuid)

    @acl_check('network')
    def network_delete_manager(self, context, network_uuid, logic=0):
        log.debug('delete the network, the context is: %s' % context)
        return self.network_op_manger.network_delete(network_uuid,
                                                     logic)

    @acl_check('network')
    def network_update_manager(self, context, network_uuid, up_dict):
        log.info('update the network, the context is: %s' % context)
        try:
            up_dict = json.loads(up_dict)
            for i in up_dict.keys():
                if i not in ('name', 'is_admin_state_up'):
                    log.error("parameters up the pool('name', "
                              "'is_admin_state_up')")
                    return request_result(101)
        except Exception, e:
            log.error('parameters format error, reason is: %s' % e)
            return request_result(101)

        up_dict['network_uuid'] = network_uuid
        return self.network_op_manger.network_update(up_dict)
