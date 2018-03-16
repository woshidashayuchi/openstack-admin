# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 11:01
import sys
p_path = sys.path[0] + '/..'
p_path1 = sys.path[0] + '/../..'
sys.path.insert(1, p_path)
sys.path.insert(1, p_path1)
from common.parameters import rpc_data, context_data
from common.logs import logging as log
from common.code import request_result
from common.rabbitmq_client import RabbitmqClient


class ComputeDriver(object):
    def __init__(self):
        self.rbtmq = RabbitmqClient()
        self.queue = "cinder_api"
        self.timeout = 5

    # 同restapi_define的context、parameters一致
    def create_osdisk(self, context, parameters):
        '''
        :param context: dict
        :param parameters: dict: {size=int,
                                  name=string,
                                  v_type=string,
                                  description=string,
                                  snapshot_uuid=string,
                                  source_volume_uuid=string
                                  image_uuid=string}
        :return:
        '''
        try:
            rpc_body = rpc_data("osdisk_cre", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def clouddisk_create(self, context, parameters=None):
        '''
        :param context: {'token':string,
                         'source_ip':source_ip}
        :param parameters: {size=int,
                            name=string,
                            v_type=string,
                            description=string,
                            snapshot_uuid=string,
                            source_volume_uuid=string}
        :return:
        '''
        context = context_data(context.get('token'),
                               'vol_vol_pro_com',
                               'create',
                               context.get('source_ip'))
        try:
            rpc_body = rpc_data("clouddisk_cre", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def clouddisk_delete(self, context, parameters):

        '''

        :param context:
        :param parameters: {"volume_uuid": string,
                            "logic": 1(逻辑删除)/0（物理删除）}
        :return:
        '''
        context = context_data(context.get('token'),
                               parameters.get('volume_uuid'),
                               'delete',
                               context.get('source_ip'))
        try:
            rpc_body = rpc_data("clouddisk_del", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def clouddisk_info(self, context, parameters={}):
        '''

        :param context:
        :param parameters:{'page_size':int,
                           'page_num': int}
                            可选
        :return:
        '''
        context = context_data(context.get('token'),
                               'vol_vol_usr_com',
                               'read')
        try:
            rpc_body = rpc_data("clouddisk_inf", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def clouddisk_recovery(self, context, parameters):
        '''

        :param context: {"token":string,
                         "source_ip"}
        :param parameters: {"volume_uuid": string}
        :return:
        '''
        context = context_data(context.get('token'),
                               parameters.get('volume_uuid'),
                               'update',
                               context.get('source_ip'))
        try:
            rpc_body = rpc_data("clouddisk_rec", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def disk_snapshot_delete(self, context, parameters):
        '''

        :param context: {"token":string,
                          "source_ip": string}
        :param parameters:{"snapshot_uuid":string,
                           "logic":1/0}
        :return:
        '''
        context = context_data(context.get('token'),
                               parameters.get('snapshot_uuid'),
                               "delete",
                               context.get('source_ip'))
        try:
            rpc_body = rpc_data("snap_del", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def disk_snapshot_revert(self, context, parameters):
        '''

        :param context:
        :param parameters: {"snapshot_uuid":string}
        :return:
        '''
        context = context_data(context.get('token'),
                               parameters.get('snapshot_uuid'),
                               'update',
                               context.get('source_ip'))
        try:
            rpc_body = rpc_data("snap_rev", context, parameters)

            return self.rbtmq.rpc_cast_client(self.queue,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)

    def disk_snapshot_revert_wait(self, context, parameters):
        '''

        :param context:{'token':string,
                        'source_ip':string,
                        }
        :param parameters: {"snapshot_uuid":string}
        :return:
        '''
        context = context_data(context.get('token'),
                               parameters.get('snapshot_uuid'),
                               'update',
                               context.get('source_ip'))
        try:
            rpc_body = rpc_data("snap_rev_wait", context, parameters)

            return self.rbtmq.rpc_call_client(self.queue,
                                              self.timeout,
                                              rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            return request_result(598)
