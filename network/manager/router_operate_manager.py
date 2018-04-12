# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/22 11:41
from common.logs import logging as log
from common.request_result import request_result
from driver.openstack_driver import OpenstackDriver
from db.network_db import NetworkDB
from common.skill import time_diff


class RouterOperateManager(object):

    def __init__(self):
        self.op_driver = OpenstackDriver()
        self.db = NetworkDB()

    def router_create(self, name, description, user_uuid,
                      project_uuid, team_uuid, is_admin_state_up=0):
        if is_admin_state_up == 1:
            is_admin_state_up_1 = True
        else:
            is_admin_state_up_1 = False
        op_result = self.op_driver.router_create(
            name=name,
            description=description,
            is_admin_state_up=is_admin_state_up_1
        )
        if op_result.get('status') != 0:
            return op_result

        try:
            db_result = self.db.db_router_create(
                name=name,
                description=description,
                is_admin_state_up=is_admin_state_up,
                user_uuid=user_uuid,
                project_uuid=project_uuid,
                team_uuid=team_uuid,
                router_uuid=op_result.get('result')
            )
        except Exception, e:
            log.error('create the router(db) error, reason is: %s' % e)
            # rollback
            self.op_driver.router_delete(op_result.get('result'))
            return request_result(402)

        log.info('create the router, op_result is: %s,'
                 'db_result is: %s' % (op_result, db_result))

        return request_result(0, {'resource_uuid': op_result.get('result'),
                                  'name': name,
                                  'description': description,
                                  'is_admin_state_up': is_admin_state_up
                                  })

    def router_list(self, user_uuid, project_uuid, team_uuid, team_priv,
                    project_priv, page_size, page_num):
        result = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.db_router_list_project(team_uuid,
                                                           project_uuid,
                                                           page_size,
                                                           page_num)
            else:
                db_result = self.db.db_router_list_user(team_uuid,
                                                        project_uuid,
                                                        user_uuid,
                                                        page_size,
                                                        page_num)

        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for router in db_result:
                router_uuid = router[0]
                name = router[1]
                description = router[2]
                status = router[3]
                create_time = time_diff(router[4])
                update_time = time_diff(router[5])
                result.append({'router_uuid': router_uuid,
                               'name': name,
                               'description': description,
                               'status': status,
                               'create_time': create_time,
                               'update_time': update_time})

        return request_result(0, result)


class RouterOperateRouteManager(object):
    def __init__(self):
        self.db = NetworkDB()
        self.op_driver = OpenstackDriver()

    def router_update(self, router_uuid, name=None,
                      is_admin_state_up=1, up_type=None):
        # update op
        op_result = self.op_driver.router_update(
                         router_uuid=router_uuid,
                         router_name=name,
                         is_admin_state_up=is_admin_state_up,
                         up_type=up_type)
        if op_result.get('status') != 0:
            return op_result

        try:
            self.db.db_router_update(router_uuid,
                                     {'name': name,
                                      'is_admin_state_up': is_admin_state_up})
        except Exception, e:
            log.error('update the db for router error, reason is: %s' % e)
            return request_result(402)

        return request_result(0, {'resource_uuid': router_uuid})

    def router_delete(self, router_uuid, logic=0):
        if logic == 1:
            # 逻辑删除
            try:
                self.db.db_router_logic_del(router_uuid)
            except Exception, e:
                log.error('logic delete the router error, reason is: %s' % e)
                return request_result(402)
        else:
            # 物理删除
            # op
            op_result = self.op_driver.router_delete(router_uuid)
            if op_result.get('status') != 0:
                return op_result
            # db
            try:
                self.db.db_router_delete(router_uuid)
            except Exception, e:
                log.error('delete the router error, reason is: %s' % e)
                # rollback
                return request_result(404)

            return request_result(0, {'resource_uuid': router_uuid})

    def router_detail(self, router_uuid):
        result = dict()
        try:
            db_result = self.db.db_router_detail(router_uuid)
        except Exception, e:
            log.error('get the detail of router error, reason is: %s' % e)
            return request_result(403)
        for router in db_result:
            result['router_uuid'] = router[0]
            result['name'] = router[1]
            result['description'] = router[2]
            result['external_gateway_info'] = router[3]
            result['is_admin_state_up'] = router[4]
            result['status'] = router[5]
            result['create_time'] = time_diff(router[6])
            result['update_time'] = time_diff(router[7])

        return request_result(0, result)

    def router_gateway_ab(self, router_uuid, network_uuid):

        op_result = self.op_driver.gateway_to_router(router_uuid,
                                                     network_uuid)
        if op_result.get('status') != 0:
            return op_result
        # else:
        #     op_result = self.op_driver.remove_gateway_from_router(router_uuid,
        #                                                           network_uuid)
        #     if op_result.get('status') != 0:
        #         return op_result

        # 操作数据库
        try:
            self.db.db_router_gateway_ab(router_uuid=router_uuid,
                                         network_uuid=network_uuid)
        except Exception, e:
            log.error('add gateway to router(db) error, '
                      'reason is: %s' % e)
            # 回滚
            return request_result(402)

        return op_result

    def router_interface_ab(self, router_uuid,  network_uuid, subnet_uuid,
                            ip_address, rtype):
        """
        :param router_uuid:
        :param network_uuid:
        :param subnet_uuid:
        :param ip_address:
        :param rtype:
        :return:
        """
        port_uuid = None
        if rtype == 'add':
            if ip_address is not None:
                # 创建port并得到port_uuid
                port = self.op_driver.port_create(network_uuid)
                if port.get('status') != 0:
                    return port
                else:
                    port_uuid = port.get('result').id
                    try:
                        self.db.db_port_create(port_uuid=port_uuid,
                                               name=port.name,
                                               description=port.description,
                                               ip_address=port.ip_address,
                                               network_uuid=network_uuid,
                                               mac_address=port.mac_address,
                                               status=port.status)
                    except Exception, e:
                        log.error('create the port(db) error, '
                                  'reason is: %s' % e)
                        return request_result(401)
                    # ip_address指向
                    add_ip_result = self.op_driver.add_ip_to_port(port_uuid,
                                                                  ip_address)
                    if add_ip_result.get('status') != 0:
                        return add_ip_result

            op_result = self.op_driver.add_interface_to_router(router_uuid,
                                                               subnet_uuid,
                                                               port_uuid)
        else:
            op_result = self.op_driver.remove_interface_from_router(
                             router_uuid,
                             subnet_uuid)

        # 每个被添加进路由接口的子网都应该有这条记录
        try:
            self.db.db_router_interface_ab(router_uuid,
                                           subnet_uuid,
                                           rtype)
        except Exception, e:
            log.error('router interface update(db) error, reason is: %s' % e)
            return request_result(402)

        return op_result

    def router_recovery(self):
        pass
