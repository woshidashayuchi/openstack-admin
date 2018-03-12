# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
from driver.cinder_driver import CinderDriver
# from driver.auth_driver import get_token
from common.token_auth import token_auth
from common.logs import logging as log
from common.request_result import request_result
from common.acl import acl_check, acl_check_uuids
from common.parameters import parameter_check
from volume_manager import VolumeManager, VolumeRouteManager
from snapshot_manager import SnapshotManager, SnapshotRouteManager


class CinderManager(object):
    def __init__(self):
        self.v_manager = VolumeManager()
        self.snap_manager = SnapshotManager()

    @acl_check('storage')
    def volume_create(self, context, name, size, description, v_type,
                      conn_to=None, is_use_domain=None, is_start=0,
                      is_secret=0):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            log.debug('the token is: %s, source_ip is: %s, user_uuid is: %s,'
                      'team_uuid is: %s, project_uuid is: %s' % (token,
                                                                 source_ip,
                                                                 user_uuid,
                                                                 team_uuid,
                                                                 project_uuid))
            parameter_check(name, ptype='pnam')
            parameter_check(size, ptype='psiz')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        result = self.v_manager.create(name=name,
                                       size=size,
                                       is_start=is_start,
                                       description=description,
                                       v_type=v_type,
                                       conn_to=conn_to,
                                       is_use_domain=is_use_domain,
                                       is_secret=is_secret,
                                       user_uuid=user_uuid,
                                       project_uuid=project_uuid,
                                       team_uuid=team_uuid)

        return result

    @acl_check('storage')
    def volume_list(self, context, page_size, page_num):
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)
        return self.v_manager.list(user_uuid, team_uuid, team_priv,
                                   project_uuid, project_priv, page_size,
                                   page_num)

    # 批量删除
    # @acl_check_uuids('storage')
    # def volumes_delete(self, context, volume_uuid, logic=0):
    #     log.info('when delete storage batch, context is : %s' % context)
    #     if logic == 1:
    #         return self.v_manager.logic_delete(volume_uuid)
    #     if logic == 0:
    #         return self.v_manager.delete(volume_uuid)
    #
    #     return request_result(603)

    @acl_check('snapshot')
    def snap_create(self, context, name, description, metadata, volume_uuid):
        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            log.debug('the token is: %s, source_ip is: %s, user_uuid is: %s,'
                      'team_uuid is: %s, project_uuid is: %s' % (token,
                                                                 source_ip,
                                                                 user_uuid,
                                                                 team_uuid,
                                                                 project_uuid))
            parameter_check(name, ptype='pnam')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.snap_manager.create(name=name,
                                        description=description,
                                        metadata=metadata,
                                        volume_uuid=volume_uuid,
                                        user_uuid=user_uuid,
                                        team_uuid=team_uuid,
                                        project_uuid=project_uuid)

    @acl_check('snapshot')
    def snap_list(self, context, page_num, page_size):
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)
        return self.snap_manager.list(user_uuid, team_uuid, team_priv,
                                      project_uuid, project_priv, page_size,
                                      page_num)


class CinderRouteManager(object):

    def __init__(self):
        self.v_manager = VolumeRouteManager()
        self.cinder = CinderDriver()
        self.snap_manager = SnapshotRouteManager()

    @acl_check('storage')
    def volume_delete(self, context, volume_uuid, logic=0):
        log.debug('delete context is: %s' % context)
        if logic == 1:
            return self.v_manager.logic_delete(volume_uuid)
        if logic == 0:
            return self.v_manager.delete(volume_uuid)

        return request_result(603)

    @acl_check('storage')
    def volume_detail(self, context, volume_uuid):
        log.debug('get the volume detail, context is: %s' % context)
        return self.v_manager.detail(volume_uuid)

    @acl_check('storage')
    def volume_update(self, context, up_dict, volume_uuid):
        log.debug('update the volume, context is: %s' % context)
        return self.v_manager.update(up_dict, volume_uuid)

    @acl_check('snapshot')
    def snap_delete(self, context, snapshot_uuid):
        log.debug('delete the snapshot, context is: %s' % context)
        return self.snap_manager.delete(snapshot_uuid)

    @acl_check('snapshot')
    def snap_update(self, context, up_dict, snapshot_uuid):
        log.debug('update the snapshot, context is: %s' % context)
        return self.snap_manager.update(up_dict, snapshot_uuid)

    @acl_check('snapshot')
    def snap_detail(self, context,  snapshot_uuid):
        log.debug('get the snapshot detail, the context is: %s' % context)
        return self.snap_manager.detail(snapshot_uuid)
