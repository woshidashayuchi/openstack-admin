# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/6 17:53
from common.logs import logging as log
from common.connect import connection
from common.request_result import request_result


class NetworkToServerManager(object):

    def __init__(self):
        self.conn = connection()

    def add_floating_ip_to_server(self, cloudhost_uuid, address,
                                  fixed_address=None):
        '''
        Parameters:
        :param cloudhost_uuid: the ID of a server instance.
        :param address: The floating IP address to be added to the server.
        :param fixed_address: The fixed IP address to be associated with the
         floating IP address. Used when the server is connected to
         multiple networks.
        :return:
        '''

        try:
            op_result = self.conn.compute.\
                add_floating_ip_to_server(server=cloudhost_uuid,
                                          address=address,
                                          fixed_address=fixed_address)
        except Exception, e:
            log.error('add the floating ip to server(op) error, reason is: '
                      '%s' % e)
            return request_result(631)
        log.info('add floating ip to server(op) result is: %s' % op_result)

        return request_result(200, 'added')

    def remove_floating_ip_from_server(self, cloudhost_uuid, address):
        try:
            op_result = self.conn.compute.\
                remove_floating_ip_from_server(server=cloudhost_uuid,
                                               address=address)
        except Exception, e:
            log.error('remove the floating ip from server(op) error, '
                      'reason is: %s' % e)
            return request_result(632)

        log.info('remove floating ip from server(op) result is: '
                 '%s' % op_result)

        return request_result(200, 'removed')
