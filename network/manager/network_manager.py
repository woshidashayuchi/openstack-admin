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
from router_operate_manager import RouterOperateManager,\
    RouterOperateRouteManager
from floating_ip_operate_manager import FloatingIpOperateManager
from port_operate_manager import PortOperateManager, PortRouteOperateManager
from os_interface_operate_manager import OsInterfaceOperateManager
from rpcclient.status_driver import StatusDriver


class NetworkManager(object):
    def __init__(self):
        self.network_op_manger = NetworkOperateManager()
        self.network_route_manger = NetworkOperateRouteManager()
        self.floating_manager = FloatingIpOperateManager()
        self.status_update = StatusDriver()

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
            is_admin_state_up = parameters.get('is_admin_state_up', 1)
            is_shared = parameters.get('is_shared', 0)
            cidr = parameters.get('cidr')
            ip_version = parameters.get('ip_version', 4)
            gateway_ip = parameters.get('gateway_ip')
            is_dhcp_enabled = parameters.get('is_dhcp_enabled', 1)
            allocation_pools = parameters.get('allocation_pools')
            dns_nameservers = parameters.get('dns_nameservers')
            host_routes = parameters.get('host_routes')
           
            parameter_check(cidr, ptype='ncid', exist='yes')
            parameter_check(is_dhcp_enabled, ptype='n01', exist='yes')
            parameter_check(ip_version, ptype='n04', exist='yes')
            parameter_check(gateway_ip, ptype='nip', exist='no')
            parameter_check(name, ptype='nname')
            parameter_check(description, ptype='ndes', exist='not_essential')
            parameter_check(is_admin_state_up, ptype='n01', exist='no')
            parameter_check(is_shared, ptype='n01', exist='no')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        result = self.network_op_manger.\
            network_create(name=name,
                           description=description,
                           is_admin_state_up=is_admin_state_up,
                           is_shared=is_shared,
                           user_uuid=user_uuid,
                           project_uuid=project_uuid,
                           team_uuid=team_uuid)
        if result.get('status') != 0:
            return result
        network_uuid = result.get('result').get('resource_uuid')
        parameters['network_uuid'] = network_uuid
        # 检查network状态
        network_status = self.network_op_manger.\
            check_network_status(network_uuid)
        if network_status.get('status') != 0:
            log.error('check the network satus is: %s' % network_status)
            return network_status
        # 创建子网
        sub_result = self.network_op_manger.\
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
        log.info('create the subnet result is: %s' % sub_result)
        if sub_result.get('status') != 0:
            # 回滚
            log.info('rollback, delete the network-:%s' % network_uuid)
            self.network_route_manger.network_delete(network_uuid)
            return sub_result
        self.status_update.network_status(network_uuid)
        return result

    @acl_check('network')
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

    @acl_check('network')
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
            parameter_check(description, ptype='ndes', exist='not_essential')
            parameter_check(is_dhcp_enabled, ptype='n01', exist='yes')
            parameter_check(network_uuid, exist='yes')
            parameter_check(ip_version, ptype='n04', exist='yes')
            parameter_check(gateway_ip, ptype='nip', exist='no')
            parameter_check(cidr, ptype='ncid', exist='yes')

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

    def subnet_list_manager(self, context, parameters):
        pass

    @acl_check('network')
    def floating_ip_create_manager(self, context, parameters):
        try:
            parameters = json.loads(parameters)
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            log.info('in manager, token is: %s, source_ip: %s' % (token,
                                                                  source_ip))
            floating_network_id = parameters.get('floating_network_id')

            parameter_check(floating_network_id, exist='yes')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

        return self.floating_manager.floating_ip_create(
                    floating_network_id=floating_network_id,
                    user_uuid=user_uuid,
                    project_uuid=project_uuid,
                    team_uuid=team_uuid)

    @acl_check('network')
    def floating_ip_list_manager(self, context, parameters):
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
        return self.floating_manager.floating_ip_list(
                    user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv, page_size,
                    page_num)


class NetworkRouteManager(object):
    def __init__(self):
        self.network_op_manger = NetworkOperateRouteManager()
        self.floatingip_op_manager = FloatingIpOperateManager()

    @acl_check('network')
    def subnet_delete_manager(self, context, subnet_uuid, logic=0):
        log.debug('delete the subnet, the context is: %s' % context)
        try:
            parameter_check(subnet_uuid, exist='yes')
        except Exception, e:
            log.error('parameters network_uuid error, reason is: %s' % e)
            return request_result(101)
        return self.network_op_manger.subnet_delete(subnet_uuid, logic)

    @acl_check('network')
    def network_detail_manager(self, context, network_uuid):
        log.debug('get the network detail, the context is: %s' % context)
        try:
            parameter_check(network_uuid, exist='yes')
        except Exception, e:
            log.error('parameters network_uuid error, reason is: %s' % e)
            return request_result(101)
        return self.network_op_manger.network_detail(network_uuid)

    @acl_check('network')
    def network_delete_manager(self, context, network_uuid):
        log.debug('delete the network, the context is: %s' % context)
        try:
            parameter_check(network_uuid, exist='yes')
        except Exception, e:
            log.error('parameters network_uuid error, reason is: %s' % e)
            return request_result(101)
        return self.network_op_manger.network_delete(network_uuid)

    @acl_check('network')
    def network_update_manager(self, context, network_uuid, up_dict):
        log.info('update the network, the context is: %s' % context)
        try:
            parameter_check(network_uuid, exist='yes')
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

    @acl_check('network')
    def floating_ip_detail_manager(self, context, floatingip_uuid):
        log.debug('get the floating ip detail, the context is: %s' % context)
        try:
            parameter_check(floatingip_uuid, exist='yes')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

        return self.floatingip_op_manager.floating_ip_detail(floatingip_uuid)

    @acl_check('network')
    def floating_ip_del_manager(self, context, floatingip_uuid, logic=0):
        log.debug('when delete the floating ip, the context is: %s' % context)
        try:
            logic = int(logic)
            parameter_check(floatingip_uuid, exist='yes')
            parameter_check(logic, ptype='n01', exist='yes')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

        return self.floatingip_op_manager.floating_ip_delete(floatingip_uuid,
                                                             logic)


class RouterManager(object):
    def __init__(self):
        self.router_manager = RouterOperateManager()

    @acl_check('network')
    def router_create_manager(self, context, parameters):
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
            is_admin_state_up = parameters.get('is_admin_state_up', 1)
            out_network_uuid = parameters.get('out_network_uuid')

            parameter_check(name, ptype='nname')
            parameter_check(out_network_uuid, exist='no')
            parameter_check(description, ptype='ndes', exist='not_essential')
            parameter_check(is_admin_state_up, ptype='n01', exist='no')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

        return self.router_manager.router_create(
            name=name,
            description=description,
            user_uuid=user_uuid,
            project_uuid=project_uuid,
            team_uuid=team_uuid,
            out_network_uuid=out_network_uuid,
            is_admin_state_up=is_admin_state_up
        )

    @acl_check('network')
    def router_list_manager(self, context, parameters):
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
        return self.router_manager.router_list(user_uuid=user_uuid,
                                               team_uuid=team_uuid,
                                               team_priv=team_priv,
                                               project_uuid=project_uuid,
                                               project_priv=project_priv,
                                               page_size=page_size,
                                               page_num=page_num)


class RouterRouteManager(object):
    def __init__(self):
        self.router = RouterOperateRouteManager()

    @acl_check('network')
    def router_detail_manager(self, context, router_uuid):
        log.debug('get the router detail, context is: %s' % context)
        try:
            parameter_check(router_uuid, exist='yes')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

        return self.router.router_detail(router_uuid)

    @acl_check('network')
    def router_delete_manager(self, context, router_uuid, logic):
        log.debug('delete the router, the context is: %s' % context)
        try:
            parameter_check(router_uuid, exist='yes')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

        return self.router.router_delete(router_uuid, logic=logic)

    # @acl_check('network')
    def router_update_manager(self, context, parameters, up_type=None):
        try:
            parameters = json.loads(parameters)
            router_uuid = context.get('resource_uuid')
            name = parameters.get('name')
            is_admin_state_up = parameters.get('is_admin_state_up')
            network_uuid = parameters.get('network_uuid')
            subnet_uuid = parameters.get('subnet_uuid')
            ip_address = parameters.get('ip_address')
            rtype = parameters.get('rtype')
            # up_type = parameters.get('up_type')
            if name is None and is_admin_state_up not in (0, 1) \
                    and up_type != 'gateway' and up_type != 'interface':
                raise Exception('param name and is_admin_state_up '
                                'can not both be None')
            if up_type not in ('name', 'is_admin_state_up', 'gateway',
                               'interface'):
                raise Exception('update type error, do not '
                                'have this up type')

            if (name is None and up_type == 'name') or \
                    (is_admin_state_up is None and
                     up_type == 'is_admin_state_up'):
                    raise Exception('parameters error, combine chaos')

            parameter_check(router_uuid, exist='yes')
            parameter_check(name, ptype='nname', exist='no')
            parameter_check(is_admin_state_up, ptype='n01', exist='no')
            parameter_check(ip_address, ptype='nip', exist='no')
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)
        if up_type != 'gateway' and up_type != 'interface':
            return self.router.router_update(
                        router_uuid,
                        name=name,
                        is_admin_state_up=is_admin_state_up,
                        up_type=up_type)
        if up_type == 'gateway':
            return self.router.router_gateway_ab(router_uuid,
                                                 network_uuid)
        if up_type == 'interface':
            return self.router.router_interface_ab(router_uuid,
                                                   network_uuid,
                                                   ip_address,
                                                   rtype)


class PortManager(object):
    def __init__(self):
        self.port_manager = PortOperateManager()

    @acl_check('network')
    def port_create(self, context, parameters):
        log.debug('create the port, the context is: %s, '
                  'parameters is: %s' % (context, parameters))
        try:
            parameters = json.loads(parameters)
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')
            log.debug('token: %s, source_ip: %s' % (token, source_ip))

            network_uuid = parameters.get('network_uuid')
            name = parameters.get('name')
            description = parameters.get('description')
            parameter_check(network_uuid, exist='yes')
            parameter_check(name, exist='no')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.port_manager.port_random_create(network_uuid=network_uuid,
                                                    name=name,
                                                    description=description,
                                                    user_uuid=user_uuid,
                                                    project_uuid=project_uuid,
                                                    team_uuid=team_uuid)

    @acl_check('network')
    def os_port_create(self, context, parameters):
        try:
            parameters = json.loads(parameters)
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')
            log.debug('token: %s, source_ip: %s' % (token, source_ip))

            port_uuid = parameters.get('port_uuid')
            vm_uuid = parameters.get('vm_uuid')
            parameter_check(port_uuid, exist='yes')
            parameter_check(vm_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.port_manager.os_port_create(port_uuid,
                                                vm_uuid,
                                                user_uuid,
                                                project_uuid,
                                                team_uuid)

    @acl_check('network')
    def get_network_ports(self, context, network_uuid, page_num, page_size):
        # 权限检测部分，在此只需要对network_uuid进行读权限验证即可
        try:
            parameter_check(network_uuid, exist='yes')

        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)

        return self.port_manager.ports_network_list(network_uuid=network_uuid,
                                                    page_num=page_num,
                                                    page_size=page_size)

    @acl_check('network')
    def get_ports(self, context, page_num, page_size):
        # 获取全部ports列表
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            parameter_check(page_size, ptype='nnum', exist='yes')
            parameter_check(page_num, ptype='nnum', exist='yes')
        except Exception, e:
            log.error('parameters error when get all ports, reason is: %s' % e)
            return request_result(101)

        return self.port_manager.ports_list(user_uuid,
                                            team_uuid,
                                            team_priv,
                                            project_uuid,
                                            project_priv,
                                            page_size,
                                            page_num)


class PortRouteManager(object):
    def __init__(self):
        self.port_manager = PortRouteOperateManager()

    @acl_check('network')
    def port_delete(self, context, port_uuid):
        try:
            parameter_check(port_uuid, exist='yes')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)
        return self.port_manager.port_operate_delete(port_uuid)

    @acl_check('network')
    def port_detail(self, context, port_uuid):
        try:
            parameter_check(port_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, context=%s, '
                      'reason is: %s' % (context, e))
            return request_result(101)

        return self.port_manager.port_operate_detail(port_uuid)

    @acl_check('network')
    def os_port_delete(self, context, parameters):
        log.info('os port delete, the context is: %s' % context)
        try:
            port_uuid = parameters.get('port_uuid')
            parameter_check(port_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.port_manager.os_port_operate_delete(port_uuid)


# RPC MANAGER
class RpcManager(object):
    def __init__(self):
        self.fltip = FloatingIpOperateManager()

    def floatingip_bind(self, context, parameters):
        log.info('bind the floatingip to vm, the context is: %s, '
                 'parameters is: %s' % (context, parameters))

        try:
            vm_uuid = parameters.get('vm_uuid')
            floatingip = parameters.get('floatip')
            fixed_address = parameters.get('fixed_address')
            parameter_check(vm_uuid, exist='yes')
            parameter_check(floatingip, ptype='nip', exist='yes')
            parameter_check(fixed_address, ptype='nip', exist='no')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.fltip.floating_ip_bind(vm_uuid,
                                           floatingip,
                                           fixed_address)

    def floatingip_unbind(self, context, parameters):
        log.info('unbind the floatingip from vm, the context is: %s,'
                 'parameters is: %s' % (context, parameters))
        try:
            token_auth(context['token'])['result']
        except Exception, e:
            log.error('token check error, reason is: %s' % e)
            return request_result(201)
        try:
            floatingip = parameters.get('floatip')
            parameter_check(floatingip, ptype='nip', exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.fltip.floating_ip_unbind(floatingip)


class OsInterfaceManager(object):
    def __init__(self):
        self.os_interface = OsInterfaceOperateManager()

    @acl_check('network')
    def os_interface_add(self, context, parameters):
        log.debug('context is: %s' % context)
        try:
            vm_uuid = parameters.get('vm_uuid')
            port_uuid = parameters.get('port_uuid')
            parameter_check(vm_uuid, exist='yes')
            parameter_check(port_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.os_interface.add_os_interface(vm_uuid=vm_uuid,
                                                  port_uuid=port_uuid)


class OsInterfaceRouterManager(object):
    def __init__(self):
        self.os_interface = OsInterfaceOperateManager()

    @acl_check('network')
    def os_interface_remove(self, context, parameters):
        log.debug(context)
        try:
            port_uuid = parameters.get('port_uuid')
            parameter_check(port_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.os_interface.remove_os_interface(port_uuid)
