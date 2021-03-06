# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/8 10:20
from db.cinder_db import CinderDB
from driver.cinder_driver import CinderDriver
# from driver.auth_driver import get_token
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff
from common import conf
from driver.openstack_driver import OpenstackDriver
from rpcclient.status_driver import StatusDriver
import time


class VolumeManager(object):
    def __init__(self):
        self.op_driver = OpenstackDriver()
        self.status_update = StatusDriver()
        self.db = CinderDB()

    def osdisk_create(self, name, volume_uuid, v_type, image_uuid,
                      size, conn_to, user_uuid, project_uuid, team_uuid,
                      description='os_volume', source_volume_uuid=None,
                      snapshot_uuid=None, is_use_domain=None,
                      is_start=1, is_secret=0):
        log.debug(size)
        try:
            size = self.op_driver.image_size(image_uuid)
        except Exception, e:
            log.error('get the image size error, reason is: %s' % e)
            return request_result(1204)
        try:
            db_result = self.db.\
                volume_create(name=name,
                              size=size,
                              description=description,
                              v_type=v_type,
                              conn_to=conn_to,
                              snapshot_uuid=snapshot_uuid,
                              source_volume_uuid=source_volume_uuid,
                              is_start=is_start,
                              is_use_domain=is_use_domain,
                              image_uuid=image_uuid,
                              is_secret=is_secret,
                              user_uuid=user_uuid,
                              team_uuid=team_uuid,
                              project_uuid=project_uuid,
                              volume_uuid=volume_uuid)
            if db_result is not None:
                return request_result(401)
        except Exception, e:
            log.error('create the volume(db) error, reason is: %s' % e)
            return request_result(401)
        return request_result(0, {'resource_uuid': volume_uuid})

    def create(self, name, size, description, v_type, conn_to=None,
               snapshot_uuid=None, is_use_domain=None, is_start=0,
               is_secret=0, source_volume_uuid=None, image_uuid=None,
               user_uuid=None, project_uuid=None, team_uuid=None):
        """:param name: 存储卷名称
        :param size: Volume size in GB
        :param description: Volume description
        :param v_type: Set the type of volume
                       Select < volume - type > from the available types as
                       shown by volume type list.
        :param conn_to:
        :param snapshot_uuid: 如果不为None,则通过卷快照创建卷
        :param source_volume_uuid: 如果不为None,则通过已存在卷创建新卷，相当于copy
        :param is_use_domain: availability-zone
        :param is_start: Mark volume as bootable
        :param is_secret: 加密
        :param image_uuid:
        :param user_uuid
        :param project_uuid
        :param team_uuid
        :return: volume_uuid """
        # 判断是否重名
        try:
            db_count = self.db.volume_name_check(name, team_uuid,
                                                 project_uuid, user_uuid)
            if db_count[0][0] != 0:
                return request_result(302)
        except Exception, e:
            log.error('check the name if used error, reason is: %s' % e)
            return request_result(403)

        # get the volume type
        try:
            if v_type not in ('ssd', 'hdd'):
                v_type = 'hdd'
            type_uuids = self.db.vol_type_detail(v_type)
            type_uuid = type_uuids[0][0]
            type_name = type_uuids[0][1]
            log.info('the volume type uuid is: %s, name is: %s' % (type_uuid,
                                                                   name))
        except Exception, e:
            log.error('get the volume type error, reason is: %s' % e)
            return request_result(403)

        op_result = self.op_driver.\
            volume_create(size=size,
                          name=name,
                          v_type=type_name,
                          description=description,
                          snapshot_uuid=snapshot_uuid,
                          source_volume_uuid=source_volume_uuid,
                          image_uuid=image_uuid)

        if op_result.get('status') != 0:
            return op_result
        if snapshot_uuid is not None:
            size = op_result.get('result').get('size')
        if image_uuid is not None:
            is_start = 1
        try:
            volume_uuid = op_result.get('result').get('id')
            db_result = self.db.\
                volume_create(name=name,
                              size=size,
                              description=description,
                              v_type=v_type,
                              conn_to=conn_to,
                              snapshot_uuid=snapshot_uuid,
                              source_volume_uuid=source_volume_uuid,
                              is_start=is_start,
                              is_use_domain=is_use_domain,
                              image_uuid=image_uuid,
                              is_secret=is_secret,
                              user_uuid=user_uuid,
                              team_uuid=team_uuid,
                              project_uuid=project_uuid,
                              volume_uuid=volume_uuid)
        except Exception, e:
            log.error('create the volume(db) error, reason is: %s' % e)
            # rollback
            rollback = self.op_driver.\
                volume_delete(op_result.get('result').get('id'))
            log.info('rollback when create error the result is: %s' % rollback)
            return request_result(401)

        log.info('op: %s, db: %s' % (op_result, db_result))
        # 异步状态更新
        self.status_update.volume_status(volume_uuid)
        return request_result(0, {'resource_uuid':
                                  op_result.get('result').get('id')})

    def list(self, user_uuid, team_uuid, team_priv,
             project_uuid, project_priv, page_size, page_num):

        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.volume_list_project(team_uuid,
                                                        project_uuid,
                                                        page_size,
                                                        page_num)
                db_count = self.db.volume_count_project(team_uuid,
                                                        project_uuid)
                log.info('get the count from db is: %s' % db_count)
                count = db_count[0][0]
            else:
                db_result = self.db.volume_list(team_uuid,
                                                project_uuid,
                                                user_uuid,
                                                page_size,
                                                page_num)
                db_count = self.db.volume_count(team_uuid,
                                                project_uuid,
                                                user_uuid)
                log.info('get the count from db is: %s' % db_count)
                count = db_count[0][0]
        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        # try:
        #     db_result = self.db.volume_list(user_uuid)
        # except Exception, e:
        #     log.error('get the volume list(db) error, reason is: %s' % e)
        #     return request_result(403)
        try:
            if len(db_result) != 0:
                for volume in db_result:
                    volume_uuid = volume[0]
                    name = volume[1]
                    description = volume[2]
                    size = volume[3]
                    status = volume[4]
                    v_type = volume[5]
                    conn_to = volume[6]
                    is_use_domain = volume[7]
                    is_start = volume[8]
                    is_secret = volume[9]
                    snapshot_uuid = volume[10]
                    source_volume_uuid = volume[11]
                    image_uuid = volume[12]
                    create_time = time_diff(volume[13])
                    update_time = time_diff(volume[14])
                    ret.append({'volume_uuid': volume_uuid,
                                'name': name,
                                'description': description,
                                'size': size,
                                'status': status,
                                'v_type': v_type,
                                'conn_to': conn_to,
                                'snapshot_uuid': snapshot_uuid,
                                'templet_uuid': source_volume_uuid,
                                'image_uuid': image_uuid,
                                'is_use_domain': is_use_domain,
                                'is_start': is_start,
                                'is_secret': is_secret,
                                'create_time': create_time,
                                'update_time': update_time})

            result = {
                'count': count,
                'volumes_list': ret
            }
        except Exception, e:
            log.error('explain the db result error, reason is: %s' % e)
            return request_result(403)

        return request_result(0, result)

    def list_cloudhost_volumes(self, cloudhost_uuid, page_size, page_num):
        ret = []

        try:
            db_result = self.db.list_cloudhost_volumes(cloudhost_uuid,
                                                       page_size,
                                                       page_num)
            db_count = self.db.count_cloudhost_volumes(cloudhost_uuid)
            count = db_count[0][0]
            if len(db_result) != 0:
                for vol in db_result:
                    ret.append({
                        'volume_uuid': vol[0],
                        'name': vol[1],
                        'size': vol[2],
                        'status': vol[3]
                    })
            result = {
                'count': count,
                'volumes_list': ret
            }
        except Exception, e:
            log.error('get the volumes which is used by cloudhost(db) '
                      'error, reason is: %s' % e)
            return request_result(403)

        return request_result(0, result)


class VolumeRouteManager(object):

    def __init__(self):
        self.op_driver = OpenstackDriver()
        self.db = CinderDB()
        self.cinder = CinderDriver()
        self.op_user = conf.op_user
        self.op_pass = conf.op_pass

    # --force
    #     Attempt forced removal of volume(s), regardless of state(defaults to
    #     False)
    # --purge
    #     Remove any snapshots along with volume(s)(defaults to False)
    #     Volume version 2 only
    # <volume>
    #     Volume(s) to delete(name or ID): this use ID
    def if_can_delete(self, volume_uuid):
        try:
            db_result = self.db.volume_if_can_delete(volume_uuid)
            if_as_templet = self.db.volume_if_as_templet(volume_uuid)
            attach_info = self.db.get_attachment_info(volume_uuid)
        except Exception, e:
            log.error('check if can delete the  volume(%s) error, '
                      'reason is: %s' % (volume_uuid, e))
            return
        if (db_result[0][0] != 0) or (len(attach_info) != 0) or (if_as_templet[0][0] != 0):
            log.warning('can\'t delete the volume(%s)' % volume_uuid)
            return False
        else:
            return True

    # 逻辑删除
    # 即：只是不再展现于页面
    def logic_delete(self, volume_uuid):
        # check if can be delete
        del_check = self.if_can_delete(volume_uuid)
        if del_check is False:
            return request_result(604)

        # update the volume show status from database
        try:
            db_result = self.db.volume_logic_update(volume_uuid)
        except Exception, e:
            log.error('logic delete the volume(db) error, reason is: %s' % e)
            return request_result(402)

        log.info('db: %s' % db_result)
        return request_result(0, 'the volume is logic deleted')

    # 物理删除
    # 即: 删除所有的
    def delete(self, volume_uuid):
        # 如果待删除的存储卷有快照依赖或者正在使用，禁止删除
        del_check = self.if_can_delete(volume_uuid)
        if del_check is False:
            return request_result(604)

        try:
            db_result = self.db.volume_delete(volume_uuid)
        except Exception, e:
            log.error('logic delete the volume(db) error, reason is: %s' % e)
            return request_result(402)

        # delete the volume from op
        op_result = self.op_driver.volume_delete(volume_uuid)
        if op_result.get('status') != 0:
            self.db.volume_rollback(volume_uuid)
            return op_result

        # delete db
        # try:
        #     db_result = self.db.volume_delete(volume_uuid)
        # except Exception, e:
        #     log.error('delete the volume(db) error, reason is: %s' % e)
        #     return request_result(404)

        log.info('op_result: %s, db_result: %s' % (op_result, db_result))
        return request_result(0, {'volume_uuid': volume_uuid})

    def detail(self, volume_uuid):
        result = dict()
        try:
            db_result = self.db.volume_detail(volume_uuid)
        except Exception, e:
            log.error('get the volume detail(db) error, reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for volume in db_result:
                result['volume_uuid'] = volume[0]
                result['name'] = volume[1]
                result['description'] = volume[2]
                result['size'] = volume[3]
                result['status'] = volume[4]
                result['v_type'] = volume[5]
                result['conn_to'] = volume[6]
                result['is_use_domain'] = volume[7]
                result['is_start'] = volume[8]
                result['is_secret'] = volume[9]
                result['snapshot_uuid'] = volume[10]
                result['templet_uuid'] = volume[11]
                result['image_uuid'] = volume[12]
                result['create_time'] = time_diff(volume[13])

        return request_result(0, result)

    def update(self, up_dict, volume_uuid):
        # update volume(op)
        op_token = self.op_driver.get_token(self.op_user,
                                            self.op_pass)
        if op_token.get('status') != 0:
            return op_token

        token = op_token.get('result').get('token')
        up_dict['volume_uuid'] = volume_uuid
        result = self.cinder.update_volume(token, up_dict)
        if result.get('status') != 0:
            return result

        # update volume(db)
        try:
            self.db.volume_update(up_dict, volume_uuid)
        except Exception, e:
            log.error('update the database error, reason is: %s' % e)
            return request_result(402)

        return request_result(0, {'resource_uuid': volume_uuid})

    def osdisk_delete(self, volume_uuid):
        # try:
        #     self.db.volume_delete(volume_uuid)
        # except Exception, e:
        #     log.error('delete the osdisk error, reason is: %s' % e)
        #     return request_result(404)
        try:
            db_ret = self.db.get_attachment_info(volume_uuid)
            if len(db_ret) != 0:
                attachment_uuid = db_ret[0][0]
                # server_uuid = db_ret[0][1]
            else:
                log.warning('don\'t have this volume(%s) attachment' 
                            'msg' % volume_uuid)
                return request_result(0)
        except Exception, e:
            log.error('get the attachment uuid error, reason is: %s' % e)
            return request_result(403)

        try:
            self.db.attachment_delete(attachment_uuid, None)
        except Exception, e:
            log.error('delete the attachment error, reason is: %s' % e)
            return request_result(402)
        return request_result(0, {'resource_uuid': volume_uuid})


# 清除过期存储卷
def volume_expire_delete():
    db = CinderDB()
    num = 0
    while True:
        try:
            db_result = db.volume_expire_list()
        except Exception, e:
            log.error('get the expire volume error, reason is: %s' % e)
            continue

        if len(db_result) == 0:
            continue
        else:
            for volume in db_result:
                volume_uuid = volume[0]
                try:
                    db.volume_delete(volume_uuid)
                except Exception, e:
                    log.error('delete the expire volume error, '
                              'reason is: %s' % e)
                    continue
                num += 1
        log.info('本次共清除过期存储卷%d个' % num)
        time.sleep(120)


# 动态更新存储卷状态与op环境一致
def volume_status_monitor():
    db = CinderDB()
    op = OpenstackDriver()
    update_num = 0
    all_num = 0
    while True:
        # get all volume
        try:
            db_result = db.volume_status_monitor()
        except Exception, e:
            log.error('get the all volumes(db) error, reason is: %s' % e)
            time.sleep(2)
            continue

        if len(db_result) == 0:
            time.sleep(2)
            continue

        else:
            for volume in db_result:
                volume_uuid = volume[0]
                status = volume[1]
                # get the status from op
                try:
                    op_result = op.volume_detail(volume_uuid)
                except Exception, e:
                    log.error('get the volume status(op) error, '
                              'reason is: %s' % e)
                    continue
                op_status = op_result.get('result')
                if status != op_status:
                    # update the status
                    try:
                        db.volume_status_update(volume_uuid, op_status)
                    except Exception, e:
                        log.error('update the database error, '
                                  'reason is: %s' % e)
                        continue
                    update_num += 1
            all_num += 1
            log.info('done update times: %d, '
                     'done all check times: %d' % (update_num,
                                                   all_num))
            time.sleep(5)


# 清除删除痕迹
def volume_del_mark_clean():
    op = OpenstackDriver()
    db = CinderDB()
    while True:
        # 查询数据库中不予以展现的volume列表
        try:
            db_result = db.volume_list_clean()
        except Exception, e:
            log.error('SERVICE(volume del mark clean)：GET THE VOLUME LIST '
                      'FROM DB ERROR, REASON IS: %s' % e)
            continue
        if len(db_result) == 0:
            continue
        for ret in db_result:
            volume_uuid = ret[0]
            op_result = op.volume_detail(volume_uuid)
            if op_result.get('status') != 0:
                continue
        time.sleep(20)
