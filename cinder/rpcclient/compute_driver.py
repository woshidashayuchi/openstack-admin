# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 15:16

# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 11:01
import sys
import socket
p_path = sys.path[0] + '/..'
p_path1 = sys.path[0] + '/../..'
sys.path.insert(1, p_path)
sys.path.insert(1, p_path1)
reload(sys)
sys.setdefaultencoding('utf8')
from common.parameters import rpc_data, context_data
from common.logs import logging as log
from common.request_result import request_result
from common.rabbitmq_client import RabbitmqClient


class ComputeDriver(object):
    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.rbtmq = RabbitmqClient()
        self.queue = "cinder_api"
        self.timeout = 5

    # # 暂时忽略
    # def create_osdisk(self, context, parameters):
    #     """
    #     :param context: dict
    #     :param name: string
    #     :param description: description,
    #
    #     :return:
    #     """
    #     try:
    #         rpc_body = rpc_data("osdisk_cre", context, parameters)
    #
    #         return self.rbtmq.rpc_call_client(self.queue,
    #                                           self.timeout,
    #                                           rpc_body)
    #     except Exception, e:
    #         log.error('Rpc client exec error, reason=%s' % e)
    #         return request_result(598)

    def clouddisk_create(self, token, volume_name, volume_size,
                         volume_type='lvm', description=None,
                         snapshot_uuid=None, source_volume_uuid=None):
        """
        :param : 'token':string,
                 'source_ip':source_ip
        :param : size=int,
        :param : name=string,
        :param : v_type=string,
        :param : description=string,
        :param : snapshot_uuid=string,
        :param : source_volume_uuid=string}
        :return:
        """
        context = context_data(token,
                               'vol_vol_pro_com',
                               'create',
                               self.local_ip)
        parameters = {'size': volume_size,
                      'name': volume_name,
                      'v_type': volume_type,
                      'description': description,
                      'snapshot_uuid': snapshot_uuid,
                      'source_volume_uuid': source_volume_uuid}
        try:
            rpc_body = rpc_data("clouddisk_cre", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            log.error('create volume error, result status is not 0')
            raise Exception('create volume status is not 0')
        else:
            return result

    def clouddisk_delete(self, token, volume_uuid, logic=0):

        """

        :param token:
        :param volume_uuid: string,
        :param logic: 1(逻辑删除)/0（物理删除）}
        :return:
        """
        context = context_data(token,
                               volume_uuid,
                               'delete',
                               self.local_ip)
        parameters = {'volume_uuid': volume_uuid,
                      'logic': logic}
        try:
            rpc_body = rpc_data("clouddisk_del", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            log.error('delete volume error, result status is not 0')
            raise Exception('delete volume status is not 0')

    def clouddisk_list(self, token, page_size=1000, page_num=1):
        """

        :param token:
        :param page_size int 可选
        :param page_num int 可选
        :return:
        """
        context = context_data(token,
                               'vol_vol_usr_com',
                               'read')
        parameters = {'page_size': page_size,
                      'page_num': page_num}
        try:
            rpc_body = rpc_data("clouddisk_lis", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            log.error('get volume list error, result status is not 0')
            raise Exception('volume list status is not 0')
        else:
            return result

    def clouddisk_info(self, token, volume_uuid):
        context = context_data(token, volume_uuid, "read")
        parameters = {'volume_uuid': volume_uuid}

        try:
            rpc_body = rpc_data("clouddisk_inf", context, parameters)
            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('RPC client exec error, reason is: %s' % e)
            raise Exception(e)

        if result.get('status') != 0:
            log.error('get volume detail error, result status is not 0')
            raise Exception('volume detail status is not 0')
        else:
            return result

    def clouddisk_recovery(self, token, volume_uuid):
        """

        :param token: string,
        :param volume_uuid: string
        :return:
        """
        context = context_data(token,
                               volume_uuid,
                               'update',
                               self.local_ip)
        parameters = {'volume_uuid': volume_uuid}
        try:
            rpc_body = rpc_data("clouddisk_rec", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            log.error('recovery volume error, result status is not 0')
            raise Exception('recovery volume status is not 0')

    def disk_snapshot_create(self, token, snapshot_name, description,
                             volume_uuid, metadata=None):
        """
        :param snapshot_name:
        :param description:
        :param metadata:
        :param vm_uuid:
        :return:
        """
        context = context_data(token, 'vol_snap_pro_com', 'create',
                               self.local_ip)
        parameters = {'volume_uuid': volume_uuid,
                      'name': snapshot_name,
                      'description': description,
                      'metadata': metadata
                      }
        try:
            rpc_body = rpc_data("snap_cre", context, parameters)

            self.rbtmq.rpc_call_client(self.queue,
                                       self.timeout,
                                       rpc_body)
        except Exception, e:
            log.error('create volume error., reason is: %s' % e)
            raise Exception(e)

    def disk_snapshot_delete(self, token, snapshot_uuid, logic=0):
        """

        :param token:string,
        :param snapshot_uuid:string,
        :param logic: 1/0
        :return:
        """
        context = context_data(token,
                               snapshot_uuid,
                               "delete",
                               self.local_ip)
        parameters = {"snapshot_uuid": snapshot_uuid,
                      "logic": logic}
        try:
            rpc_body = rpc_data("snap_del", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            log.error('delete snapshot error, result status is not 0')
            raise Exception('delete snapshot status is not 0')

    def disk_snapshot_revert(self, token, snapshot_uuid):
        """

        :param token:
        :param snapshot_uuid:
        :return:
        """
        context = context_data(token,
                               snapshot_uuid,
                               "delete",
                               self.local_ip)
        parameters = {'snapshot_uuid': snapshot_uuid}
        try:
            rpc_body = rpc_data("snap_rev", context, parameters)

            self.rbtmq.rpc_call_client(self.queue,
                                       self.timeout,
                                       rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)

    def disk_snapshot_revert_wait(self, token, snapshot_uuid):
        """
        :param token:
        :param snapshot_uuid:
        :return:
        """
        context = context_data(token,
                               snapshot_uuid,
                               "delete",
                               self.local_ip)
        parameters = {'snapshot_uuid': snapshot_uuid}

        try:
            rpc_body = rpc_data("snap_rev_wait", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            log.error('revert snapshot error, result status is not 0')
            raise Exception('revert snapshot status is not 0')

    def clouddisk_mount(self, token, vm_uuid, volume_uuid):
        """
        :param token:
        :param vm_uuid:
        :param volume_uuid:
        :return:
        """

        context = context_data(token, 'vol_attach_pro_com',
                               'create', self.local_ip)
        parameters = {'server_uuid': vm_uuid,
                      'volume_uuid': volume_uuid}
        try:
            rpc_body = rpc_data("attach_cre", context, parameters)

            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            raise Exception('the result status is not correct')

    def clouddisk_unmount(self, token, volume_uuid):
        """
        :param attachment_uuid:
        :return:
        """
        context = context_data(token, volume_uuid, "delete", self.local_ip)
        parameters = {'volume_uuid': volume_uuid}

        try:
            rpc_body = rpc_data("attach_del", context, parameters)
            result = self.rbtmq.rpc_call_client(self.queue,
                                                self.timeout,
                                                rpc_body)
        except Exception, e:
            log.error('Rpc client exec error, reason=%s' % e)
            raise Exception(e)
        if result.get('status') != 0:
            raise Exception('the result status is not correct')


if __name__ == '__main__':
    op = ComputeDriver()
    op.clouddisk_unmount('586cb978-ca47-43ea-acbd-a9c5adce83b8','a4240115-12a1-4ef6-b76d-288e67a009b8')
