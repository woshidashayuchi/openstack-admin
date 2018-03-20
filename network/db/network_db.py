# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/20 11:23
from common.db.mysql_base import MysqlInit
from common.logs import logging as log
import uuid


class NetworkDB(MysqlInit):
    def __init__(self):
        super(NetworkDB, self).__init__()

    def data_init(self):
        # network api acl init
        sql1 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'0', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('net_net_adm_com', 'net_net_adm_com')

        sql2 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('net_net_tem_com', 'net_net_tem_com')

        sql3 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', '0', now(), now() FROM dual WHERE NOT " \
               "EXISTS (SELECT resource_uuid FROM resources_acl " \
               "WHERE resource_uuid='%s')" % ('net_net_pro_com',
                                              'net_net_pro_com')

        sql4 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', 'global', now(), now() FROM dual WHERE " \
               "NOT EXISTS (SELECT resource_uuid FROM resources_acl WHERE " \
               "resource_uuid='%s')" % ('net_net_usr_com', 'net_net_usr_com')

        return super(NetworkDB, self).exec_update_sql(sql1, sql2, sql3, sql4)


    def db_network_create(self, network_uuid, name, description,
                          is_admin_state_up=1, is_shared=0,
                          team_uuid=None, project_uuid=None, user_uuid=None):
        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (network_uuid,
                                                              'network',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

        sql = "insert into network(uuid, name, description, " \
              "is_admin_state_up, is_shared) values('%s', '%s', " \
              "'%s', %d, %d)" % (network_uuid, name, description,
                                 is_admin_state_up, is_shared)

        return super(NetworkDB, self).exec_update_sql(sql, sql_acl)

    def db_network_list_user(self, team_uuid, project_uuid, user_uuid,
                             page_size,  page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.name, b.name as subnet_name, b.cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time from network a, subnet b, " \
              "resources_acl c where a.uuid=b.network_uuid and " \
              "a.uuid=c.resource_uuid and c.user_uuid='%s' " \
              "and c.project_uuid='%s' and c.team_uuid='%s' " \
              "order by create_time DESC limit %d, %d" % (user_uuid,
                                                          project_uuid,
                                                          team_uuid,
                                                          start_position,
                                                          page_size)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_list_project(self, team_uuid, project_uuid,
                                page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.name, b.name as subnet_name, b.cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time from network a, subnet b, " \
              "resources_acl c where a.uuid=b.network_uuid and " \
              "a.uuid=c.resource_uuid " \
              "and c.project_uuid='%s' and c.team_uuid='%s' " \
              "order by create_time DESC limit %d, %d" % (project_uuid,
                                                          team_uuid,
                                                          start_position,
                                                          page_size)

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_subnet_create(self, name, description, is_dhcp_enabled,
                         network_uuid, ip_version, gateway_ip,
                         allocation_pools, cidr, dns_nameservers=[],
                         host_routes=[], user_uuid=None,
                         project_uuid=None, team_uuid=None):
        subnet_uuid = str(uuid.uuid4())
        sql = "insert into subnet(uuid, name, description, is_dhcp_enabled," \
              "network_uuid, ip_version, gateway_ip, allocation_pools, " \
              "cidr, dns_nameservers, host_routes) values('%s','%s','%s'," \
              "%d,'%s','%s','%s','%s'," \
              "'%s','%s','%s')" % (subnet_uuid, name, description,
                                   is_dhcp_enabled, network_uuid, ip_version,
                                   gateway_ip, allocation_pools, cidr,
                                   dns_nameservers, host_routes)

        return super(NetworkDB, self).exec_update_sql(sql)
