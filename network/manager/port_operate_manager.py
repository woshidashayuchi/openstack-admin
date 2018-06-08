# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/4/9 9:43
from common.logs import logging as log
from common.request_result import request_result
from driver.openstack_driver import OpenstackDriver
from rpcclient.status_driver import StatusDriver
from db.network_db import NetworkDB
from common.skill import time_diff


class PortOperateManager(object):
    def __init__(self):
        self.driver = OpenstackDriver()
        self.status_update = StatusDriver()
        self.db = NetworkDB()

    def os_port_create(self, port_uuid, vm_uuid,
                       user_uuid=None,
                       project_uuid=None, team_uuid=None):
        try:
            port_detail = self.driver.get_port(port_uuid)

            network_uuid = port_detail.network_id
            ip_address = port_detail.fixed_ips[0].get('ip_address')
            # status = port_detail.status
            status = 'available'
            mac_address = port_detail.mac_address
        except Exception, e:
            log.error('get the os port detail error, reason is: %s' % e)
            return request_result(1064)

        try:
            self.db.db_port_create(port_uuid=port_uuid,
                                   name=port_uuid,
                                   description='DHCP:OS-PORT',
                                   ip_address=ip_address,
                                   network_uuid=network_uuid,
                                   mac_address=mac_address,
                                   status=status,
                                   user_uuid=user_uuid,
                                   project_uuid=project_uuid,
                                   team_uuid=team_uuid)
            self.db.db_port_vm_attach(port_uuid, vm_uuid)
        except Exception, e:
            log.error('insert the port into db error, reason is: %s' % e)
            return request_result(401)
        self.status_update.port_status(port_uuid)
        return request_result(0, {'resource_uuid': port_uuid})

    def port_random_create(self, network_uuid, name=None, description=None,
                           user_uuid=None, project_uuid=None, team_uuid=None):
        # check the network if bind subnet, if not, forbid to create port
        try:
            db_result = self.db.db_check_network_if_bind_subnet(network_uuid)
            if db_result[0][0] == 0:
                return request_result(1024)
        except Exception, e:
            log.error('check the network if connect to subnet error, '
                      'reason is: %s' % e)
            return request_result(403)

        op_result = self.driver.port_create(network_uuid=network_uuid,
                                            name=name,
                                            description=description)
        if op_result.get('status') != 0:
            return op_result

        try:
            port_uuid = op_result.get('result').id
            mac_address = op_result.get('result').mac_address
            # status = op_result.get('result').status
            status = 'available'
            ip_address = op_result.get('result').fixed_ips[0]['ip_address']
        except Exception, e:
            log.error('op_result explain error, reason is: %s' % e)
            # rollback
            self.driver.port_delete(op_result.get('result').id)
            return request_result(1061)

        try:
            self.db.db_port_create(port_uuid=port_uuid,
                                   name=name,
                                   description=description,
                                   ip_address=ip_address,
                                   network_uuid=network_uuid,
                                   mac_address=mac_address,
                                   status=status,
                                   user_uuid=user_uuid,
                                   project_uuid=project_uuid,
                                   team_uuid=team_uuid)
        except Exception, e:
            log.error('insert the port into db error, reason is: %s' % e)
            # rollback
            self.driver.port_delete(op_result.get('result').id)
            return request_result(401)
        self.status_update.port_status(port_uuid)
        return request_result(0, {'resource_uuid': port_uuid})

    def ports_network_list(self, network_uuid, page_num, page_size):
        ret = []
        try:
            db_result = self.db.db_ports_list(network_uuid,
                                              page_num=page_num,
                                              page_size=page_size)
            db_count = self.db.db_ports_count(network_uuid)
            count = db_count[0][0]
            if len(db_result) != 0:
                for port in db_result:
                    ret.append({'port_uuid': port[0],
                                'vm_uuid': port[8],
                                # 'name': port[1],
                                # 'description': port[2],
                                'ip_address': port[3],
                                'mac_address': port[4],
                                'status': port[5],
                                'create_time': time_diff(port[6]),
                                'update_time': time_diff(port[7])
                                })
            result = {
                'count': count,
                'ports_list': ret
            }
        except Exception, e:
            log.error('get the ports of network error, reason is: %s' % e)
            return request_result(403)

        return request_result(0, result)

    def ports_list(self, user_uuid, team_uuid, team_priv, project_uuid,
                   project_priv, page_size, page_num):
        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.ports_all_project(team_uuid,
                                                      project_uuid,
                                                      page_size,
                                                      page_num)
                db_count = self.db.ports_all_count_project(team_uuid,
                                                           project_uuid)
                count = db_count[0][0]
            else:
                db_result = self.db.ports_all_users(team_uuid,
                                                    project_uuid,
                                                    user_uuid,
                                                    page_size,
                                                    page_num)
                db_count = self.db.ports_all_users_count(team_uuid,
                                                         project_uuid,
                                                         user_uuid)
                count = db_count[0][0]
            if len(db_result) != 0:
                for port in db_result:
                    ret.append({
                        'port_uuid': port[0],
                        'vm_uuid': port[1],
                        # 'name': port[2],
                        # 'description': port[3],
                        'ip_address': port[4],
                        'network_uuid': port[5],
                        'mac_address': port[6],
                        'status': port[7],
                        'create_time': time_diff(port[8]),
                        'update_time': time_diff(port[9])
                    })

            result = {
                'count': count,
                'ports_list': ret
            }
            return request_result(0, result)
        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)


class PortRouteOperateManager(object):
    def __init__(self):
        self.driver = OpenstackDriver()
        self.db = NetworkDB()

    def port_operate_detail(self, port_uuid):
        result = dict()
        try:
            db_result = self.db.db_port_detail(port_uuid)
            if len(db_result) != 0:
                log.info('get the network detail result is: %s' % db_result)
                result['port_uuid'] = port_uuid,
                result['vm_uuid'] = db_result[0][1]
                result['name'] = db_result[0][2]
                result['description'] = db_result[0][3]
                result['ip_address'] = db_result[0][4]
                result['network_uuid'] = db_result[0][5]
                result['mac_address'] = db_result[0][6]
                result['status'] = db_result[0][7]
                result['create_time'] = time_diff(db_result[0][8])
                result['update_time'] = time_diff(db_result[0][9])
        except Exception, e:
            log.error('get the detail of port(db) error, reason is: %s' % e)
            return request_result(404)

        return request_result(0, result)

    def port_operate_delete(self, port_uuid):
        # check: if can delete the port
        try:
            db_result = self.db.db_port_if_can_del(port_uuid)
            # if db_result[0][0].lower() != 'down':
            if db_result[0][0].lower() != 'available':
                return request_result(405)
        except Exception, e:
            log.error('check the port if can delete error, reason is: %s' % e)
            return request_result(404)

        # delete the port from openstack env
        op_result = self.driver.port_delete(port_uuid)
        if op_result.get('status') != 0:
            return op_result

        # delete the port from database
        try:
            self.db.db_port_delete(port_uuid)
        except Exception, e:
            log.error('delete the port error, reason is: %s' % e)
            # rollback when delete error

            return request_result(404)
        return request_result(0, {'resource_uuid': port_uuid})

    def os_port_operate_delete(self, port_uuid):
        try:
            self.db.db_port_delete(port_uuid)
        except Exception, e:
            log.error('delete the port(db) error, reason is: %s' % e)
            return request_result(404)
        return request_result(0, {'resource_uuid': port_uuid})
