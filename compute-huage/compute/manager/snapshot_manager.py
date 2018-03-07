# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

import uuid
import json

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.json_encode import CJsonEncoder

from compute.db import compute_db
from compute.driver import compute_driver


class SnapshotManager(object):

    def __init__(self):

        self.billing_check = conf.billing
        self.compute_db = compute_db.ComputeDB()
        self.compute_driver = compute_driver.ComputeDriver()

    def snapshot_create(self, team_uuid, project_uuid, user_uuid,
                        snapshot_name, vm_uuid, comment,
                        token, source_ip, resource_name):

        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_ip = cloudhost_info['vm_ip']
            vm_cpu =  cloudhost_info['vm_cpu']
            vm_mem = cloudhost_info['vm_mem']
            vm_disk = cloudhost_info['vm_disk']
            vm_nic = cloudhost_info['vm_nic']
            availzone_uuid = cloudhost_info['availzone_uuid']
            availzone_name = cloudhost_info['availzone_name']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            name_check = self.compute_db.snapshot_name_check(
                              snapshot_name, project_uuid,
                              availzone_uuid)['name_check']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if name_check != 0:
            log.warning('Snapshot name(%s) already exists'
                        % (snapshot_name))
            return request_result(301)

        # 配置文件和所有磁盘都需要做快照保存
        disk_snapshot_list = []
        try:
            cnt = 1
            for disk_info in vm_disk:
                disk_uuid = disk_info['disk_uuid']
                disk_snapshot_name = '%s_0%s' % (snapshot_name, cnt)

                result = self.compute_driver.disk_snapshot_create(
                              token, disk_uuid, disk_snapshot_name)
                disk_snapshot_uuid = result['snapshot_uuid']
                disk_snapshot_info = {
                                         "disk_uuid": disk_uuid,
                                         "snapshot_uuid": disk_snapshot_uuid
                                     }
                disk_snapshot_list.append(disk_snapshot_info)
                cnt += 1
        except Exception, e:
            log.error('clouddisk create failure, reason=%s' % (e))
            for disk_snapshot_uuid in disk_snapshot_list:
                self.compute_driver.disk_snapshot_delete(
                     token, disk_snapshot_uuid)
            return request_result(511)

        snapshot_uuid = str(uuid.uuid4())

        try:
            self.compute_db.snapshot_create(
                 snapshot_uuid, snapshot_name, vm_uuid,
                 vm_ip, vm_cpu, vm_mem, vm_disk, vm_nic,
                 disk_snapshot_list, availzone_uuid,
                 availzone_name, comment,
                 team_uuid, project_uuid, user_uuid)
        except Exception, e:
            log.error('Database insert error, reason=%s' % (e))
            for disk_snapshot_uuid in disk_snapshot_list:
                self.compute_driver.disk_snapshot_delete(
                     token, disk_snapshot_uuid)
            return request_result(401)

        result = {
                     "snapshot_uuid": snapshot_uuid,
                     "snapshot_name": snapshot_name,
                     "vm_uuid": vm_uuid,
                     "vm_name": vm_name,
                     "resource_uuid": snapshot_uuid
                 }

        return request_result(0, result)

    def snapshot_list(self, user_uuid, team_uuid, team_priv,
                      project_uuid, project_priv, page_size,
                      page_num):

        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                snapshots_list_info = self.compute_db.snapshot_list_project(
                                           team_uuid, project_uuid,
                                           page_size, page_num)
            else:
                snapshots_list_info = self.compute_db.snapshot_list_user(
                                           team_uuid, project_uuid, user_uuid,
                                           page_size, page_num)

            snapshot_list = snapshots_list_info['snapshot_list']
            count = snapshots_list_info['count']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        result = {
                     "count": count,
                     "snapshot_list": snapshot_list
                 }

        return request_result(0, result)

    def snapshot_info(self, snapshot_uuid):

        try:
            snapshot_info = self.compute_db.snapshot_info(
                                 snapshot_uuid)['snapshot_info']
            snapshot_uuid = snapshot_info['snapshot_uuid']
            snapshot_name = snapshot_info['snapshot_name']
            vm_uuid = snapshot_info['vm_uuid']
            disk_snapshot = snapshot_info['disk_snapshot']
            availzone_uuid = snapshot_info['availzone_uuid']
            availzone_name = snapshot_info['availzone_name']
            comment = snapshot_info['comment']
            status = snapshot_info['status']
            create_time = snapshot_info['create_time']
            update_time = snapshot_info['update_time']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        result = {
                     "snapshot_uuid": snapshot_uuid,
                     "snapshot_name": snapshot_name,
                     "vm_uuid": vm_uuid,
                     "disk_snapshot": disk_snapshot,
                     "availzone_uuid": availzone_uuid,
                     "status": status,
                     "comment": comment,
                     "create_time": create_time,
                     "update_time": update_time
                 }

        return request_result(0, result)

    def snapshot_revert(self, snapshot_uuid,
                        token, source_ip, resource_uuid):

        try:
            snapshot_info = self.compute_db.snapshot_info(
                                 snapshot_uuid)['snapshot_info']
            snapshot_name = snapshot_info['snapshot_name']
            vm_uuid = snapshot_info['vm_uuid']
            vm_ip = snapshot_info['vm_ip']
            vm_cpu = snapshot_info['vm_cpu']
            vm_mem = snapshot_info['vm_mem']
            vm_disk = snapshot_info['vm_disk']
            vm_nic = snapshot_info['vm_nic']
            disk_snapshot = snapshot_info['disk_snapshot']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        # 判断是否满足快照恢复条件，即检查快照依赖的云硬盘和网卡
        # 是否仍然被快照vm所使用，并判断执行恢复的vm是否处于关闭状态
        try:
            cloudhost_info = self.compute_db.cloudhost_info(
                                  vm_uuid)['cloudhost_info']
            vm_name = cloudhost_info['vm_name']
            vm_vm_disk = cloudhost_info['vm_disk']
            vm_vm_nic = cloudhost_info['vm_nic']
            status = cloudhost_info['status']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        if status != 'off':
            log.warning('vm status is not off, snapshot revert denied, '
                        'vm_uuid=%s, vm_name=%s'
                        % (vm_uuid, vm_name))
            return request_result(202)

        for disk_info in vm_disk:
            if disk_info not in vm_vm_disk:
                disk_uuid = disk_info.get('disk_uuid')
                log.warning('vm disk %s is not used by vm %s, snapshot revert denied'
                            % (disk_uuid, vm_name))
                return request_result(202)

        for vnic_info in vm_nic:
            if vnic_info not in vm_vm_nic:
                vnic_uuid = vnic_info.get('vnic_uuid')
                log.warning('vm vnic %s is not used by vm %s, snapshot revert denied'
                            % (vnic_uuid, vm_name))
                return request_result(202)

        try:
            for disk_snapshot_info in disk_snapshot:
                disk_uuid = disk_snapshot_info.get('disk_uuid')
                disk_snapshot_uuid = disk_snapshot_info.get('snapshot_uuid')

                self.compute_driver.disk_snapshot_revert(
                     token, disk_snapshot_uuid)
                # 等待磁盘快照恢复返回结果
                self.compute_driver.disk_snapshot_revert_wait(
                     token, disk_uuid)
                log.info('Disk snapshot revert success, disk_uuid=%s, '
                         'snapshot_uuid=%s' % (disk_uuid, disk_snapshot_uuid))
        except Exception, e:
            log.error('Disk snapshot revert failure, disk_snapshot_uuid=%s, '
                      'snapshot_name=%s, reason=%s'
                      % (disk_snapshot_uuid, snapshot_name, e))
            return request_result(1501)

        try:
            self.compute_db.snapshot_revert(
                 vm_uuid, vm_ip, vm_cpu,
                 vm_mem, vm_disk, vm_nic)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        result = {
                     "snapshot_uuid": snapshot_uuid,
                     "snapshot_name": snapshot_name,
                     "vm_uuid": vm_uuid,
                     "vm_name": vm_name,
                     "resource_name": snapshot_name
                 }

        return request_result(0, result)

    def snapshot_delete(self, snapshot_uuid, token,
                        source_ip, resource_uuid):

        try:
            snapshot_info = self.compute_db.snapshot_info(
                                 snapshot_uuid)['snapshot_info']
            snapshot_name = snapshot_info['snapshot_name']
            disk_snapshot = snapshot_info['disk_snapshot']
        except Exception, e:
            log.error('Database select error, reason=%s' % (e))
            return request_result(404)

        try:
            for disk_snapshot_info in disk_snapshot:
                disk_snapshot_uuid = disk_snapshot_info.get('snapshot_uuid')
                self.compute_driver.disk_snapshot_delete(
                     token, disk_snapshot_uuid)
        except Exception, e:
            log.error('Disk snapshot delete failure, disk_snapshot_uuid=%s, '
                      'snapshot_name=%s, reason=%s'
                      % (disk_snapshot_uuid, snapshot_name, e))
            return request_result(501)

        try:
            self.compute_db.snapshot_delete(snapshot_uuid)
        except Exception, e:
            log.error('Database delete error, reason=%s' % (e))
            return request_result(402)

        result = {
                     "resource_name": snapshot_name
                 }

        return request_result(0, result)
