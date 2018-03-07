# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

import re
import uuid
import json
import socket

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder
from common.ucenter_api import UcenterApi

from compute.db import compute_db
from compute.driver import compute_driver
from compute.driver import openstack_driver


class CloudHostManager(object):

    def __init__(self):

        self.billing_check = conf.billing
        self.ucenter_api = UcenterApi()
        self.compute_db = compute_db.ComputeDB()
        self.compute_driver = compute_driver.ComputeDriver()
        self.local_ip = socket.gethostbyname(socket.gethostname())

    def cloudhost_create(self, team_uuid, project_uuid, user_uuid,
                         availzone_uuid, image_uuid, vm_name, vm_cpu,
                         vm_mem, disk_list, nic_list, password, cost,
                         token, source_ip, resource_name):

        # disk_list为包含volume_type，volume_size字典的一个列表
        # nic_list为包含vswitch_uuid的列表

        # 创建步骤
        # 1.克隆镜像
        # 2.创建数据盘
        # 3.创建网卡
        # 4.写入数据库
        # 注意，任意步骤出现异常时，需要回滚之前已执行的步骤

        vm_uuid = str(uuid.uuid4())

        os_disk_name = '%s_osdisk' % (vm_name)
        vm_disk_list = []
        try:
            req_result = self.compute_driver.osdisk_create(
                              token, image_uuid, os_disk_name)
            disk_uuid = req_result['volume_uuid']
            disk_name = req_result['disk_name']

            disk_info = {
                            "disk_uuid": disk_uuid,
                            "disk_name": disk_name
                        }
            vm_disk_list.append(disk_info)
        except Exception, e:
            log.error('osdisk create failure, image_uuid=%s, reason=%s'
                      % (image_uuid, e))
            return request_result(511)

        try:
            cnt = 1
            for v_disk_info in disk_list:
                disk_type = v_disk_info['disk_type']
                disk_size = v_disk_info['disk_size']
                disk_name = '%s_datadisk0%s' % (vm_name, cnt)

                req_result = self.compute_driver.clouddisk_create(
                                  token, availzone_uuid, disk_name,
                                  disk_type, disk_size)
                disk_uuid = req_result['volume_uuid']
                disk_name = req_result['disk_name']

                disk_info = {
                                "disk_uuid": disk_uuid,
                                "disk_name": disk_name
                            }
                vm_disk_list.append(disk_info)
                cnt += 1
        except Exception, e:
            log.error('clouddisk create failure, reason=%s' % (e))
            for disk_info in vm_disk_list:
                disk_uuid = disk_info['disk_uuid']
                self.compute_driver.clouddisk_delete(
                     token, disk_uuid)
            return request_result(511)

        vm_ip_list = []
        vm_nic_list = []
        try:
            for vswitch_uuid in nic_list:
                req_result = self.compute_driver.vnic_create(
                                  token, vswitch_uuid, vm_uuid, vm_name)
                vnic_uuid = req_result['vnic_uuid']
                vnic_mac = req_result['vnic_mac']
                vnic_ip = req_result['vnic_ip']
                netmask = req_result['netmask']
                gateway = req_result['gateway']
                dns = req_result['dns']

                vnic_info = {
                                "vnic_uuid": vnic_uuid,
                                "vnic_mac": vnic_mac,
                                "vnic_ip": vnic_ip,
                                "netmask": netmask,
                                "gateway": gateway,
                                "dns": dns
                            }
                vm_ip_list.append(vnic_ip)
                vm_nic_list.append(vnic_info)
        except Exception, e:
            log.error('vnic create failure, reason=%s' % (e))
            for vnic_info in vm_nic_list:
                vnic_uuid = vnic_info['vnic_uuid']
                self.compute_driver.vnic_delete(
                     token, vnic_uuid)

            for disk_info in vm_disk_list:
                disk_uuid = disk_info['disk_uuid']
                self.compute_driver.clouddisk_delete(
                     token, disk_uuid)
            return request_result(5001)

        try:
            self.compute_db.cloudhost_create(
                 vm_uuid, vm_name, image_name, vm_ip_list,
                 vm_cpu, vm_mem, vm_disk_list, vm_nic_list,
                 availzone_uuid, availzone_name, login_way,
                 keys_name, team_uuid, project_uuid, user_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))

            for vnic_info in vm_nic_list:
                vnic_uuid = vnic_info['vnic_uuid']
                self.compute_driver.vnic_delete(
                     token, vnic_uuid)

            for disk_info in vm_disk_list:
                disk_uuid = disk_info['disk_uuid']
                self.compute_driver.clouddisk_delete(
                     token, disk_uuid)

            return request_result(401)

        if self.billing_check is True:
            resource_type = 'cloudhost'
            vm_conf = int(vm_cpu) * 4 + int(vm_mem)
            resource_conf = str(vm_conf) + 'X'
            resource_status = 'off'
            self.ucenter_api.billing_create(
                 token, vm_uuid, vm_name, resource_type,
                 resource_conf, resource_status)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_name": vm_name,
                     "vm_cpu": vm_cpu,
                     "vm_mem": vm_mem,
                     "pool_uuid": pool_uuid,
                     "availzone_uuid": availzone_uuid,
                     "resource_uuid": vm_uuid
                 }

        return request_result(0, result)

    def cloudhost_list(self, user_uuid, team_uuid, team_priv,
                       project_uuid, project_priv,
                       page_size, page_num):

        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                cloudhosts_list_info = self.compute_db.cloudhost_list_project(
                                            team_uuid, project_uuid,
                                            page_size, page_num)
            else:
                cloudhosts_list_info = self.compute_db.cloudhost_list_user(
                                            team_uuid, project_uuid, user_uuid,
                                            page_size, page_num)

            cloudhost_list = cloudhosts_list_info['cloudhost_list']
            count = cloudhosts_list_info['count']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        result = {
                     "count": count,
                     "cloudhost_list": cloudhost_list
                 }

        return request_result(0, result)

    def cloudhost_info(self, vm_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        result = {"cloudhost_info": cloudhost_info}

        return request_result(0, result)

    def cloudhost_power_on(self, vm_uuid, token,
                           source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, power on denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        try:
            self.compute_driver.vm_boot(
                 token, vm_uuid)

            log.info('cloudhost power on finish, '
                     'vm_uuid=%s, vm_name=%s'
                     % (vm_uuid, vm_name))
        except Exception, e:
            log.error('cloudhost power on failure, '
                      'vm_uuid=%s, vm_name=%s, '
                      'reason=%s'
                      % (vm_uuid, vm_name, e))
            return request_result(1501)

        try:
            self.compute_db.cloudhost_status_update(
                 vm_uuid, 'start')
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            self.ucenter_api.billing_update(
                 token, vm_uuid, resource_status='on')

        return request_result(0)

    def cloudhost_power_off(self, vm_uuid, token,
                            source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status == 'off':
            return request_result(0)

        try:
            self.compute_driver.vm_shut(
                 token, vm_uuid)
            log.info('cloudhost power off finish, '
                     'vm_uuid=%s, vm_name=%s'
                     % (vm_uuid, vm_name))
        except Exception, e:
            log.error('cloudhost power off failure, '
                      'vm_uuid=%s, vm_name=%s, reason=%s'
                      % (vm_uuid, vm_name, e))
            return request_result(501)

        try:
            self.compute_db.cloudhost_status_update(
                 vm_uuid, 'off')
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            self.ucenter_api.billing_update(
                 token, vm_uuid, resource_status='off')

        return request_result(0)

    def cloudhost_cpu_update(self, vm_uuid, vm_cpu,
                             token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_mem = cloudhost_info['vm_mem']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, cpu update denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        try:
            self.compute_db.cloudhost_cpu_update(
                 vm_uuid, vm_cpu)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            vm_conf = int(vm_cpu) * 4 + int(vm_mem)
            resource_conf = str(vm_conf) + 'X'
            self.ucenter_api.billing_update(
                 token, vm_uuid, resource_conf=resource_conf)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_cpu": vm_cpu,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_mem_update(self, vm_uuid, vm_mem,
                             token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_cpu = cloudhost_info['vm_cpu']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, mem update denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        try:
            self.compute_db.cloudhost_mem_update(
                 vm_uuid, vm_mem)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            vm_conf = int(vm_cpu) * 4 + int(vm_mem)
            resource_conf = str(vm_conf) + 'X'
            self.ucenter_api.billing_update(
                 token, vm_uuid, resource_conf=resource_conf)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_mem": vm_mem,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_disk_mount(self, vm_uuid, disk_uuid,
                             token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_disk = cloudhost_info['vm_disk']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        # if status != 'off':
        #    log.warning('vm status is not off, disk mount denied, '
        #                'vm_uuid=%s, vm_name=%s'
        #                % (vm_uuid, vm_name))
        #    return request_result(202)

        vm_disk_list = [json.loads(x) for x in vm_disk.split(";")]
        try:
            req_result = self.compute_driver.clouddisk_info(
                              token, disk_uuid)
            disk_name = req_result['disk_name']

            disk_info = {
                            "disk_uuid": disk_uuid,
                            "disk_name": disk_name
                        }
            vm_disk_list.append(disk_info)
        except Exception, e:
            log.error('clouddisk info get failure, disk_uuid=%s, reason=%s'
                      % (disk_uuid, e))
            return request_result(1501)

        try:
            self.compute_db.cloudhost_disk_update(
                 vm_uuid, vm_disk_list)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_disk": vm_disk_list,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_disk_umount(self, vm_uuid, disk_uuid,
                              token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_disk = cloudhost_info['vm_disk']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, disk umount denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        vm_disk = [json.loads(x) for x in vm_disk.split(";")]
        vm_disk_list = []
        for disk_info in vm_disk:
            v_disk_uuid = disk_info["disk_uuid"]
            if v_disk_uuid == disk_uuid:
                continue
            else:
                vm_disk_list.append(disk_info)

        try:
            self.compute_db.cloudhost_disk_update(
                 vm_uuid, vm_disk_list)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_disk": vm_disk_list,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_nic_attach(self, vm_uuid, vnic_uuid,
                             token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_ip = cloudhost_info['vm_ip']
            vm_nic = cloudhost_info['vm_nic']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, nic attach denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        vm_ip_list = [str(x) for x in vm_ip.split(";")]
        vm_nic_list = [json.loads(x) for x in vm_nic.split(";")]
        try:
            req_result = self.compute_driver.vnic_info(
                              token, vnic_uuid)
            vnic_mac = req_result['vnic_mac']
            vnic_ip = req_result['vnic_ip']

            vnic_info = {
                            "vnic_uuid": vnic_uuid,
                            "vnic_mac": vnic_mac
                        }
            vm_ip_list.append(vnic_ip)
            vm_nic_list.append(vnic_info)
        except Exception, e:
            log.error('vnic info get failure, vnic_uuid=%s, reason=%s'
                      % (vnic_uuid, e))
            return request_result(1501)

        try:
            self.compute_db.cloudhost_vnic_update(
                 vm_uuid, vm_ip_list, vm_nic_list)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_ip": vm_ip_list,
                     "vm_nic": vm_nic_list,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_nic_unattach(self, vm_uuid, vnic_uuid,
                               token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_ip = cloudhost_info['vm_ip']
            vm_nic = cloudhost_info['vm_nic']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, vnic unattach denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        vm_ip_list = [str(x) for x in vm_ip.split(";")]
        vm_nic_list = [json.loads(x) for x in vm_nic.split(";")]
        try:
            req_result = self.compute_driver.vnic_info(
                              token, vnic_uuid)
            vnic_mac = req_result['vnic_mac']
            vnic_ip = req_result['vnic_ip']

            vnic_info = {
                            "vnic_uuid": vnic_uuid,
                            "vnic_mac": vnic_mac
                        }
            vm_ip_list.remove(vnic_ip)
            vm_nic_list.remove(vnic_info)
        except Exception, e:
            log.error('vnic info get failure, vnic_uuid=%s, reason=%s'
                      % (vnic_uuid, e))
            return request_result(1501)

        try:
            self.compute_db.cloudhost_vnic_update(
                 vm_uuid, vm_ip_list, vm_nic_list)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_ip": vm_ip_list,
                     "vm_nic": vm_nic_list,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_floatip_bind(self, vm_uuid, lan_ip,
                               floatip, start_port, end_port,
                               token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            self.compute_driver.floatip_bind(
                 token, vm_uuid, vm_name, lan_ip,
                 floatip, start_port, end_port, source_ip)
            log.info('cloudhost floatip bind finish, '
                     'vm_uuid=%s, vm_name=%s'
                     % (vm_uuid, vm_name))
        except Exception, e:
            log.error('cloudhost floatip bind failure, '
                      'vm_uuid=%s, vm_name=%s, reason=%s'
                      % (vm_uuid, vm_name, e))
            return request_result(1501)

        try:
            self.compute_db.cloudhost_floatip_update(
                 vm_uuid, floatip)
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "vm_uuid": vm_uuid,
                     "lan_ip": lan_ip,
                     "floatip": floatip,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_floatip_unbind(self, vm_uuid, token,
                                 source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            floatip = cloudhost_info['floatip']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if floatip == 'None':
            log.warning('vm not bind floatip, operate denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        try:
            self.compute_driver.floatip_unbind(
                 token, vm_uuid, vm_name, floatip, source_ip)
            log.info('cloudhost floatip unbind finish, '
                     'vm_uuid=%s, vm_name=%s'
                     % (vm_uuid, vm_name))
        except Exception, e:
            log.error('cloudhost floatip unbind failure, '
                      'vm_uuid=%s, vm_name=%s, reason=%s'
                      % (vm_uuid, vm_name, e))
            return request_result(501)

        try:
            self.compute_db.cloudhost_floatip_update(
                 vm_uuid, 'None')
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        result = {
                     "vm_uuid": vm_uuid,
                     "floatip": floatip,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_password_change(self, vm_uuid, password,
                                  token, source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'on':
            log.warning('vm status is not on, password change denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        try:
            self.compute_driver.vm_pwd_reset(
                 token, host_uuid, vm_uuid, password)
            log.info('cloudhost password change finish, '
                     'vm_uuid=%s, vm_name=%s'
                     % (vm_uuid, vm_name))
        except Exception, e:
            log.error('cloudhost password change failure, '
                      'vm_uuid=%s, vm_name=%s, reason=%s'
                      % (vm_uuid, vm_name, e))
            return request_result(1501)

        result = {
                     "vm_uuid": vm_uuid,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_delete(self, vm_uuid, token,
                         source_ip, resource_uuid):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            try:
                self.compute_driver.vm_shut(
                     token, host_uuid, vm_uuid)
            except Exception, e:
                log.error('vm shutdown failure, host_uuid=%s, '
                          'vm_uuid=%s, reason=%s'
                          % (host_uuid, vm_uuid, e))
                return request_result(1501)

        try:
            self.compute_db.cloudhost_status_update(
                 vm_uuid, 'delete')
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            self.ucenter_api.billing_delete(token, vm_uuid)

        result = {
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_recovery(self, vm_uuid, token,
                           source_ip, resource_uuid):

        # 注意，vm恢复时，需要将vm使用的云硬盘和网卡一并恢复
        if self.billing_check is True:
            # 获取并检查用户余额，只有当余额大于0时才允许执行恢复操作
            team_balance = self.ucenter_api.team_balance(token)
            if team_balance.get('status') != 0:
                log.error('Get balance info error, '
                          'team_balance=%s' % (team_balance))
                return request_result(601)
            else:
                balance = team_balance.get('result').get('balance')
                if float(balance) <= 0:
                    return request_result(302)

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_cpu = cloudhost_info['vm_cpu']
            vm_mem = cloudhost_info['vm_mem']
            vm_disk = cloudhost_info['vm_disk']
            vm_nic = cloudhost_info['vm_nic']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            for disk_info in vm_disk:
                disk_uuid = disk_info["disk_uuid"]
                self.compute_driver.clouddisk_recovery(
                     token, disk_uuid)
        except Exception, e:
            log.error('Clouddisk recovery failure, '
                      'disk_uuid=%s, reason=%s'
                      % (disk_uuid, e))
            return request_result(501)

        try:
            for vnic_info in vm_nic:
                vnic_uuid = vnic_info["vnic_uuid"]
                self.compute_driver.vnic_recovery(
                     token, vnic_uuid)
        except Exception, e:
            log.error('vnic recovery failure, '
                      'vnic_uuid=%s, reason=%s'
                      % (vnic_uuid, e))
            return request_result(501)

        try:
            self.compute_db.cloudhost_status_update(vm_uuid, 'off')
        except Exception, e:
            log.error('Database update error, reason=%s' % (e))
            return request_result(403)

        if self.billing_check is True:
            pass
            # 创建计费信息
            # resource_type = 'cloudhost'
            # vm_conf = int(vm_cpu) * 4 + int(vm_mem)
            # resource_conf = str(vm_conf) + 'X'
            # resource_status = 'off'
            # self.ucenter_api.billing_create(
            #     token, vm_uuid, vm_name, resource_type,
            #     resource_conf, resource_status)

        result = {
                     "vm_uuid": vm_uuid,
                     "resource_name": vm_name
                 }

        return request_result(0, result)

    def cloudhost_reclaim_check(self):

        balances_check = self.ucenter_api.balances_check()
        if balances_check.get('status') != 0:
            log.error('Billing balances check error, '
                      'balances_check=%s' % (balances_check))
            return request_result(601)
        else:
            teams_list = balances_check.get('result').get('teams_list')

        try:
            ret = self.ucenter_api.service_token()
            if int(ret.get('status')) == 0:
                token = ret['result']['user_token']
            else:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Get service token error: reason=%s' % (e))
            return request_result(601)

        for team_info in teams_list:
            try:
                team_uuid = team_info['team_uuid']
                balance = team_info['balance']
                if float(balance) <= 0:
                    # 获取该team下的所有云主机资源列表，然后进行逻辑删除
                    cloudhosts_list = self.compute_db.cloudhost_list_team(
                                           team_uuid)['cloudhost_list']
                    for cloudhost_info in cloudhosts_list:
                        vm_uuid = cloudhost_info['vm_uuid']
                        self.cloudhost_delete(
                             vm_uuid, token, source_ip=self.local_ip,
                             resource_uuid=vm_uuid)
            except Exception, e:
                log.error('cloudhost reclaim failure, reason=%s' % (e))

    def cloudhost_reclaim_delete(self):

        try:
            ret = self.ucenter_api.service_token()
            if int(ret.get('status')) == 0:
                token = ret['result']['user_token']
            else:
                raise(Exception('request_code not equal 0'))
        except Exception, e:
            log.error('Get service token error: reason=%s' % (e))
            return request_result(601)

        try:
            cloudhosts_list = self.compute_db.cloudhost_list_dead(
                                   )['cloudhost_list']
            for cloudhost_info in cloudhosts_list:
                vm_uuid = cloudhost_info['vm_uuid']
                vm_name = cloudhost_info['vm_name']

                self.compute_db.cloudhost_delete(vm_uuid)
                log.critical('cloudhost name=%s, uuid=%s, '
                             'physical delete finish.'
                             % (vm_name, vm_uuid))
        except Exception, e:
            log.error('cloudhost reclaim delete failure, '
                      'vm_uuid=%s, vm_name=%s, reason=%s'
                      % (vm_uuid, vm_name, e))
