# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 14:23
from db.compute_db import ComputeDB
from common.logs import logging as log
from common.request_result import request_result
from common.skill import use_time, time_diff
from common.connect import connection


class CloudhostManager(object):

    def __init__(self):
        self.conn = connection()
        self.db = ComputeDB()

    @staticmethod
    def list_change(security_groups):
        # exchange the security to a string
        result = ""
        for security_group in security_groups:
            result = result + security_group['name'] + ','

        return result.rstrip(',')

    @staticmethod
    def string_change(security_groups):
        result = []
        for security_group in security_groups.split(','):
            result.append({'name': security_group})

        return result

    def create(self, instance_name, availability_zone, instance_num, image,
               instance_cpu, instance_mem, instance_type, net, net_interface,
               flavor_id, security_groups, keypair):
        '''
        :param instance_name:
        :param availability_zone:
        :param instance_num:
        :param image: image id
        :param instance_cpu:
        :param instance_mem:
        :param instance_type:
        :param net: 如果环境中只有一个网络，是不用设置此项的
        :param net_interface:
        :param flavor_id:
        :param security_groups:
        :param keypair:
        :param flavor_id:
        :return:
        '''
        try:

            op_result = self.conn.\
                compute.create_server(name=instance_name,
                                      availability_zone=availability_zone,
                                      image_id=image, # id
                                      security_groups=security_groups, # array
                                      # networks=,
                                      key_name=keypair, # name
                                      flavor_id=flavor_id # str
                                      )
        except Exception, e:
            log.error('create the cloudhost(op) error, reason is: %s' % e)
            return request_result(611)

        cloudhost_uuid = op_result.id
        access_ipv4 = op_result.access_ipv4

        try:
            db_result = self.db.\
                cloudhost_create(cloudhost_uuid=cloudhost_uuid,
                                 instance_name=instance_name,
                                 availability_zone=availability_zone,
                                 access_ipv4=access_ipv4,
                                 instance_num=instance_num,
                                 image=image,
                                 instance_cpu=instance_cpu,
                                 instance_mem=instance_mem,
                                 instance_type=instance_type,
                                 net=net,
                                 net_interface=net_interface,
                                 security_groups=self.
                                 list_change(security_groups),
                                 keypair=keypair,
                                 flavor_id=flavor_id,
                                 status=None,
                                 power_state=None)
        except Exception, e:
            log.error('create the cloudhost(db) error, reason is: %s' % e)
            return request_result(401)

        log.info('op_result: %s, db_result: %s' % (op_result, db_result))

        return request_result(200, cloudhost_uuid)

    def list(self):
        # all cloudhost list
        result = []
        try:
            db_result = self.db.cloudhost_list()
        except Exception, e:
            log.error('get the cloudhost list error, reason is: %s' % e)
            return request_result(403)
        if len(db_result) != 0:
            for host in db_result:
                cloudhost_uuid = host[0]
                instance_name = host[1]
                image = host[2]
                ip = host[3]
                instance_type = host[4]
                keypair = host[5]
                status = host[6]
                availability_zone = host[7]
                power_state = host[8]
                create_time = time_diff(host[9])
                result.append({'cloudhost_uuid': cloudhost_uuid,
                               'instance_name': instance_name,
                               'image': image,
                               'ip': ip,
                               'instance_type': instance_type,
                               'keypair': keypair,
                               'status': status,
                               'availability_zone': availability_zone,
                               'power_state': power_state,
                               'create_time': create_time})

        return request_result(200, result)

    def recover(self, cloudhost_uuid):
        '''
        :param cloudhost_uuid: uuid of cloudhost
        :return: dict
        '''
        cloudhost_route = CloudhostRouteManager()
        cloudhost_detail = cloudhost_route.detail(cloudhost_uuid)
        if cloudhost_detail.get('status') != 200:
            return cloudhost_detail
        else:
            # create new cloudhost for recover
            cloudhost_detail = cloudhost_detail.get('result')
            instance_name = cloudhost_detail.get('instance_name')
            availability_zone = cloudhost_detail.get('availability_zone')
            instance_num = cloudhost_detail.get('instance_num')
            image = cloudhost_detail.get('image')
            instance_cpu = cloudhost_detail.get('instance_cpu')
            instance_mem = cloudhost_detail.get('instance_mem')
            instance_type = cloudhost_detail.get('instance_type')
            net = cloudhost_detail.get('net')
            net_interface = cloudhost_detail.get('net_interface')
            flavor_id = cloudhost_detail.get('flavor_id')
            security_groups = self.string_change(cloudhost_detail.
                                                 get('security_groups'))
            keypair = cloudhost_detail.get('keypair')

            result = self.create(instance_name=instance_name,
                                 availability_zone=availability_zone,
                                 instance_num=instance_num,
                                 image=image,
                                 instance_cpu=instance_cpu,
                                 instance_mem=instance_mem,
                                 instance_type=instance_type,
                                 net=net,
                                 net_interface=net_interface,
                                 flavor_id=flavor_id,
                                 security_groups=security_groups,
                                 keypair=keypair)
            if result.get('status') != 200:
                return result
            # delete the old cloudhost from db
            try:
                self.db.cloudhost_old_delete(cloudhost_uuid)
            except Exception, e:
                log.error('delete the old cloudhost(db) error, '
                          'reason is: %s' % e)
                return request_result(404)

            return request_result(200, result.get('result'))


class CloudhostRouteManager(object):

    def __init__(self):
        self.db = ComputeDB()
        self.conn = connection()

    def detail(self, cloudhost_uuid):
        result = {}
        try:
            db_result = self.db.cloudhost_detail(cloudhost_uuid)
        except Exception, e:
            log.error('get the cloudhost detail(db) error, reason is: %s' % e)
            return request_result(403)

        if len(db_result) != 0:
            for host in db_result:
                result['cloudhost_uuid'] = host[0]
                result['instance_name'] = host[1]
                result['image'] = host[2]
                result['ip'] = host[3]
                result['instance_type'] = host[4]
                result['keypair'] = host[5]
                result['status'] = host[6]
                result['availability_zone'] = host[7]
                result['power_state'] = host[8]
                result['instance_num'] = host[9]
                result['instance_cpu'] = host[10]
                result['instance_mem'] = host[11]
                result['net'] = host[12]
                result['net_interface'] = host[13]
                result['security_groups'] = host[14]
                result['flavor_id'] = host[15]
                result['create_time'] = time_diff(host[16])

        return request_result(200, result)

    def delete(self, cloudhost_uuid):
        try:
            op_result = self.conn.compute.delete_server(cloudhost_uuid)
        except Exception, e:
            log.error('delete the clouhost(op) error, reason is: %s' % e)
            return request_result(613)

        try:
            db_result = self.db.cloudhost_delete(cloudhost_uuid)
        except Exception, e:
            log.error('delete the cloudhost(db) error, reason is: %s' % e)
            return request_result(404)

        log.info('when delete the cloudhost, op_result is: %s, '
                 'db_result is: %s' % (op_result, db_result))
        return request_result(200, 'deleted')

    def update(self, cloudhost_uuid, up_type=None, reboot_type='SOFT',
               attach={}):

        op_result = ''

        if up_type is None:
            op_result = 'not_define'
        else:
            try:
                # start cloudhost (启动)
                if up_type == 'start':
                    op_result = self.conn.compute.start_server(cloudhost_uuid)

                # stop cloudhost （停止）
                if up_type == 'stop':
                    op_result = self.conn.compute.stop_server(cloudhost_uuid)

                # suspend cloudhost (挂起)
                if up_type == 'suspend':
                    op_result = self.conn.compute.\
                        suspend_server(cloudhost_uuid)

                # resume cloudhost （继续）
                if up_type == 'resume':
                    op_result = self.conn.compute.resume_server(cloudhost_uuid)

                # reboot server , reboot_type: HARD OR SOFT (默认SOFT)
                if up_type == 'reboot':
                    op_result = self.conn.compute.reboot_server(cloudhost_uuid,
                                                                reboot_type)
                # lock_server
                if up_type == 'lock':
                    op_result = self.conn.compute.lock_server(cloudhost_uuid)

                # unlock_server
                if up_type == 'unlock':
                    op_result = self.conn.compute.unlock_server(cloudhost_uuid)

                # pause_server (暂停)
                if up_type == 'pause':
                    op_result = self.conn.compute.pause_server(cloudhost_uuid)

                # unpause_server (继续)
                if up_type == 'unpause':
                    op_result = self.conn.compute.\
                        unpause_server(cloudhost_uuid)

                # Attach a volume to an instance.
                # attach: a VolumeAttachment
                #: Name of the device such as, /dev/vdb.
                # device = resource.Body('device')
                #: The ID of the attachment.
                # id = resource.Body('id')
                #: The ID for the server.
                # server_id = resource.URI('server_id')
                #: The ID of the attached volume.
                # volume_id = resource.Body('volumeId')
                #: The ID of the attachment you want to delete or update.
                # attachment_id = resource.Body('attachment_id',
                #                               alternate_id=True)
                if up_type == 'attach':
                    op_result = self.conn.\
                        compute.create_volume_attachment(attach)

            except Exception, e:
                log.error('%s the cloudhost(op) error, '
                          'reason is: %s' % (up_type, e))
                return request_result(612)

        log.info('update the cloudhost op_result is: %s' % op_result)
        try:
            # update the database message
            db_rsult = self.db.cloudhost_update(cloudhost_uuid=cloudhost_uuid,
                                                up_type=up_type)
        except Exception, e:
            log.error('update the cloudhost(db) error, reason is: %s"' % e)
            return request_result(402)

        log.info('update the cloudhost(db) db_result is: %s' % db_rsult)

        return request_result(200, {'cloudhost_uuid': cloudhost_uuid})
