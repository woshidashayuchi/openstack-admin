# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/8 10:20
from db.cinder_db import CinderDB
from driver.cinder_driver import CinderDriver
# from driver.auth_driver import get_token
from common.logs import logging as log
from common.request_result import request_result
from common.skill import time_diff, use_time
from common import conf
from driver.openstack_driver import OpenstackDriver
import time


class VolumeManager(object):
    def __init__(self):
        self.op_driver = OpenstackDriver()
        self.db = CinderDB()

    # size <size>
    #     Volume size in GB(Required unless –snapshot or –source or
    #     –source - replicated is specified)
    # type <volume-type>
    #     Set the type of volume
    #     Select < volume - type > from the available types as shown
    #     by volume type list.
    # image <image>
    #     Use <image> as source of volume(name or ID)
    #     This is commonly used to create a boot volume for a server.
    # snapshot <snapshot>
    #     Use < snapshot > as source of volume(name or ID)
    # source <volume>
    #     Volume to clone(name or ID)
    # source-replicated <replicated-volume>
    #     Replicated volume to clone(name or ID)
    # description <description>
    #     Volume description
    # user <user>
    #     Specify an alternate user(name or ID)
    # project <project>
    #     Specify an alternate project(name or ID)
    # availability-zone <availability-zone>
    #     Create volume in <availability-zone>
    # consistency - group < consistency - group >
    #     Consistency group where the new volume belongs to
    # property < key = value >
    #     Set a property on this volume(repeat option to set
    #     multiple properties)
    # hint < key = value >
    #     Arbitrary scheduler hint key-value pairs to help boot
    #     an instance(repeat option to set multiple hints)
    # multi-attach
    #     Allow volume to be attached more than once(default to False)
    # bootable
    #     Mark volume as bootable
    # non-bootable
    #     Mark volume as non - bootable(default)
    # read-only
    #     Set volume to read-only access mode
    # read-write Set volume to read-write access mode(default)
    # <name> Volume name

    def create(self, name, size, description, v_type, conn_to=None,
               snapshot_uuid=None, is_use_domain=None, is_start=0,
               is_secret=0, source_volume_uuid=None, image_uuid=None,
               user_uuid=None, project_uuid=None, team_uuid=None):
        '''
          Parameter
          :param name: 存储卷名称
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
          :return: volume_uuid
        '''
        # 获取snapshot的相关信息
        op_result = self.op_driver.volume_create(size=size,
                                                 name=name,
                                                 v_type=v_type,
                                                 description=description,
                                                 snapshot_uuid=snapshot_uuid,
                                                 source_volume_uuid=
                                                 source_volume_uuid,
                                                 image_uuid=image_uuid)

        if op_result.get('status') != 200:
            return op_result
        if snapshot_uuid is not None:
            size = op_result.get('result').get('size')
        if image_uuid is not None:
            is_start = 1
        try:
            db_result = self.db.volume_create(name=name,
                                              size=size,
                                              description=description,
                                              v_type=v_type,
                                              conn_to=conn_to,
                                              snapshot_uuid=snapshot_uuid,
                                              source_volume_uuid=
                                              source_volume_uuid,
                                              is_start=is_start,
                                              is_use_domain=is_use_domain,
                                              image_uuid=image_uuid,
                                              is_secret=is_secret,
                                              user_uuid=user_uuid,
                                              team_uuid=team_uuid,
                                              project_uuid=project_uuid,
                                              volume_uuid=op_result.
                                              get('result').get('id'))
        except Exception, e:
            log.error('create the volume(db) error, reason is: %s' % e)
            return request_result(401)

        log.info('op: %s, db: %s' % (op_result, db_result))

        return request_result(200, {'resource_uuid':
                                        op_result.get('result').get('id')})

    def list(self, user_uuid, team_uuid, team_priv,
             project_uuid, project_priv, page_size, page_num):

        result = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
               or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.volume_list_project(team_uuid,
                                                        project_uuid,
                                                        page_size,
                                                        page_num)
            else:
                db_result = self.db.volume_list(team_uuid,
                                                project_uuid,
                                                user_uuid,
                                                page_size,
                                                page_num)

        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)

        # try:
        #     db_result = self.db.volume_list(user_uuid)
        # except Exception, e:
        #     log.error('get the volume list(db) error, reason is: %s' % e)
        #     return request_result(403)

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
                result.append({'volume_uuid': volume_uuid,
                               'name': name,
                               'description': description,
                               'size': size,
                               'status': status,
                               'type': v_type,
                               'conn_to': conn_to,
                               'snapshot_uuid': snapshot_uuid,
                               'source_volume_uuid': source_volume_uuid,
                               'image_uuid': image_uuid,
                               'is_use_domain': is_use_domain,
                               'is_start': is_start,
                               'is_secret': is_secret,
                               'create_time': create_time})

        return request_result(200, result)

    def logic_delete(self, volume_uuid):
        pass

    def delete(self, volume_uuid):
        pass


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
        except Exception, e:
            log.error('get the snapshot for the volume(%s) error, '
                      'reason is: %s' % (volume_uuid, e))
            return
        log.info('if can delete check , the db_result:%s' % db_result[0][0])
        if db_result[0][0] != 0:
            return False
        else:
            return True

    # 逻辑删除
    # 即：只是不再展现于页面
    def logic_delete(self, volume_uuid):
        # update the volume show status from database
        try:
            db_result = self.db.volume_logic_update(volume_uuid)
        except Exception, e:
            log.error('logic delete the volume(db) error, reason is: %s' % e)
            return request_result(402)

        log.info('db: %s' % db_result)
        return request_result(200, 'the volume is logic deleted')

    # 物理删除
    # 即: 删除所有的
    def delete(self, volume_uuid):
        # 如果待删除的存储卷有快照依赖，禁止删除
        del_check = self.if_can_delete(volume_uuid)
        if del_check is False:
            return request_result(604)

        # delete the volume from op
        op_result = self.op_driver.volume_delete(volume_uuid)
        if op_result.get('status') != 200:
            return op_result

        # delete db
        try:
            db_result = self.db.volume_delete(volume_uuid)
        except Exception, e:
            log.error('delete the volume(db) error, reason is: %s' % e)
            return request_result(404)

        log.info('op_result: %s, db_result: %s' % (op_result, db_result))
        return request_result(200, {'volume_uuid': volume_uuid})

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
                result['type'] = volume[5]
                result['conn_to'] = volume[6]
                result['is_use_domain'] = volume[7]
                result['is_start'] = volume[8]
                result['is_secret'] = volume[9]
                result['snapshot_uuid'] = volume[10]
                result['source_volume_uuid'] = volume[11]
                result['image_uuid'] = volume[12]
                result['create_time'] = time_diff(volume[13])

        return request_result(200, result)

    def update(self, up_dict, volume_uuid):
        # update volume(op)
        op_token = self.op_driver.get_token(self.op_user,
                                            self.op_pass)
        if op_token.get('status') != 200:
            return op_token

        token = op_token.get('result').get('token')
        up_dict['volume_uuid'] = volume_uuid
        result = self.cinder.update_volume(token, up_dict)
        if result.get('status') != 200:
            return result

        # update volume(db)
        try:
            self.db.volume_update(up_dict, volume_uuid)
        except Exception, e:
            log.error('update the database error, reason is: %s' % e)
            return request_result(402)

        return request_result(200, {'resource_uuid': volume_uuid})


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
                    break
                op_status = op_result.get('result')
                if status != op_status:
                    # update the status
                    try:
                        db.volume_status_update(volume_uuid, op_status)
                    except Exception, e:
                        log.error('update the database error, '
                                  'reason is: %s' % e)
                        break
                    update_num += 1
            all_num += 1
            log.info('done update times: %d, '
                     'done all check times: %d' % (update_num,
                                                      all_num))
            time.sleep(5)
