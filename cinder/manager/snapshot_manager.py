# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/7 14:29
from db.cinder_db import CinderDB
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time, parameters_check
from common.connect import connection
from driver.openstack_driver import OpenstackDriver
from driver.cinder_driver import CinderDriver
from common.ssh import exec_cmd
from common import conf
from rpcclient.status_driver import StatusDriver
from driver.qemu_driver import QemuDriver
from uuid import uuid4


class SnapshotManager(object):

    def __init__(self):
        self.conn = connection()
        self.db = CinderDB()
        self.status_update = StatusDriver()
        self.qemu = QemuDriver()

    def create(self, name, description, metadata, volume_uuid,
               team_uuid, project_uuid, user_uuid):

        """
        :param name:
        :param description:
        :param metadata: object
        :param volume_uuid:
        :param team_uuid:
        :param project_uuid:
        :param user_uuid:
        :return:"""
        try:
            op_result = self.conn.block_storage.\
                create_snapshot(name=name, description=description,
                                metadata=metadata, volume_id=volume_uuid,
                                is_forced=True)
            snapshot_uuid = op_result.id
            status = op_result.status
            metadata = op_result.metadata
            size = op_result.size
            is_forced = op_result.is_forced

        except Exception, e:
            log.error('create the snapshot(op) error, reason is: %s' % e)
            return request_result(1001)

        try:
            db_result = self.db.\
                snapshot_create(snapshot_uuid=snapshot_uuid,
                                name=name,
                                s_type = 'ordinary',
                                description=description,
                                status=status,
                                metadata=metadata,
                                size=size,
                                volume_uuid=volume_uuid,
                                is_forced=is_forced,
                                user_uuid=user_uuid,
                                project_uuid=project_uuid,
                                team_uuid=team_uuid)
        except Exception, e:
            log.error('create the snapshot(db) error, reason is: %s' % e)
            # rollback
            return request_result(401)

        log.info('op_result:%s, db_result: %s' % (op_result, db_result))
        self.status_update.snapshot_status(snapshot_uuid)
        return request_result(0,
                              {'snapshot_uuid': snapshot_uuid}
                              )

    def list(self, user_uuid, team_uuid, team_priv,
             project_uuid, project_priv, page_size, page_num, volume_uuid):
        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.snap_list_project(team_uuid,
                                                      project_uuid,
                                                      page_size,
                                                      page_num,
                                                      volume_uuid)

                db_count = self.db.snap_count_project(team_uuid,
                                                      project_uuid,
                                                      volume_uuid)
            else:
                db_result = self.db.snap_list(team_uuid,
                                              project_uuid,
                                              user_uuid,
                                              page_size,
                                              page_num,
                                              volume_uuid)

                db_count = self.db.snap_count(team_uuid,
                                              project_uuid,
                                              user_uuid,
                                              volume_uuid)
            count = db_count[0][0]
            if len(db_result) != 0:
                for snapshot in db_result:
                    snapshot_uuid = snapshot[0]
                    name = snapshot[1]
                    description = snapshot[2]
                    status = snapshot[3]
                    metadata = snapshot[4]
                    size = snapshot[5]
                    volume_uuid = snapshot[6]
                    is_forced = snapshot[7]
                    create_time = time_diff(snapshot[8])
                    ret.append({'snapshot_uuid': snapshot_uuid,
                                   'name': name,
                                   'description': description,
                                   'status': status,
                                   'metadata': metadata,
                                   'size': size,
                                   'volume_uuid': volume_uuid,
                                   'is_forced': is_forced,
                                   'create_time': create_time})
            result = {
                'count': count,
                'snapshot_list': ret
            }
            return request_result(0, result)

        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        # try:
        #     db_result = self.db.snapshot_list()
        # except Exception, e:
        #     log.error('get the snapshot(db) error, reason is: %s' % e)
        #     return request_result(403)

    def os_disks_snapshot_create(self, description, name, vm_uuid, metadata,
                                 user_uuid, team_uuid,
                                 project_uuid):
        snapshot_uuid = str(uuid4())
        # 系统盘快照
        if vm_uuid is not None:
            size = 0
            try:
                self.qemu.os_snap_create(vm_uuid, name)
            except Exception, e:
                log.error('create the osdisk snapshot error, '
                          'reason is: %s' % e)
                return request_result(1001)
            try:
                snap_info = self.qemu.os_snap_detail(vm_uuid)
                for i in snap_info:
                    log.info('get the size of the snapshot, '
                             'the items is: %s' % i)
                    if name in i:
                        size = i.split(' ')[1].rstrip()
                        log.info('get the size from qemu is: %s' % size)
                        size = int(size)
            except Exception, e:
                log.error('get the snap detail error, reason is: %s' % e)
                # rollback
                try:
                    self.qemu.os_snap_delete(name, vm_uuid)
                except Exception, e:
                    log.error('recovery the snapshot error, reason is: %s' % e)
                return request_result(1004)
            # 入库
            db_result = self.db. \
                snapshot_create(snapshot_uuid=snapshot_uuid,
                                name=name,
                                s_type='os_disk',
                                description=description,
                                status=None,
                                metadata=metadata,
                                size=size,
                                volume_uuid=vm_uuid,
                                is_forced=None,
                                user_uuid=user_uuid,
                                project_uuid=project_uuid,
                                team_uuid=team_uuid)
            log.info('insert to the database for the os snapshot '
                     'result is: %s' % db_result)
            return request_result(0, {'snapshot_uuid': snapshot_uuid})

        else:
            return request_result(101)
           

class SnapshotRouteManager(object):

    def __init__(self):
        self.db = CinderDB()
        self.conn = connection()
        self.op_driver = OpenstackDriver()
        self.cinder = CinderDriver()
        self.snapshot_manager = SnapshotManager()
        self.volume_pool = conf.volume_pool
        self.vms_pool = conf.vms_pool
        self.qemu = QemuDriver()

    def detail(self, snapshot_uuid):
        result = dict()
        try:
            db_result = self.db.snapshot_detail(snapshot_uuid)
        except Exception, e:
            log.error('get the snapshot detail(db) error, reason is: %s' % e)
            return request_result(403)

        if len(db_result) != 0:
            for snapshot in db_result:
                result['snapshot_uuid'] = snapshot[0]
                result['name'] = snapshot[1]
                result['description'] = snapshot[2]
                result['status'] = snapshot[3]
                result['metadata'] = snapshot[4]
                result['size'] = snapshot[5]
                result['volume_uuid'] = snapshot[6]
                result['is_forced'] = snapshot[7]
                result['create_time'] = time_diff(snapshot[8])
                result['s_type'] = snapshot[9]
        return request_result(0, result)

    def delete(self, snapshot_uuid):
        # get the type of the snap, check it if os_disk
        try:
            db_result = self.db.snapshot_detail(snapshot_uuid)
            name = db_result[0][1]
            description = db_result[0][2]
            metadata = db_result[0][4]
            volume_uuid = db_result[0][6]
            vm_uuid = db_result[0][6]
            s_type = db_result[0][9]
        except Exception, e:
            log.error('get the type of snap error, reason is: %s' % e)
            return request_result(403)
        if s_type == 'os_disk':
            try:
                self.qemu.os_snap_delete(name, vm_uuid)
            except Exception, e:
                log.error('delete os snapshot from ceph error, '
                          'reason is:%s' % e)
                return request_result(1003)
        else:
            # op delete
            try:
                self.conn.block_storage.\
                    delete_snapshot(snapshot_uuid)
            except Exception, e:
                log.error('delete the snapshot(op) error, reason is: %s' % e)
                return request_result(1003)

        # db delete
        try:
            self.db.snapshot_delete(snapshot_uuid)
        except Exception, e:
            log.error('delete the snapshot(db) error, reason is: %s' % e)
            # rollback
            try:
                if s_type == 'os_disk':
                    self.qemu.os_snap_create(vm_uuid, name)
                else:
                    self.conn.block_storage.\
                        create_snapshot(
                                name=name, description=description,
                                metadata=metadata, volume_id=volume_uuid,
                                is_forced=True)
            except Exception, e:
                log.error('rollback the snapshot(%s) error, '
                          'reason is: %s' % (snapshot_uuid, e))

            return request_result(404)

        return request_result(0, {'resource_uuid': snapshot_uuid})

    def logic_delete(self, snapshot_uuid):
        # op delete
        try:
            op_result = self.conn.block_storage. \
                delete_snapshot(snapshot_uuid)
        except Exception, e:
            log.error('delete the snapshot(op) error, reason is: %s' % e)
            return request_result(1003)

        try:
            db_result = self.db.snapshot_logic_delete(snapshot_uuid)
        except Exception, e:
            log.error('logic delete the snapshot(db) error, reason is: %s' % e)
            return request_result(404)
        log.info('logic delete the snapshot op_result is: %s, '
                 'db_result is: %s' % (op_result, db_result))
        return request_result(0, {'resource_uuid': snapshot_uuid})

    def recovery_msg_ready(self, snapshot_uuid):
        # 数据库查询信息
        result = dict()
        try:
            snapshot_db_detail = self.db.\
                snapshot_recovery_msg_get(snapshot_uuid)
            if len(snapshot_db_detail) == 0:
                log.error('have no message in database of '
                          '%s' % snapshot_uuid)
                return request_result(1001)
            result['name'] = snapshot_db_detail[0][0]
            result['description'] = snapshot_db_detail[0][1]
            result['metadata'] = snapshot_db_detail[0][2]
            result['size'] = snapshot_db_detail[0][3]
            result['volume_uuid'] = snapshot_db_detail[0][4]
            result['user_uuid'] = snapshot_db_detail[0][5]
            result['project_uuid'] = snapshot_db_detail[0][6]
            result['team_uuid'] = snapshot_db_detail[0][7]
        except Exception, e:
            log.error('get the message of snapshot(%s) '
                      'from db error, reason is: %s' % snapshot_uuid)
            raise Exception(e)
        return result

    def update(self, up_dict, snapshot_uuid, volume_uuid):
        if up_dict.get('up_type') == 'revert':
            return self.revert(snapshot_uuid, volume_uuid)
        if up_dict.get('up_type') == 'recovery':
            # 获取信息
            try:
                param = self.recovery_msg_ready(snapshot_uuid)
            except Exception, e:
                log.error('get the message from db error, reason is: %s' % e)
                return request_result(403)

            name = param.get('name')
            description = param.get('description')
            # metadata = param.get('metadata')
            # if metadata == 'None':
            #     metadata = None
            volume_uuid = param.get('volume_uuid')
            user_uuid = param.get('user_uuid')
            project_uuid = param.get('project_uuid')
            team_uuid = param.get('team_uuid')

            # 恢复snapshot
            op_result = self.snapshot_manager.create(name=name,
                                                     description=description,
                                                     volume_uuid=volume_uuid,
                                                     metadata=None,
                                                     team_uuid=team_uuid,
                                                     project_uuid=project_uuid,
                                                     user_uuid=user_uuid)
            if op_result.get('status') != 0:
                return request_result(1001)

            # 删除原来的snapshot及权限信息
            del_snap = self.delete(snapshot_uuid)
            if del_snap.get('status') != 0:
                return del_snap

            return op_result

        else:
            op_token = self.op_driver.get_token(conf.op_user, conf.op_pass)
            if op_token.get('status') != 0:
                return op_token

            token = op_token.get('result').get('token')
            up_dict['snapshot_uuid'] = snapshot_uuid
            result = self.cinder.update_snapshot(token, up_dict)
            if result.get('status') != 0:
                return result

            # update db
            try:
                db_result = self.db.snapshot_update(up_dict, snapshot_uuid)
            except Exception, e:
                log.error('update the snapshot(db) error, reason is: %s' % e)
                return request_result(402)
            log.debug('update the snapshot(db) result is: %s' % db_result)
            return request_result(0, {'resource_uuid': snapshot_uuid})

    def revert(self, snapshot_uuid, volume_uuid):
        # select the volume_uuid which is the snapshot belong to
        # if volume_uuid is None:
        #     try:
        #         volume_uuid = self.db.volume_uuid_from_snap(
        #             snapshot_uuid
        #         )[0][0]
        #     except Exception, e:
        #         log.error('get the volume_uuid(db) error, reason is: %s' % e)
        #         return request_result(403)

        # if volume_uuid == 'osdisk':
        #     try:
        #         statement = "%s -a snapshot-%s rbd:%s/%s_disk" % (
        #                     'qemu-img snapshot',
        #                     snapshot_uuid,
        #                     self.vms_pool,
        #                     volume_uuid)
        #         exec_cmd(statement)
        #     except Exception, e:
        #         log.error('exec the cmd(%s) error, reason is: %s' % e)
        #         return request_result(602)

        # revert the volume to the snapshot point
        try:
            db_result = self.db.snapshot_detail(snapshot_uuid)
            name = db_result[0][1]
            volume_uuid = db_result[0][6]
            vm_uuid = db_result[0][6]
            s_type = db_result[0][9]
        except Exception, e:
            log.error('get the detail of the snap error, reason is: %s' % e)
            return request_result(403)

        if s_type == 'os_disk':
            try:
                self.qemu.os_snap_revert(name, vm_uuid)
            except Exception, e:
                log.error('revert the os disk(%s) error, '
                          'reason is: %s' % (vm_uuid, e))
                return request_result(602)
        else:
            try:
                self.qemu.snap_revert(snapshot_uuid, volume_uuid)
            except Exception, e:
                log.error('revert the disk(%s) error, reason is: %s' % (name,
                                                                        e))
                return request_result(602)
        # try:
        #     statement = "%s -a snapshot-%s rbd:%s/volume-%s" % (
        #                  'qemu-img snapshot',
        #                  snapshot_uuid,
        #                  self.volume_pool,
        #                  volume_uuid)
        #     exec_cmd(statement)
        # except Exception, e:
        #     log.error('exec the cmd(%s) error, reason is: %s' % e)
        #     return request_result(602)

        # delete the snapshot which create after the snapshot used just now
        # first: get the list
        ######### delete later ########
        # try:
        #     snaps = self.db.get_snaps_after_one(name, volume_uuid, s_type)
        #     log.info('get the the snaps after %s is: %s' % (volume_uuid,
        #                                                     snaps))
        #     if len(snaps) == 0:
        #         return request_result(0)
        #     else:
        #         for snap in snaps:
        #             log.info('snap revert,operate the snap is: %s' % snap)
        #             result = self.delete(snap[0])
        #             if result.get('status') != 0:
        #                 raise Exception('delete the snapshot which create '
        #                                 'after the snapshot used error')
        # except Exception, e:
        #     log.error('delete snapshot error,reason is: %s' % e)
        #     return request_result(1003)
        return request_result(0)
