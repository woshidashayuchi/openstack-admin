# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:44
from common.logs import logging as log
from common.request_result import request_result
from driver.openstack_driver import OpenstackDriver
from db.network_db import NetworkDB
from common.skill import time_diff


class NetworkOperateManager(object):

    def __init__(self):
        self.op_driver = OpenstackDriver()
        self.db = NetworkDB()

    def network_create(self, name, description, is_admin_state_up=1,
                       is_shared=0, user_uuid=None, project_uuid=None,
                       team_uuid=None):
        if is_admin_state_up == 1:
            is_admin_state_up_1 = True
        else:
            is_admin_state_up = 0
            is_admin_state_up_1 = False

        if is_shared == 1:
            is_shared_1 = True
        else:
            is_shared = 0
            is_shared_1 = False

        op_result = self.op_driver.\
            network_create(name=name,
                           description=description,
                           is_admin_state_up=is_admin_state_up_1,
                           is_shared=is_shared_1)
        if op_result.get('status') != 200:
            return op_result
        network_uuid = op_result.get('result')

        # insert to db
        try:
            db_result = self.db.\
                db_network_create(network_uuid=network_uuid,
                                  name=name,
                                  description=description,
                                  is_admin_state_up=is_admin_state_up,
                                  is_shared=is_shared,
                                  team_uuid=team_uuid,
                                  project_uuid=project_uuid,
                                  user_uuid=user_uuid)
        except Exception, e:
            log.error('create the network(db) error, reason is: %s' % e)
            return request_result(401)
        log.info('create the network result is: %s, '
                 'db result is: %s' % (op_result, db_result))

        return request_result(200, {'resource_uuid': network_uuid})

    def network_list(self, user_uuid, team_uuid, team_priv,
                     project_uuid, project_priv, page_size, page_num):
        result = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.db_network_list_project(team_uuid,
                                                            project_uuid,
                                                            page_size,
                                                            page_num)
            else:
                db_result = self.db.db_network_list_user(team_uuid,
                                                         project_uuid,
                                                         user_uuid,
                                                         page_size,
                                                         page_num)

        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        if len(db_result) != 0:
            for network in db_result:
                name = network[0]
                subnet_name = network[1]
                cidr = network[2]
                description = network[3]
                is_shared = network[4]
                is_router_external = network[5]
                size = network[6]
                status = network[7]
                is_admin_state_up = network[8]
                create_time = time_diff(network[9])
                result.append({'name': name,
                               'subnet_name_and_cidr': subnet_name+' '+cidr,
                               'description': description,
                               'is_shared': is_shared,
                               'is_router_external': is_router_external,
                               'size': size,
                               'status': status,
                               'is_admin_state_up': is_admin_state_up,
                               'create_time': create_time})

        return request_result(200, result)

    def subnet_create(self, name, description, is_dhcp_enabled, network_uuid,
                      ip_version, gateway_ip, allocation_pools, cidr,
                      dns_nameservers=[], host_routes=[], user_uuid=None,
                      project_uuid=None, team_uuid=None):
        """

        :param name:
        :param description:
        :param is_dhcp_enabled:
        :param network_uuid:
        :param ip_version:
        :param gateway_ip:
        :param allocation_pools: [{"start":"xx","end":"xx"},
                                  {"start":"","end":""}]
        :param cidr:
        :param dns_nameservers:
        :param host_routes:
        :param user_uuid:
        :param project_uuid:
        :param team_uuid:
        :return:
        """
        if is_dhcp_enabled == 1:
            is_dhcp_enabled_1 = True
        else:
            is_dhcp_enabled = 0
            is_dhcp_enabled_1 = False
        # 创建op资源
        op_result = self.op_driver.\
            subnet_create(name=name,
                          description=description,
                          is_dhcp_enabled=is_dhcp_enabled_1,
                          network_id=network_uuid,
                          ip_version=ip_version,
                          gateway_ip=gateway_ip,
                          allocation_pools=allocation_pools,
                          cidr=cidr,
                          dns_nameservers=dns_nameservers,
                          host_routes=host_routes)
        if op_result.get('status') != 200:
            return op_result

        # 创建数据库资源
        try:
            db_result = self.db.\
                db_subnet_create(name=name,
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
        except Exception, e:
            log.error('create the subnet error, reason is: %s' % e)
            return request_result(401)

        log.info('create the subnet op_result is: %s, '
                 'db_result is: %s' % (op_result, db_result))
        return request_result(200, 'ok')


class NetworkOperateRouteManager(object):
    def __init__(self):
        pass
