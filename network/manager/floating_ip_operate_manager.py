# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/27 14:11
from driver.openstack_driver import OpenstackDriver
from db.network_db import NetworkDB
from rpcclient.status_driver import StatusDriver
from common.request_result import request_result
from common.logs import logging as log
from common.skill import time_diff


class FloatingIpOperateManager(object):
    def __init__(self):
        self.op = OpenstackDriver()
        self.status_update = StatusDriver()
        self.db = NetworkDB()

    def floating_ip_create(self, floating_network_id, user_uuid,
                           project_uuid, team_uuid):
        op_result = self.op.floating_ip_create(floating_network_id)
        if op_result.get('status') != 0:
            return op_result
        try:
            floatingip_uuid = op_result.get('result').id
            name = op_result.get('result').name
            description = op_result.get('result').description
            router_uuid = op_result.get('result').router_id
            fixed_ip_address = op_result.get('result').fixed_ip_address
            floating_ip_address = op_result.get('result').floating_ip_address
            revision_number = op_result.get('result').revision_number
            port_id = op_result.get('result').port_id
        except Exception, e:
            log.error('explain the floatingip create result of openstack '
                      'error, reason is: %s' % e)
            return request_result(1051)

        try:
            self.db.db_floating_ip_create(
                floatingip_uuid=floatingip_uuid,
                name=name,
                description=description,
                router_uuid=router_uuid,
                fixed_ip_address=fixed_ip_address,
                floating_ip_address=floating_ip_address,
                revision_number=revision_number,
                port_id=port_id,
                user_uuid=user_uuid,
                project_uuid=project_uuid,
                team_uuid=team_uuid)
        except Exception, e:
            log.error('create the floating ip(db) error, reason is: %s' % e)
            return request_result(401)
        self.status_update.floatip_status(floatingip_uuid)
        return request_result(0, {'resource_uuid': floatingip_uuid,
                                  'name': name,
                                  'description': description,
                                  'router_uuid': router_uuid,
                                  'fixed_ip_address': fixed_ip_address,
                                  'floating_ip_address': floating_ip_address,
                                  'revision_number': revision_number,
                                  'port_id': port_id})

    def floating_ip_list(self, user_uuid, team_uuid, team_priv,
                         project_uuid, project_priv, page_size, page_num):
        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.db_floating_ip_list_project(team_uuid,
                                                                project_uuid,
                                                                page_size,
                                                                page_num)
                db_count = self.db.floatingip_project_count(team_uuid,
                                                            project_uuid)
                count = db_count[0][0]
            else:
                db_result = self.db.db_floating_ip_list(team_uuid,
                                                        project_uuid,
                                                        user_uuid,
                                                        page_size,
                                                        page_num)
                db_count = self.db.floatingip_user_count(team_uuid,
                                                         project_uuid,
                                                         user_uuid)
                count = db_count[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        try:
            if len(db_result) != 0:
                for fltip in db_result:
                    floatingip_uuid = fltip[0]
                    name = fltip[1]
                    description = fltip[2]
                    router_uuid = fltip[3]
                    fixed_ip_address = fltip[4]
                    floating_ip_address = fltip[5]
                    revision_number = fltip[6]
                    port_id = fltip[7]
                    vm_uuid = fltip[10]
                    status = fltip[11]
                    create_time = time_diff(fltip[8])
                    update_time = time_diff(fltip[9])
                    ret.append(
                        {
                            'floatingip_uuid': floatingip_uuid,
                            'name': name,
                            'description': description,
                            'router_uuid': router_uuid,
                            'fixed_ip_address': fixed_ip_address,
                            'floating_ip_address': floating_ip_address,
                            'revision_number': revision_number,
                            'port_id': port_id,
                            'vm_uuid': vm_uuid,
                            'status': status,
                            'create_time': create_time,
                            'update_time': update_time
                        }
                    )
            result = {
                'count': count,
                'floatingip_list': ret
            }
        except Exception, e:
            log.error('explain the db result error, reason is: %s' % e)
            return request_result(999)
        return request_result(0, result)

    def floating_ip_detail(self, floatingip_uuid):
        result = dict()
        try:
            db_result = self.db.db_floating_ip_detail(floatingip_uuid)
        except Exception, e:
            log.error('get the floatingip(db) detail error, reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            result['floatingip_uuid'] = db_result[0][0]
            result['name'] = db_result[0][1],
            result['description'] = db_result[0][2],
            result['router_uuid'] = db_result[0][3],
            result['fixed_ip_address'] = db_result[0][4]
            result['floating_ip_address'] = db_result[0][5]
            result['revision_number'] = db_result[0][6]
            result['port_id'] = db_result[0][7]
            result['vm_uuid'] = db_result[0][10]
            result['status'] = db_result[0][11]
            result['create_time'] = time_diff(db_result[0][8])
            result['update_time'] = time_diff(db_result[0][9])

        return request_result(0, result)

    def floating_ip_delete(self, floatingip_uuid, logic):
        # 检查是否可以删除
        try:
            del_check = self.db.db_is_floating_ip_del(floatingip_uuid)
            log.info('the fixed_ip_address count of the '
                     'floatingip is: %s' % del_check)
            if del_check[0][0] != 0:
                return request_result(0, 'floating ip is '
                                         'used by instance, can not delete')
        except Exception, e:
            log.error('check the floating ip if could delete '
                      'error, reason is: %s' % e)
            return request_result(403)
        if logic == 1:
            try:
                self.db.db_floating_ip_logic_del(floatingip_uuid)

            except Exception, e:
                log.error('delete the db(logic) error, reason is: %s' % e)
                return request_result(404)

            return request_result(0, {'resource_uuid': floatingip_uuid})

        else:
            # 删除数据库中的数据(更改显示状态为0，方便回滚，后期使用服务删除)
            try:
                self.db.db_floating_ip_logic_del(floatingip_uuid)
            except Exception, e:
                log.error('delete the db(real) error, reason is: %s' % e)
                return request_result(404)

            # 删除op
            op_result = self.op.floating_ip_delete(floatingip_uuid)
            # 如果op删除失败，回滚数据库
            if op_result.get('status') != 0:
                self.db.db_floating_ip_rollback(floatingip_uuid)
                return request_result(1053)

            return request_result(0, {'resource_uuid': floatingip_uuid})

    def floating_ip_bind(self, vm_uuid, floatingip, fixed_address):

        try:
            # get the float ip uuid
            floatingip_uuid = self.db.db_get_floatingip_uuid(floatingip)
            if len(floatingip_uuid[0]) == 0:
                return request_result(1058)
            else:
                floatingip_uuid = floatingip_uuid[0][0]
            # check the float ip if it has binded
            db_check = self.db.db_check_floatingip_bind(floatingip_uuid)
            if db_check[0][0] != 0:
                return request_result(1058)
        except Exception, e:
            log.error('check the floatingip if bined(db) error,'
                      'reason is: %s' % e)
            return request_result(403)

        # bind
        op_result = self.op.floatip_bind(vm_uuid,
                                         floatingip,
                                         fixed_address)
        if op_result.get('status') != 0:
            return op_result

        # update the database
        try:
            self.db.db_floating_ip_bind(vm_uuid,
                                        floatingip_uuid,
                                        fixed_address)
        except Exception, e:
            log.error('bind the floatingip to vm(db) error, reason is: %s' % e)
            # rollback
            self.op.floatip_unbind(vm_uuid, floatingip)
            return request_result(402)
        log.info('bind end...')
        return request_result(0, floatingip)

    def floating_ip_unbind(self, floatingip):
        try:
            # get the float ip uuid
            floatingip_uuid = self.db.db_get_floatingip_uuid(floatingip)
            if len(floatingip_uuid[0]) == 0:
                return request_result(1058)
            else:
                floatingip_uuid = floatingip_uuid[0][0]

            # check the float ip if need unbind
            db_check = self.db.db_check_floatingip_bind(floatingip_uuid)
            if db_check[0][0] == 0:
                log.info('need not unbind!!!')
                return request_result(0)

            # get the vm_uuid the floatip binded
            db_message = self.db.db_get_floatingip_addr(
                                 floatingip_uuid)
            floatingip_addr = db_message[0][0]
            vm_uuid = db_message[0][1]
            fixed_ip_address = db_message[0][2]
            if fixed_ip_address == 'None':
                fixed_ip_address = None
        except Exception, e:
            log.error('check the floatingip if unbined(db) error, '
                      'reason is: %s' % e)
            return request_result(403)

        # unbind
        op_result = self.op.floatip_unbind(vm_uuid, floatingip_addr)
        if op_result.get('status') != 0:
            return op_result

        # update the database
        try:
            self.db.db_floating_ip_unbind(floatingip_uuid)
        except Exception, e:
            log.error('unbind the floatingip from vm(db) error, '
                      'reason is: %s' % e)
            # rollback
            self.op.floatip_bind(vm_uuid,
                                 floatingip,
                                 fixed_address=fixed_ip_address)
            return request_result(402)

        return request_result(0, floatingip)
