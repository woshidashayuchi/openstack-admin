# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/20 11:23
from common.db.mysql_base import MysqlInit
from common.logs import logging as log
import uuid
import json


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

    def network_name_check(self, network_name, user_uuid, project_uuid,
                           team_uuid):
        sql = "select count(*) from network a, resources_acl b  " \
              "where a.name='%s' and a.uuid=b.resource_uuid and " \
              "b.user_uuid='%s' and " \
              "b.project_uuid='%s' and " \
              "b.team_uuid='%s'" % (network_name,
                                    user_uuid,
                                    project_uuid,
                                    team_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_create(self, network_uuid, name, description,
                          is_admin_state_up=1, is_shared=0,
                          team_uuid=None, project_uuid=None, user_uuid=None):
        sql_acl = "insert into resources_acl(resource_uuid, resource_type, " \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (network_uuid,
                                                              'network',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

        sql = "insert into network(uuid, name, description, " \
              "is_admin_state_up, is_shared, is_show) values('%s', '%s', " \
              "'%s', %d, %d, %d)" % (network_uuid, name, description,
                                     is_admin_state_up, is_shared, 1)

        return super(NetworkDB, self).exec_update_sql(sql, sql_acl)

    def db_network_list_user(self, team_uuid, project_uuid, user_uuid,
                             page_size,  page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.name, b.name as subnet_name, b.cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time, a.uuid, a.update_time " \
              "from network a, subnet b, " \
              "resources_acl c where a.is_show=1 and a.uuid=b.network_uuid " \
              "and a.uuid=c.resource_uuid and c.user_uuid='%s' " \
              "and c.project_uuid='%s' and c.team_uuid='%s' " \
              "UNION " \
              "select a.name, '' as subnet_name, '' as cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time, a.uuid, a.update_time " \
              "from network a, " \
              "subnet b, resources_acl c where a.is_show=1 " \
              "and a.uuid not in (select network_uuid from subnet) " \
              "and a.uuid=c.resource_uuid and c.user_uuid='%s' " \
              "and c.project_uuid='%s' and c.team_uuid='%s' " \
              "order by create_time DESC limit %d, %d" % (user_uuid,
                                                          project_uuid,
                                                          team_uuid,
                                                          user_uuid,
                                                          project_uuid,
                                                          team_uuid,
                                                          start_position,
                                                          page_size)
        log.info('user network list sql is: %s' % sql)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_list_project(self, team_uuid, project_uuid,
                                page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.name, b.name as subnet_name, b.cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time, a.uuid, a.update_time " \
              "from network a, subnet b, " \
              "resources_acl c where a.is_show=1 and a.uuid=b.network_uuid " \
              "and a.uuid=c.resource_uuid " \
              "and c.project_uuid='%s' and c.team_uuid='%s' " \
              "UNION " \
              "select a.name, '' as subnet_name, '' as cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time,a.uuid,a.update_time " \
              "from network a, " \
              "subnet b, resources_acl c where a.is_show=1 and " \
              "a.uuid not in (select network_uuid from subnet) " \
              "and a.uuid=c.resource_uuid " \
              "and c.project_uuid='%s' and c.team_uuid='%s' " \
              "order by create_time DESC limit %d, %d" % (project_uuid,
                                                          team_uuid,
                                                          project_uuid,
                                                          team_uuid,
                                                          start_position,
                                                          page_size)

        log.info('project network list sql is: %s' % sql)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_user_count(self, team_uuid, project_uuid, user_uuid):
        sql = "select count(*) from network a, resources_acl b where " \
              "a.is_show=1 and a.uuid=b.resource_uuid and " \
              "b.project_uuid='%s' and b.team_uuid='%s' and " \
              "b.user_uuid='%s'" % (project_uuid,
                                    team_uuid,
                                    user_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_project_count(self, team_uuid, project_uuid):
        sql = "select count(*) from network a, resources_acl b where " \
              "a.is_show=1 and a.uuid=b.resource_uuid and " \
              "b.project_uuid='%s' and b.team_uuid='%s'" % (project_uuid,
                                                            team_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_detail(self, network_uuid):
        sql = "select a.name, b.name as subnet_name, b.cidr, a.description, " \
              "a.is_shared, a.is_router_external, a.size, a.status, " \
              "a.is_admin_state_up, a.create_time,a.update_time,b.gateway_ip," \
              "b.allocation_pools,b.dns_nameservers,b.host_routes from " \
              "network a, subnet b " \
              "where a.uuid=b.network_uuid and a.uuid='%s'" % network_uuid

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_logic_delete(self, network_uuid):
        sql = "update network set is_show=0 where " \
              "uuid='%s'" % network_uuid

        return super(NetworkDB, self).exec_update_sql(sql)
    
    def delete_network_chk(self, network_uuid):
        sql = "select count(*) from port where network_uuid='%s' and " \
              "vm_uuid is not NULL and vm_uuid != 'None'" % (network_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_network_delete(self, network_uuid):
        # 删除网络
        sql_network = "delete from network where " \
                      "uuid='%s'" % network_uuid

        # 删除子网
        sql_subnet = "delete from subnet where " \
                     "network_uuid='%s'" % network_uuid

        # 删除acl权限表中与该网络资源相关的记录
        sql_acl = "delete from resources_acl where " \
                  "resource_uuid='%s'" % network_uuid

        # 删除acl权限表中与该网络相关子网的记录
        sql_acl_sub = "delete from resources_acl where " \
                      "resource_uuid=(select uuid from subnet where " \
                      "network_uuid='%s')" % network_uuid

        return super(NetworkDB, self).exec_update_sql(sql_network,
                                                      sql_subnet,
                                                      sql_acl,
                                                      sql_acl_sub)

    def db_network_update(self, up_dict):
        network_uuid = up_dict.get('network_uuid')
        up_nets = up_dict.keys()
        for column in up_nets:
            if column == 'network_uuid':
                continue
            sql = "update network set %s='%s' " \
                  "where uuid='%s'" % (column, up_dict[column], network_uuid)

            super(NetworkDB, self).exec_update_sql(sql)

        return

    def get_subnet_from_network(self, network_uuid):
        sql = "select uuid from subnet where network_uuid='%s'" % network_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_subnet_create(self, subnet_uuid, name, description, is_dhcp_enabled,
                         network_uuid, ip_version, gateway_ip,
                         allocation_pools, cidr, dns_nameservers=[],
                         host_routes=[], user_uuid=None,
                         project_uuid=None, team_uuid=None):

        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (subnet_uuid,
                                                              'network',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

        sql = "insert into subnet(uuid, name, description, is_dhcp_enabled," \
              "network_uuid, ip_version, gateway_ip, allocation_pools, " \
              "cidr, dns_nameservers, host_routes) values('%s','%s','%s'," \
              "%d,'%s','%s','%s','%s'," \
              "'%s','%s','%s')" % (subnet_uuid, name, description,
                                   is_dhcp_enabled, network_uuid, ip_version,
                                   gateway_ip, allocation_pools, cidr,
                                   dns_nameservers, host_routes)
        log.info('create sql is: (%s;%s)' % (sql_acl, sql))
        return super(NetworkDB, self).exec_update_sql(sql_acl, sql)

    def db_subnet_list_user(self, team_uuid, project_uuid, user_uuid,
                           page_size,  page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as subnet_uuid, a.name, a.description from " \
              "subnet a, resources_acl b where a.uuid=b.resource_uuid and " \
              "b.user_uuid='%s' and b.project_uuid='%s' and " \
              "b.team_uuid='%s' limit %d, %d" % (user_uuid,
                                                 project_uuid,
                                                 team_uuid,
                                                 start_position,
                                                 page_size)

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_subnet_list_project(self, team_uuid, project_uuid, page_size,
                               page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as subnet_uuid, a.name, a.description from " \
              "subnet a, resources_acl b where a.uuid=b.resource_uuid and " \
              "b.project_uuid='%s' and " \
              "b.team_uuid='%s' limit %d, %d" % (project_uuid,
                                                 team_uuid,
                                                 start_position,
                                                 page_size)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_subnet_user_count(self, team_uuid, project_uuid, user_uuid):
        sql = "select count(*) from subnet a, resources_acl b where " \
              "a.uuid=b.resource_uuid and " \
              "b.user_uuid='%s' and b.project_uuid='%s' and " \
              "b.team_uuid='%s'" % (user_uuid,
                                    project_uuid,
                                    team_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_subnet_project_count(self, team_uuid, project_uuid):
        sql = "select count(*) from subnet a, resources_acl b where " \
              "a.uuid=b.resource_uuid and " \
              "b.project_uuid='%s' and " \
              "b.team_uuid='%s'" % (project_uuid,
                                    team_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    # def db_subnet_project_count(self, team_uuid, project_uuid):
    #     pass

    def db_subnet_delete(self, subnet_uuid):
        del_acl = "delete from resources_acl where " \
                  "resource_uuid='%s'" % subnet_uuid

        del_sql = "delete from subnet where uuid='%s'" % subnet_uuid

        return super(NetworkDB, self).exec_update_sql(del_acl, del_sql)

    def get_subnet_uuid_by_network(self, network_uuid):
        sql = "select uuid from subnet where network_uuid='%s'" % network_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def check_router_name(self, router_name, user_uuid, project_uuid,
                          team_uuid):
        sql = "select count(*) from router a, resources_acl b where " \
              "a.name='%s' and a.uuid=b.resource_uuid and " \
              "b.user_uuid='%s' and b.project_uuid='%s' and " \
              "b.team_uuid='%s'" % (router_name,
                                    user_uuid,
                                    project_uuid,
                                    team_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    # router
    def db_router_create(self, name, description, out_network_uuid, 
                         is_admin_state_up,
                         user_uuid, project_uuid, team_uuid, router_uuid):
        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (router_uuid,
                                                              'network',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)
        sql = "insert into router(uuid, name, description, " \
              "external_gateway_info, " \
              "is_admin_state_up, status, is_show) values " \
              "('%s', '%s', '%s', '%s', %d, 'creating', 1)" % (router_uuid,
                                                               name,
                                                               description,
                                                               out_network_uuid,
                                                               is_admin_state_up)
        return super(NetworkDB, self).exec_update_sql(sql_acl, sql)

    def db_router_list_project(self, team_uuid, project_uuid,
                               page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as router_uuid, a.name, a.description, " \
              "a.status,a.create_time,a.update_time, " \
              "a.external_gateway_info from router a, " \
              "resources_acl b where " \
              "a.uuid=b.resource_uuid and a.is_show=1 and " \
              "b.team_uuid='%s' and b.project_uuid='%s' " \
              "order by create_time limit %d, %d" % (team_uuid,
                                                     project_uuid,
                                                     start_position,
                                                     page_size)
        log.info('sql is: %s' % sql)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_router_list_user(self, team_uuid, project_uuid, user_uuid,
                            page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as router_uuid, a.name, a.description, " \
              "a.status,a.create_time,a.update_time, " \
              "a.external_gateway_info from router a, " \
              "resources_acl b where " \
              "a.uuid=b.resource_uuid and a.is_show=1 and " \
              "b.team_uuid='%s' and b.project_uuid='%s' and " \
              "b.user_uuid='%s' " \
              "order by create_time limit %d, %d" % (team_uuid,
                                                     project_uuid,
                                                     user_uuid,
                                                     start_position,
                                                     page_size)
        log.info('sql: %s' % sql)
        return super(NetworkDB, self).exec_select_sql(sql)

    def router_pro_count(self, team_uuid, project_uuid):
        sql = "select count(*) from router a, " \
              "resources_acl b where " \
              "a.uuid=b.resource_uuid and a.is_show=1 and " \
              "b.team_uuid='%s' and b.project_uuid='%s'" % (team_uuid,
                                                            project_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def router_usr_count(self, team_uuid, project_uuid, user_uuid):
        sql = "select count(*) from router a, " \
              "resources_acl b where " \
              "a.uuid=b.resource_uuid and a.is_show=1 and " \
              "b.team_uuid='%s' and b.project_uuid='%s' and " \
              "b.user_uuid='%s'" % (team_uuid,
                                    project_uuid,
                                    user_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_router_detail(self, router_uuid):
        sql = "select uuid as router_uuid, name, description, " \
              "external_gateway_info, is_admin_state_up, status, " \
              "create_time, update_time from router " \
              "where uuid='%s'" % router_uuid

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_router_update(self, router_uuid, up_dict):
        for column in up_dict:
            if column == 'router_uuid':
                continue
            sql = "update router set %s='%s' " \
                  "where uuid='%s'" % (column, up_dict[column], router_uuid)

            super(NetworkDB, self).exec_update_sql(sql)

    def db_router_gateway_ab(self, router_uuid, network_uuid):
        sql = "update router set external_gateway_info='%s' where " \
              "uuid='%s'" % (network_uuid, router_uuid)

        return super(NetworkDB, self).exec_update_sql(sql)

    def db_router_interface_ab(self, router_uuid, subnet_uuid, rtype):
        if rtype == 'add':
            sql = "update subnet set router_interface='%s' where " \
                  "uuid='%s'" % (router_uuid, subnet_uuid)
        elif rtype == 'remove':
            sql = "update subnet set " \
                  "router_interface=NULL where uuid='%s'" % subnet_uuid
        else:
            sql = ""
        return super(NetworkDB, self).exec_update_sql(sql)

    def db_port_create(self, port_uuid, name, description, ip_address,
                       network_uuid, mac_address, status, user_uuid=None,
                       project_uuid=None, team_uuid=None):
        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (port_uuid,
                                                              'network',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)
        if name is None:
            name = ip_address
        sql = "insert into port(uuid, name, description, ip_address, " \
              "network_uuid, mac_address, status) values('%s', '%s', " \
              "'%s', '%s', '%s', '%s', '%s')" % (port_uuid,
                                                 name,
                                                 description,
                                                 ip_address,
                                                 network_uuid,
                                                 mac_address,
                                                 status)
        return super(NetworkDB, self).exec_update_sql(sql_acl, sql)

    def db_check_network_if_bind_subnet(self, network_uuid):
        sql = "select count(*) from subnet where " \
              "network_uuid='%s'" % network_uuid

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_ports_list(self, network_uuid, page_size=1000, page_num=1):
        start_position = (page_num - 1) * page_size
        sql = "select uuid as port_uuid, name, description, ip_address, " \
              "mac_address, status, create_time, update_time, vm_uuid " \
              "from port " \
              "where network_uuid='%s' order by create_time desc " \
              "limit %d, %d " % (network_uuid, start_position, page_size)

        return super(NetworkDB, self).exec_select_sql(sql)

    def ports_all_project(self, team_uuid, project_uuid, page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid, a.vm_uuid, a.name, a.description, a.ip_address, " \
              "a.network_uuid, a.mac_address, a.status, a.create_time, " \
              "a.update_time from port a, resources_acl b where " \
              "a.uuid=b.resource_uuid and b.project_uuid='%s' and " \
              "b.team_uuid='%s' order by create_time desc limit %d, " \
              "%d" % (project_uuid,
                      team_uuid,
                      start_position,
                      page_size)
        return super(NetworkDB, self).exec_select_sql(sql)

    def ports_all_count_project(self, team_uuid, project_uuid):
        sql = "select count(*) from port a, resources_acl b where " \
              "a.uuid = b.resource_uuid and b.team_uuid='%s' and " \
              "b.project_uuid='%s'" % (team_uuid, project_uuid)

        return super(NetworkDB, self).exec_select_sql(sql)

    def ports_all_users(self, team_uuid, project_uuid, user_uuid,
                        page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid, a.vm_uuid, a.name, a.description, a.ip_address, " \
              "a.network_uuid, a.mac_address, a.status, a.create_time, " \
              "a.update_time from port a, resources_acl b where " \
              "a.uuid=b.resource_uuid and b.project_uuid='%s' and " \
              "and b.user_uuid = '%s' " \
              "b.team_uuid='%s' order by create_time desc limit %d, " \
              "%d" % (project_uuid,
                      user_uuid,
                      team_uuid,
                      start_position,
                      page_size)

        return super(NetworkDB, self).exec_select_sql(sql)

    def ports_all_users_count(self, team_uuid, project_uuid, user_uuid):
        sql = "select count(*) from port a, resources_acl b where " \
              "a.uuid==b.resource_uuid and b.team_uuid='%s' and " \
              "b.project_uuid='%s' and b.team_uuid='%s' and b.user_" \
              "uuid = '%s'" % (project_uuid, team_uuid, user_uuid)

        return super(NetworkDB, self).exec_select_sql(sql)

    def ports_all_count_user(self):
        pass

    def ports_all_user(self):
        pass

    def db_ports_count(self, network_uuid):
        sql = "select count(*) from port where " \
              "network_uuid='%s'" % network_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_port_detail(self, port_uuid):
        sql = "select uuid as port_uuid, vm_uuid, name, description, " \
              "ip_address, network_uuid, mac_address, status, " \
              "create_time, update_time from port where uuid='%s'" % port_uuid

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_port_if_can_del(self, port_uuid):
        sql = "select status from port where uuid='%s'" % port_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_port_delete(self, port_uuid):
        sql_acl = "delete from resources_acl where " \
                  "resource_uuid='%s'" % port_uuid

        sql = "delete from port where uuid='%s'" % port_uuid

        return super(NetworkDB, self).exec_update_sql(sql_acl, sql)

    def db_port_attach_check(self, port_uuid):
        sql = "select vm_uuid, status from port where uuid='%s'" % port_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_port_vm_attach(self, port_uuid, vm_uuid):
        sql = "update port set vm_uuid='%s', status='in-use' where " \
              "uuid='%s'" % (vm_uuid, port_uuid)
        return super(NetworkDB, self).exec_update_sql(sql)

    def db_port_vm_unattach(self, port_uuid):
        sql = "update port set vm_uuid=NULL, status='available' " \
              "where uuid='%s'" % port_uuid
        return super(NetworkDB, self).exec_update_sql(sql)

    def db_router_logic_del(self, router_uuid):
        sql = "update router set is_show=0 where " \
              "router_uuid='%s'" % router_uuid

        return super(NetworkDB, self).exec_update_sql(sql)

    def db_router_delete(self, router_uuid):
        sql = "delete from router where uuid='%s'" % router_uuid

        sql_acl = "delete from resources_acl where " \
                  "resource_uuid='%s'" % router_uuid

        return super(NetworkDB, self).exec_update_sql(sql, sql_acl)

    # floating ip
    def db_floating_ip_create(self, floatingip_uuid, name, description,
                              router_uuid, fixed_ip_address,
                              floating_ip_address, revision_number, port_id,
                              user_uuid, project_uuid, team_uuid):

        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (floatingip_uuid,
                                                              'network',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

        sql = "insert into floating_ip(uuid, name, description, router_uuid," \
              "fixed_ip_address, floating_ip_address, revision_number, " \
              "port_id, is_show) values('%s', '%s', '%s', '%s', '%s', '%s', " \
              "%d, '%s', 1)" % (floatingip_uuid, name, description, router_uuid,
                                fixed_ip_address, floating_ip_address,
                                revision_number, port_id)

        return super(NetworkDB, self).exec_update_sql(sql_acl, sql)

    def db_floating_ip_list_project(self, team_uuid, project_uuid,
                                    page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as floatingip_uuid, a.name, a.description, " \
              "a.router_uuid, a.fixed_ip_address, a.floating_ip_address," \
              "a.revision_number, a.port_id, a.create_time, a.update_time, " \
              "a.vm_uuid, a.status from floating_ip a, " \
              "resources_acl b WHERE a.is_show=1 and a.uuid=b.resource_uuid " \
              "and b.team_uuid='%s' and b.project_uuid='%s' order by " \
              "create_time DESC limit %d, %d" % (team_uuid,
                                                 project_uuid,
                                                 start_position,
                                                 page_size)

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_floating_ip_list(self, team_uuid, project_uuid, user_uuid,
                            page_size, page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as floatingip_uuid, a.name, a.description, " \
              "a.router_uuid, a.fixed_ip_address, a.floating_ip_address," \
              "a.revision_number, a.port_id, a.create_time, a.update_time, " \
              "a.vm_uuid, a.status from floating_ip a, " \
              "resources_acl b WHERE a.is_show=1 and a.uuid=b.resource_uuid " \
              "and b.team_uuid='%s' and b.project_uuid='%s' and " \
              "b.user_uuid='%s' order by " \
              "create_time DESC limit %d, %d" % (team_uuid,
                                                 project_uuid,
                                                 user_uuid,
                                                 start_position,
                                                 page_size)
        return super(NetworkDB, self).exec_select_sql(sql)

    def floatingip_project_count(self, team_uuid, project_uuid):
        sql = "select count(*) from  floating_ip a, " \
              "resources_acl b WHERE a.is_show=1 and a.uuid=b.resource_uuid " \
              "and b.team_uuid='%s' and b.project_uuid='%s'" % (team_uuid,
                                                                project_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def floatingip_user_count(self, team_uuid, project_uuid, user_uuid):
        sql = "select count(*) from floating_ip a, " \
              "resources_acl b WHERE a.is_show=1 and a.uuid=b.resource_uuid " \
              "and b.team_uuid='%s' and b.project_uuid='%s' " \
              "and b.user_uuid='%s'" % (team_uuid,
                                        project_uuid,
                                        user_uuid)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_floating_ip_detail(self, floatingip_uuid):
        sql = "select a.uuid as floatingip_uuid, a.name, a.description, " \
              "a.router_uuid, a.fixed_ip_address, a.floating_ip_address," \
              "a.revision_number, a.port_id, a.create_time, a.update_time, " \
              "a.vm_uuid, a.status from floating_ip a where " \
              "a.uuid='%s'" % floatingip_uuid

        return super(NetworkDB, self).exec_select_sql(sql)

    def db_is_floating_ip_del(self, floatingip_uuid):
        sql = "select count(fixed_ip_address) from floating_ip " \
              "where uuid='%s' and fixed_ip_address !='None'" % floatingip_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_floating_ip_logic_del(self, floatingip_uuid):
        sql = "update floating_ip set is_show=0 where " \
              "uuid='%s'" % floatingip_uuid

        return super(NetworkDB, self).exec_update_sql(sql)

    def db_floating_ip_rollback(self, floatingip_uuid):
        sql = "update floating_ip set is_show=1 where " \
              "uuid='%s'" % floatingip_uuid

        return super(NetworkDB, self).exec_update_sql(sql)

    def db_floating_ip_delete(self, floatingip_uuid):
        sql = "delete from floating_ip where uuid='%s'" % floatingip_uuid

        return super(NetworkDB, self).exec_update_sql(sql)

    def db_check_floatingip_status(self, floatingip_uuid):
        sql = "select status from floating_ip where " \
              "uuid='%s'" % floatingip_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_get_floatingip_uuid(self, floatip):
        sql = "select uuid from floating_ip where floating_ip_" \
              "address='%s'" % floatip
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_check_floatingip_bind(self, floatingip_uuid):
        sql = "select count(*) from floating_ip where uuid='%s' " \
              "and vm_uuid is not NULL and vm_uuid != 'None'" % floatingip_uuid
        log.debug('check the floatingip bind sql is: %s' % sql)
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_get_floatingip_addr(self, floatingip_uuid):
        sql = "select floating_ip_address, vm_uuid, fixed_ip_address from " \
              "floating_ip where " \
              "uuid='%s'" % floatingip_uuid
        return super(NetworkDB, self).exec_select_sql(sql)

    def db_floating_ip_bind(self, vm_uuid, floatingip_uuid, fixed_address):
        sql = "update floating_ip set vm_uuid='%s', fixed_ip_address='%s', " \
              "status='in-use' where uuid='%s'" % (vm_uuid, fixed_address, floatingip_uuid)
        return super(NetworkDB, self).exec_update_sql(sql)

    def db_floating_ip_unbind(self, floatingip_uuid):
        sql = "update floating_ip set vm_uuid=NULL, fixed_ip_address='None', " \
              "status='available' where uuid='%s'" % floatingip_uuid
        return super(NetworkDB, self).exec_update_sql(sql)
