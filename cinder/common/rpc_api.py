# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:32
from common.logs import logging as log
from common.request_result import request_result


class RpcAPI(object):

    def __init__(self):

        self.app_resources = {}

    def add_resource(self, api, resource):

        self.app_resources[api] = resource

    def rpcapp_run(self, dict_data):

        try:
            api = dict_data['api']
            context = dict_data['context']
            parameters = dict_data['parameters']
        except Exception, e:
            log.warning('parameters error: %s' % e)
            return request_result(101)

        try:
            return self.app_resources[api](context, parameters)
        except Exception, e:
            log.error('RPC API routing error: %s' % e)
            return request_result(102)
