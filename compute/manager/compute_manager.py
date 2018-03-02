# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 14:23
from db.compute_db import ComputeDB
from common.logs import logging as log
from common.request_result import request_result
from common.skill import use_time, time_diff
import openstack


def connection():
    try:
        conn = openstack.connect(cloud='demo')
    except Exception, e:
        log.error('connect to op error, reason is: %s' % e)
        return False

    return conn


class CloudhostManager(object):

    def __init__(self):
        self.conn = connection()
        self.db = ComputeDB()

    @staticmethod
    def list_change(security_groups):
        result = ""
        for security_group in security_groups:
            result = result + security_group['name'] + ','

        return result.strip(',')

    def create(self, instance_name, availability_zone, instance_num, image,
               instance_cpu, instance_mem, instance_type, net, net_interface,
               flavor_id, security_groups, keypair):
        try:

            op_result = self.conn.\
                compute.create_server(name=instance_name,
                                      availability_zone=availability_zone,
                                      image_id=image,
                                      security_groups=security_groups,
                                      key_name=keypair,
                                      flavor_id=flavor_id
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
                                 security_groups=self.list_change(security_groups),
                                 keypair=keypair,
                                 status=None,
                                 power_state=None)
        except Exception, e:
            log.error('create the cloudhost(db) error, reason is: %s' % e)
            return request_result(401)

        log.info('op_result: %s, db_result: %s' % (op_result, db_result))

        request_result(200, cloudhost_uuid)

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
                result['create_time'] = time_diff(host[9])

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

    def upadte(self, cloudhost_uuid):
        pass
