# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:44
from common.logs import logging as log
from common.parameters import allocation_pools_conform, dns_nameservers_conform, gateway_ip_create
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
        try:
            same_name = self.db.network_name_check(name, user_uuid,
                                                   project_uuid, team_uuid)
            if same_name[0][0] != 0:
                return request_result(302)
        except Exception, e:
            log.error('check the name is used(db) error, reason is: %s' % e)
            return request_result(999)

        op_result = self.op_driver.\
            network_create(name=name,
                           description=description,
                           # is_admin_state_up=is_admin_state_up_1,
                           # is_shared=is_shared_1
                          )
        if op_result.get('status') != 0:
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
            # rollback
            rollback_result = self.op_driver.network_delete(network_uuid)
            log.info('rollback result(op) is: %s' % rollback_result)
            return request_result(401)

        log.info('create the network result is: %s, '
                 'db result is: %s' % (op_result, db_result))

        return request_result(0, {'resource_uuid': network_uuid,
                                  'name': name,
                                  'description': description,
                                  'is_admin_state_up': is_admin_state_up,
                                  'is_shared': is_shared})

    def network_list(self, user_uuid, team_uuid, team_priv,
                     project_uuid, project_priv, page_size, page_num):
        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.db_network_list_project(team_uuid,
                                                            project_uuid,
                                                            page_size,
                                                            page_num)
                db_count = self.db.db_network_project_count(team_uuid,
                                                            project_uuid)
                count = db_count[0][0]
            else:
                db_result = self.db.db_network_list_user(team_uuid,
                                                         project_uuid,
                                                         user_uuid,
                                                         page_size,
                                                         page_num)
                db_count = self.db.db_network_user_count(team_uuid,
                                                         project_uuid,
                                                         user_uuid)
                count = db_count[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        try:
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
                    update_time = time_diff(network[11])
                    network_uuid = network[10]
                    ret.append({'network_uuid': network_uuid,
                                'name': name,
                                'subnet_name_and_cidr': subnet_name+' '+cidr,
                                'description': description,
                                'is_shared': is_shared,
                                'is_router_external': is_router_external,
                                # 'size': size,
                                'status': status,
                                'is_admin_state_up': is_admin_state_up,
                                'create_time': create_time,
                                'update_time': update_time})
            result = {
                'count': count,
                'network_list': ret
            }
        except Exception, e:
            log.error('explain the db result error, reason is: %s' % e)
            return request_result(999)

        return request_result(0, result)

    def check_network_status(self, network_uuid):
        try:
            network_status = self.op_driver.network_status(network_uuid)
            return network_status
        except Exception, e:
            log.error('check the status of network error, reason is: %s' % e)
            return request_result(999)

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
        try:
            allocation_pools_op = allocation_pools_conform(allocation_pools)
            dns_nameservers_op = dns_nameservers_conform(dns_nameservers)
            gateway_ip = gateway_ip_create(cidr)
        except Exception, e:
            log.error('exchange the parameters error, reason is: %s' % e)
            return request_result(999)
        
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
                          allocation_pools=allocation_pools_op,
                          cidr=cidr,
                          dns_nameservers=dns_nameservers_op,
                          host_routes=host_routes)
        if op_result.get('status') != 0:
            return op_result

        # 创建数据库资源
        try:
            subnet_uuid = op_result.get('result').id
            db_result = self.db.\
                db_subnet_create(subnet_uuid=subnet_uuid,
                                 name=name,
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
            # 回滚
            self.op_driver.subnet_delete(
                 op_result.get('result').id
            )
            return request_result(401)

        log.info('create the subnet op_result is: %s, '
                 'db_result is: %s' % (op_result, db_result))
        return request_result(0, 'ok')

    def subnet_list(self, user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv, page_size, page_num):
        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.db_subnet_list_project(team_uuid,
                                                           project_uuid,
                                                           page_size,
                                                           page_num)
                db_count = self.db.db_subnet_project_count(team_uuid,
                                                           project_uuid)
                count = db_count[0][0]
            else:
                db_result = self.db.db_subnet_list_user(team_uuid,
                                                        project_uuid,
                                                        user_uuid,
                                                        page_size,
                                                        page_num)
                db_count = self.db.db_subnet_user_count(team_uuid,
                                                        project_uuid,
                                                        user_uuid)
                count = db_count[0][0]

        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)
        try:
            if len(db_result) != 0:
                for subnet in db_result:
                    subnet_uuid = subnet[0]
                    name = subnet[1]
                    description = subnet[2]

                    ret.append({'subnet_uuid': subnet_uuid,
                                'name': name,
                                'description': description})
            result = {
                'count': count,
                'subnet_list': ret
            }
        except Exception, e:
            log.error('explain the db result error, reason is: %s' % e)
            return request_result(999)
        return request_result(0, result)

class NetworkOperateRouteManager(object):
    def __init__(self):
        self.op_driver = OpenstackDriver()
        self.db = NetworkDB()

    def network_detail(self, network_uuid):
        result = dict()
        try:
            db_result = self.db.db_network_detail(network_uuid)
        except Exception, e:
            log.error('get the network detail from db error, '
                      'reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for network in db_result:
                result['network_uuid'] = network_uuid
                result['name'] = network[0]
                result['subnet_name_and_cidr'] = network[1] + ' ' + network[2]
                result['description'] = network[3]
                result['is_shared'] = network[4]
                result['is_router_external'] = network[5]
                # result['size'] = network[6]
                result['status'] = network[7]
                result['is_admin_state_up'] = network[8]
                result['gateway_ip'] = network[11]
                result['allocation_pools'] = network[12]
                result['dns_nameservers'] = network[13]
                result['host_routes'] = network[14]
                result['create_time'] = time_diff(network[9])
                result['update_time'] = time_diff(network[10])

        return request_result(0, result)

    def network_delete(self, network_uuid):
        # 首先检查该网络有没有被虚拟机使用,如果正在使用，则禁止删除
        try:
            used_vm = self.db.delete_network_chk(network_uuid)[0][0]
            if used_vm != 0:
                return request_resul5(404)
        except Exception, e:
            log.error('check the network if used by vm error,'
                      'reason is: %s' % e)
            return request_result(403)
        
        # 删除openstack环境网络
        op_result = self.op_driver.network_delete(network_uuid)
        if op_result.get('status') != 0:
            return op_result

        # 删除数据库
        try:
            db_result = self.db.db_network_delete(network_uuid)
        except Exception, e:
            log.error('delete the network(db) error, reason is: %s' % e)
            # 回滚openstack

            return request_result(404)

        if db_result is not None:
            return request_result(404)
        return request_result(0, {'resource_uuid': network_uuid})

    def network_update(self, up_dict):
        try:
            op_result = self.op_driver.network_update(up_dict)
        except Exception, e:
            log.error('update the network(op) error, reason is: %s' % e)
            return request_result(1021)
        if op_result.get('status') != 0:
            return op_result

        # update db
        try:
            db_result = self.db.db_network_update(up_dict)
        except Exception, e:
            log.error('update the network(db) error, reason is: %s' % e)
            return request_result(402)

        log.info('update the network op_result is: %s, '
                 'db_result is: %s' % (op_result, db_result))

        return request_result(0, {'resource_uuid': up_dict['network_uuid']})

    def network_recovery(self):
        pass

    def subnet_delete(self, subnet_uuid, logic):
        # 子网只实现物理删除
        op_result = self.op_driver.subnet_delete(subnet_uuid)
        if op_result.get('status') != 0:
            return op_result
        # 删除数据库数据
        try:
            self.db.db_subnet_delete(subnet_uuid)
        except Exception, e:
            log.error('delete the subnet(db) error, reason is: %s' % e)
            return request_result(404)

        return op_result
