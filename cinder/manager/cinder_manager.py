# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:13
from driver.cinder_driver import CinderDriver
from common.token_auth import token_auth
from common.logs import logging as log
from common.request_result import request_result
from common.acl import acl_check
from common.parameters import parameter_check
from volume_manager import VolumeManager, VolumeRouteManager
from snapshot_manager import SnapshotManager, SnapshotRouteManager
from attachment_manager import AttachmentManager
from templet_manager import TempletManager, TempletRouterManager
import json


class CinderManager(object):
    def __init__(self):
        self.v_manager = VolumeManager()
        self.snap_manager = SnapshotManager()
        self.attach_manager = AttachmentManager()
        self.templet_manager = TempletManager()

    @acl_check('storage')
    def osdisk_create(self, context, parameters):
        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            log.info('the token is: %s, source_ip is: %s, user_uuid is: %s,'
                     'team_uuid is: %s, project_uuid is: %s' % (token,
                                                                source_ip,
                                                                user_uuid,
                                                                team_uuid,
                                                                project_uuid))
            name = parameters.get('name')
            description = parameters.get('description')
            volume_uuid = parameters.get('volume_uuid')
            v_type = 'system'
            size = parameters.get('size')
            conn_to = parameters.get('conn_to')
            image_uuid = parameters.get('image_uuid')
            if name is None:
                name = volume_uuid
            parameter_check(volume_uuid, exist='yes')
            parameter_check(conn_to, exist='yes')
            parameter_check(image_uuid, exist='yes')

        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        result = self.v_manager.osdisk_create(
            name=name,
            size=size,
            description=description,
            v_type=v_type,
            volume_uuid=volume_uuid,
            conn_to=conn_to,
            image_uuid=image_uuid,
            user_uuid=user_uuid,
            project_uuid=project_uuid,
            team_uuid=team_uuid,
            # snapshot_uuid=snapshot_uuid,
            # source_volume_uuid=source_volume_uuid,
            # is_start=is_start,
            # is_use_domain=is_use_domain,
            # is_secret=is_secret
        )
        return result

    @acl_check('storage')
    def volume_create(self, context, parameters):
        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            log.info('the token is: %s, source_ip is: %s, user_uuid is: %s,' 
                     'team_uuid is: %s, project_uuid is: %s' % (token,
                                                                source_ip,
                                                                user_uuid,
                                                                team_uuid,
                                                                project_uuid))
            name = parameters.get('name')
            size = parameters.get('size')
            description = parameters.get('description')
            v_type = parameters.get('v_type')
            conn_to = parameters.get('conn_to')
            snapshot_uuid = parameters.get('snapshot_uuid')
            is_use_domain = parameters.get('is_use_domain', 1)
            source_volume_uuid = parameters.get('templet_uuid')
            image_uuid = parameters.get('image_uuid')
            is_start = parameters.get('is_start')
            is_secret = parameters.get('is_secret')
            if is_start is None:
                is_start = 0
            if is_secret is None:
                is_secret = 0
            # if v_type not in ('ssd', 'hdd'):
            #     raise Exception('v_type keyword error')
            parameter_check(is_use_domain, ptype='n01')
            parameter_check(is_start, ptype='n01')
            parameter_check(is_secret, ptype='n01')
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
                                       snapshot_uuid=snapshot_uuid,
                                       source_volume_uuid=source_volume_uuid,
                                       image_uuid=image_uuid,
                                       is_use_domain=is_use_domain,
                                       is_secret=is_secret,
                                       user_uuid=user_uuid,
                                       project_uuid=project_uuid,
                                       team_uuid=team_uuid)

        return result

    @acl_check('storage')
    def volume_list(self, context, parameters):
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')
            cloudhost_uuid = parameters.get('cloudhost_uuid')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)
        if cloudhost_uuid is None:
            return self.v_manager.list(user_uuid, team_uuid, team_priv,
                                       project_uuid, project_priv, page_size,
                                       page_num)
        else:
            return self.v_manager.list_cloudhost_volumes(cloudhost_uuid,
                                                         page_size,
                                                         page_num)

    @acl_check('templet')
    def templet_create(self, context, parameters):
        try:

            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            name = parameters.get('name')
            description = parameters.get('description')
            source_volume_uuid = parameters.get('source_volume_uuid')

            parameter_check(name, ptype='pnam')
            parameter_check(source_volume_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.templet_manager.templet_create(
                    name=name,
                    description=description,
                    source_volume_uuid=source_volume_uuid,
                    user_uuid=user_uuid,
                    project_uuid=project_uuid,
                    team_uuid=team_uuid)

    @acl_check('storage')
    def templet_list(self, context, parameters):
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)

        return self.templet_manager.list_templets(
                    user_uuid, team_uuid, team_priv, project_uuid,
                    project_priv, page_size, page_num)


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
    def snap_create(self, context, parameters):
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

            name = parameters.get('name')
            description = parameters.get('description')
            metadata = parameters.get('metadata')
            volume_uuid = parameters.get('volume_uuid')
            vm_uuid = parameters.get('vm_uuid')
            parameter_check(name, ptype='pnam')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        if vm_uuid is None:
            return self.snap_manager.create(name=name,
                                            description=description,
                                            metadata=metadata,
                                            volume_uuid=volume_uuid,
                                            user_uuid=user_uuid,
                                            team_uuid=team_uuid,
                                            project_uuid=project_uuid)
        else:
            return self.snap_manager.os_disks_snapshot_create(
                name=name,
                description=description,
                vm_uuid=vm_uuid,
                metadata=metadata,
                user_uuid=user_uuid,
                team_uuid=team_uuid,
                project_uuid=project_uuid
            )

    @acl_check('snapshot')
    def snap_list(self, context, parameters):
        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')
            volume_uuid = parameters.get('volume_uuid')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')
            parameter_check(volume_uuid, exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, reason=%s'
                        % (context, e))
            return request_result(101)
        return self.snap_manager.list(user_uuid, team_uuid, team_priv,
                                      project_uuid, project_priv,
                                      page_size, page_num, volume_uuid)

    @acl_check('attach')
    def attachment_create(self, context, server_uuid, volume_uuid):
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
            parameter_check(server_uuid, exist='yes')
            parameter_check(volume_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        result = self.attach_manager.\
            attachment_create(server_uuid=server_uuid,
                              volume_uuid=volume_uuid,
                              team_uuid=team_uuid,
                              project_uuid=project_uuid,
                              user_uuid=user_uuid)
        return result


class CinderRouteManager(object):

    def __init__(self):
        self.v_manager = VolumeRouteManager()
        self.cinder = CinderDriver()
        self.templet_manager = TempletRouterManager()
        self.snap_manager = SnapshotRouteManager()
        self.attach_manager = AttachmentManager()

    @acl_check('storage')
    def volume_delete(self, context, parameters):
        log.debug('delete context is: %s' % context)
        try:
            volume_uuid = parameters.get('volume_uuid')
            logic = parameters.get('logic')
            if logic is None:
                logic = 1
        except Exception, e:
            log.error('parameters check error, reason is: %s' % e)
            return request_result(101)

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
    def snap_delete(self, context, snapshot_uuid, logic=0):
        log.debug('delete the snapshot, context is: %s' % context)
        if logic == 0:
            return self.snap_manager.delete(snapshot_uuid)
        if logic == 1:
            return self.snap_manager.logic_delete(snapshot_uuid)

        return request_result(1003)

    @acl_check('snapshot')
    def snap_update(self, context, up_dict, snapshot_uuid, volume_uuid=None):
        log.debug('update the snapshot, context is: %s' % context)
        if up_dict.get('up_type') is None:
            return request_result(101)
        return self.snap_manager.update(up_dict, snapshot_uuid, volume_uuid)

    @acl_check('snapshot')
    def snap_detail(self, context,  snapshot_uuid):
        log.debug('get the snapshot detail, the context is: %s' % context)
        return self.snap_manager.detail(snapshot_uuid)

    def attachment_delete(self, context, volume_uuid):
        log.debug('delete the attachment, the context is: %s' % context)
        return self.attach_manager.\
            attachment_delete(volume_uuid)

    @acl_check('storage')
    def osdisk_delete(self, context, volume_uuid):
        log.info('osdisk delete, the context is: %s' % context)
        try:
            parameter_check(volume_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.v_manager.osdisk_delete(volume_uuid)

    @acl_check('storage')
    def templet_detail(self, context, templet_uuid):
        log.debug('get the detail of templet, the context is: %s' % context)
        try:
            parameter_check(templet_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.templet_manager.templet_detail(templet_uuid)

    @acl_check('storage')
    def templet_delete(self, context, templet_uuid):
        log.debug('delete the templet, the context is: %s' % context)
        try:
            parameter_check(templet_uuid, exist='yes')
        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)
        return self.templet_manager.templet_delete(templet_uuid)

    @acl_check('storage')
    def templet_update(self, context, parameters):
        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            templet_uuid = context.get('resource_uuid')
            parameters = json.loads(parameters)
            name = parameters.get('name')
            description = parameters.get('description')
            parameter_check(name, ptype='pnam', exist='no')

        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        return self.templet_manager.templet_update(templet_uuid,
                                                   name,
                                                   description,
                                                   user_uuid,
                                                   project_uuid,
                                                   team_uuid)