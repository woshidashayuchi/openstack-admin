# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 9:48
from common.db.compute_mysql_base import MysqlInit
from common.logs import logging as log
import uuid


class ComputeDB(MysqlInit):

    def __init__(self):
        super(ComputeDB, self).__init__()

    def cloudhost_create(self, cloudhost_uuid, instance_name, access_ipv4,
                         availability_zone, instance_num, image, instance_cpu,
                         instance_mem, instance_type, net, net_interface,
                         security_groups, keypair, status, power_state):

        sql = "insert into cloudhost(uuid, instance_name, access_ipv4," \
              "availability_zone, instance_num, image, instance_cpu, " \
              "instance_mem, instance_type, net, net_interface, " \
              "security_groups, keypair, status, power_state) VALUES ('%s', " \
              "'%s','%s', " \
              "'%s', %d, '%s',%d, %d, '%s', '%s', '%s', " \
              "'%s', '%s', '%s', '%s')" % (cloudhost_uuid,
                                           instance_name,
                                           access_ipv4,
                                           availability_zone,
                                           instance_num,
                                           image,
                                           instance_cpu,
                                           instance_mem,
                                           instance_type,
                                           net,
                                           net_interface,
                                           str(security_groups),
                                           keypair,
                                           status,
                                           power_state)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_list(self):
        sql = "select uuid as cloudhost_uuid, instance_name, image, " \
              "access_ipv4 as ip, instance_type, keypair, status, " \
              "availability_zone, power_state, create_time from cloudhost"

        return super(ComputeDB, self).exec_select_sql(sql)

    def cloudhost_detail(self, cloudhost_uuid):
        sql = "select uuid as cloudhost_uuid, instance_name, image, " \
              "access_ipv4 as ip, instance_type, keypair, status, " \
              "availability_zone,power_state, create_time from cloudhost " \
              "where uuid='%s'" % cloudhost_uuid

        return super(ComputeDB, self).exec_select_sql(sql)

    def cloudhost_delete(self, cloudhost_uuid):
        sql = "delete from cloudhost WHERE uuid='%s'" % cloudhost_uuid

        return super(ComputeDB, self).exec_update_sql(sql)
