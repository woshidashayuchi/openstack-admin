# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:58

from common.logs import logging as log
from common.time_log import time_log
from common.request_result import request_result
from manager.cinder_manager import CinderManager, CinderRouteManager


class CinderRpcAPIs(object):

    def __init__(self):
        self.cinder_manager = CinderManager()
        self.cinder_route_manager = CinderRouteManager()

    def osdisk_create(self, context, parameters):
        try:
            result = self.cinder_manager. \
                osdisk_create(context=context, parameters=parameters)
        except Exception, e:
            log.error('create the osdisk(mq) error, reason is: %s' % e)
            return request_result(999)
        return result

    def osdisk_delete(self, context, parameters):
        try:
            volume_uuid = parameters.get('volume_uuid')
            result = self.cinder_route_manager.osdisk_delete(context,
                                                             volume_uuid)
        except Exception, e:
            log.error('delete the osdisk(mq) error, reason is: %s' % e)
            return request_result(999)
        return result

    def clouddisk_create(self, context, parameters=None):
        log.info('create the vol base data is: context:%s, '
                 'parameters: %s' % (context, parameters))
        try:
            result = self.cinder_manager. \
                volume_create(context=context, parameters=parameters)

        except Exception, e:
            log.error('create the volume(mq) error, reason=%s' % e)
            return request_result(999)
        log.info('create the volume(mq) result is: %s' % result)
        return result

    def clouddisk_delete(self, context, parameters):
        try:
            result = self.cinder_route_manager.\
                volume_delete(context, parameters)
        except Exception, e:
            log.error('delete the volume(mq) error, reason is: %s' % e)
            return request_result(999)

        return result

    def clouddisk_list(self, context, parameters):
        try:
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')
            if page_size is None and page_num is None:
                page_size = 1000
                page_num = 1
            parameters['page_size'] = page_size
            parameters['page_num'] = page_num
            result = self.cinder_manager.volume_list(context, parameters)
        except Exception, e:
            log.error('list the volumes(mq) error, reason is: %s' % e)
            return request_result(999)
        return result

    def clouddisk_info(self, context, parameters):
        try:
            volume_uuid = parameters.get('volume_uuid')
            result = self.cinder_route_manager.volume_detail(
                                               context,
                                               volume_uuid)
        except Exception, e:
            log.error('get the volume detail(mq) error, reason is: %s' % e)
            return request_result(999)

        return result

    def clouddisk_recovery(self, context, parameters):
        volume_uuid = parameters.get('volume_uuid')
        up_dict = {'up_type': 'recovery'}
        try:
            result = self.cinder_route_manager.\
                volume_update(context=context,
                              up_dict=up_dict,
                              volume_uuid=volume_uuid)
        except Exception, e:
            log.error('recovery the volume(mq) error, reason is: %s' % e)
            return request_result(999)

        return result

    def disk_snapshot_create(self, context, parameters):
        log.info('<<<<vm snapshot create, context: %s>>>>>>' % context)
        log.info('<<<<vm snapshot create, parameters: %s>>>>>>' % context)
        try:
            result = self.cinder_manager.snap_create(context, parameters)
        except Exception, e:
            log.error('create the snapshot error, reason is: %s' % e)
            return request_result(999)

        return result

    def disk_snapshot_delete(self, context, parameters):
        try:
            snapshot_uuid = parameters.get('snapshot_uuid')
            logic = parameters.get('logic')
            if logic is None:
                logic = 0
            result = self.cinder_route_manager.\
                snap_delete(context,
                            snapshot_uuid=snapshot_uuid,
                            logic=logic)
        except Exception, e:
            log.error('snapshot delete(mq) error, reason is: %s' % e)
            return request_result(999)
        return result

    def disk_snapshot_revert(self, context, parameters):
        try:
            snapshot_uuid = parameters.get('snapshot_uuid')
            volume_uuid = parameters.get('volume_uuid')
            up_dict = {'up_type': 'revert'}
            self.cinder_route_manager.snap_update(context,
                                                  up_dict,
                                                  snapshot_uuid,
                                                  volume_uuid)
        except Exception, e:
            log.error('revert snapshot(mq) error, reason is: %s' % e)
            return request_result(999)

    def disk_snapshot_revert_wait(self, context, parameters):
        try:
            snapshot_uuid = parameters.get('snapshot_uuid')
            up_dict = {'up_type': 'recovery'}
            result = self.cinder_route_manager.snap_update(context,
                                                           up_dict,
                                                           snapshot_uuid)

            return result
        except Exception, e:
            log.error('revert snapshot(mq) wait error, reason is: %s' % e)
            return request_result(999)

    @time_log
    def attachment_create(self, context, parameters):
        log.info('>>>>>>>>>>>>>>>>>>>>>>>>>')
        try:
            server_uuid = parameters.get('server_uuid')
            volume_uuid = parameters.get('volume_uuid')
            result = self.cinder_manager.attachment_create(context,
                                                           server_uuid,
                                                           volume_uuid)
        except Exception, e:
            log.error('attachment create(mq) error, reason is: %s' % e)
            return request_result(999)

        return result

    @time_log
    def attachment_delete(self, context, parameters):
        try:
            volume_uuid = parameters.get('volume_uuid')

            result = self.cinder_route_manager.attachment_delete(
                          context,
                          volume_uuid
            )
        except Exception, e:
            log.error('attachment delete(mq) error, reason is: %s' % e)
            return request_result(999)

        return result
