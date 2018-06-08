# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/6/5 16:45
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


class TempletManager(object):
    def __init__(self):
        self.db = CinderDB()
        self.status_driver = StatusDriver()
        self.op_driver = OpenstackDriver()

    def templet_create(self, name, description, source_volume_uuid,
                       user_uuid, project_uuid, team_uuid):

        op_result = self.op_driver. \
            volume_create(size=None,
                          name=name,
                          v_type=None,
                          description=description,
                          snapshot_uuid=None,
                          source_volume_uuid=source_volume_uuid,
                          image_uuid=None)

        if op_result.get('status') != 0:
            return op_result

        try:
            templet_uuid = op_result.get('result').get('id')
            size = op_result.get('result').get('size')
            status = op_result.get('result').get('status')
            self.db.templet_create(templet_uuid, name, description,
                                   source_volume_uuid, team_uuid,
                                   project_uuid, user_uuid, size,
                                   status)
        except Exception, e:
            log.error('templet insert into db error, reason is: %s' % e)
            return request_result(401)
        self.status_driver.templet_status(templet_uuid)
        return request_result(0, {'resource_uuid': templet_uuid})

    def list_templets(self, user_uuid, team_uuid, team_priv, project_uuid,
                      project_priv, page_size, page_num):
        ret = []
        try:
            if ((project_priv is not None) and ('R' in project_priv)) \
                    or ((team_priv is not None) and ('R' in team_priv)):
                db_result = self.db.templet_list_project(team_uuid,
                                                         project_uuid,
                                                         page_size,
                                                         page_num)
                db_count = self.db.templet_count_project(team_uuid,
                                                         project_uuid)
                log.info('get the count from db is: %s' % db_count)
                count = db_count[0][0]
            else:
                db_result = self.db.templet_list(team_uuid,
                                                 project_uuid,
                                                 user_uuid,
                                                 page_size,
                                                 page_num)
                db_count = self.db.templet_count(team_uuid,
                                                 project_uuid,
                                                 user_uuid)
                log.info('get the count from db is: %s' % db_count)
                count = db_count[0][0]

            if len(db_result) != 0:
                for templet in db_result:
                    ret.append({
                        'templet_uuid': templet[0],
                        'name': templet[1],
                        'description': templet[2],
                        'source_volume_uuid': templet[3],
                        'size': templet[6],
                        'status': templet[7],
                        'type': templet[8],
                        'create_time': time_diff(templet[4]),
                        'update_time': time_diff(templet[5])
                    })
            result = {
                'count': count,
                'templets_list': ret
            }
        except Exception, e:
            log.error('Database select error, reason=%s' % e)
            return request_result(403)
        return request_result(0, result)


class TempletRouterManager(object):
    def __init__(self):
        self.db = CinderDB()
        self.status_driver = StatusDriver()
        self.op_driver = OpenstackDriver()

    def templet_detail(self, templet_uuid):
        result = dict()
        try:
            db_result = self.db.templet_detail(templet_uuid)
            for templet in db_result:
                result['templet_uuid'] = templet_uuid
                result['name'] = templet[1]
                result['description'] = templet[2]
                result['source_volume_uuid'] = templet[3]
                result['size'] = templet[6]
                result['type'] = templet[7]
                result['status'] = templet[8]
                result['create_time'] = time_diff(templet[4])
                result['update_time'] = time_diff(templet[5])
        except Exception, e:
            log.error('get the templet(%s) detail(db) error, '
                      'reason is: %s' % (templet_uuid, e))
            return request_result(403)
        return request_result(0, result)

    def templet_delete(self, templet_uuid):
        try:
            self.db.templet_delete(templet_uuid)
        except Exception, e:
            log.error('delete the templet(%s) error, '
                      'reason is: %s' % (templet_uuid, e))
            return request_result(404)
        op_result = self.op_driver.volume_delete(templet_uuid)
        if op_result.get('status') != 0:
            return op_result

        return request_result(0, templet_uuid)

    def templet_update(self, templet_uuid, name=None, description=None,
                       user_uuid=None, project_uuid=None, team_uuid=None):
        if name is None and description is None:
            return request_result(0, templet_uuid)
        if name is None and description is not None:
            try:
                self.db.templet_update(templet_uuid, name, description)
            except Exception, e:
                log.error('update the templet(db) error, reason is: %s' % e)
                return request_result(402)
            return request_result(0, templet_uuid)
        if name is not None:
            try:
                db_count = self.db.volume_name_check(name, team_uuid,
                                                     project_uuid, user_uuid)
                if db_count[0][0] != 0:
                    return request_result(302)
            except Exception, e:
                log.error('check the name if used error, reason is: %s' % e)
                return request_result(403)

            op_result = self.op_driver. \
                volume_create(size=None,
                              name=name,
                              v_type=None,
                              description=description,
                              snapshot_uuid=None,
                              source_volume_uuid=templet_uuid,
                              image_uuid=None)
            if op_result.get('status') != 0:
                return op_result
            else:
                size = op_result.get('result').get('size')
                volume_uuid = op_result.get('result').get('id')
                try:
                    v_type = self.db.templet_detail(templet_uuid)[0][7]
                except Exception, e:
                    log.error('get the type of templet error, reason is: '
                              '%s' % e)
                    # rollback
                    self.op_driver.volume_delete(volume_uuid)
                    return request_result(601)
            try:

                db_result = self.db. \
                    volume_create(name=name,
                                  size=size,
                                  description=description,
                                  v_type=v_type,
                                  conn_to=None,
                                  snapshot_uuid=None,
                                  source_volume_uuid=templet_uuid,
                                  is_start=0,
                                  is_use_domain=0,
                                  image_uuid=None,
                                  is_secret=0,
                                  user_uuid=user_uuid,
                                  team_uuid=team_uuid,
                                  project_uuid=project_uuid,
                                  volume_uuid=volume_uuid)
                self.status_driver.volume_status(volume_uuid)
            except Exception, e:
                log.error('create the volume from templet error, '
                          'reason is: %s' % e)
                return request_result(401)

            return request_result(0, volume_uuid)
