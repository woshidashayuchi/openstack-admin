# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/24 14:15
from common.db.mysql_base import MysqlInit
from common.logs import logging as log
import uuid


class CinderDB(MysqlInit):

    def __init__(self):
        super(CinderDB, self).__init__()

    def data_init(self):
        sql1 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'0', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('vol_vol_adm_com', 'vol_vol_adm_com')

        sql2 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('vol_vol_tem_com', 'vol_vol_tem_com')

        sql3 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', '0', now(), now() FROM dual WHERE NOT " \
               "EXISTS (SELECT resource_uuid FROM resources_acl " \
               "WHERE resource_uuid='%s')" % ('vol_vol_pro_com',
                                              'vol_vol_pro_com')

        sql4 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', 'global', now(), now() FROM dual WHERE " \
               "NOT EXISTS (SELECT resource_uuid FROM resources_acl WHERE " \
               "resource_uuid='%s')" % ('vol_vol_usr_com', 'vol_vol_usr_com')

        return super(CinderDB, self).exec_update_sql(sql1, sql2, sql3, sql4)

    def volumes_list_get(self, user_uuid):
        sql = "SELECT * FROM volume WHERE user_uuid='%s'" % user_uuid

        log.info('operate the db sql is: %s' % sql)
        return super(CinderDB, self).exec_select_sql(sql)

    def volume_create(self, name, size, description, v_type, conn_to=None,
                      is_use_domain=None, is_start=0, is_secret=0,
                      user_uuid=None, volume_uuid=None, project_uuid=None,
                      team_uuid=None):

        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (volume_uuid,
                                                              'volume',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

        sql = "insert into volume(uuid, team_uuid, project_uuid, user_uuid, " \
              "name, description, size, status, type, conn_to, is_use_domain, " \
              "is_start, is_secret) VALUES ('%s', '%s', '%s', '%s', '%s', " \
              "'%s', %d, %d, '%s', '%s', '%s', %d, %d)" % (volume_uuid,
                                                           team_uuid,
                                                           project_uuid,
                                                           user_uuid,
                                                           name,
                                                           description,
                                                           size,
                                                           0,
                                                           v_type,
                                                           conn_to,
                                                           is_use_domain,
                                                           is_start,
                                                           is_secret)

        return super(CinderDB, self).exec_update_sql(sql_acl, sql)

    def volume_list(self, team_uuid, project_uuid, user_uuid, page_size,
                    page_num):
        start_position = (page_num - 1) * page_size
        sql = "select uuid as volume_uuid, user_uuid, name, description, " \
              "size, status, type, conn_to, is_use_domain, is_start, " \
              "is_secret, create_time from volume where " \
              "user_uuid='%s' and project_uuid='%s' and " \
              "team_uuid='%s' limit %d, %d" % (user_uuid, project_uuid,
                                               team_uuid, start_position,
                                               page_size)

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_list_project(self, team_uuid, project_uuid, page_size,
                            page_num):
        start_position = (page_num - 1) * page_size
        sql = "select uuid as volume_uuid, user_uuid, name, description, " \
              "size, status, type, conn_to, is_use_domain, is_start, " \
              "is_secret, create_time from volume where " \
              "project_uuid='%s' and " \
              "team_uuid='%s' limit %d, %d" % (project_uuid, team_uuid,
                                               start_position, page_size)

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_detail(self, volume_uuid):
        sql = "select uuid as volume_uuid, user_uuid, name, description, " \
              "size, status, type, conn_to, is_use_domain, is_start, " \
              "is_secret, create_time from volume where " \
              "uuid='%s'" % volume_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_logic_update(self, volume_uuid):
        sql = "update volume set is_show=0, " \
              "update_time=(select now() from dual) " \
              "where uuid='%s'" % volume_uuid
        return super(CinderDB, self).exec_update_sql(sql)

    def volume_delete(self, volume_uuid):
        sql = "delete from volume WHERE uuid='%s'" % volume_uuid

        return super(CinderDB, self).exec_update_sql(sql)

    def volume_update(self, up_dict, volume_uuid):
        up_columns = up_dict.keys()
        for column in up_columns:
            sql = "update volume set %s='%s' " \
                  "where uuid='%s'" % (column, up_dict[column], volume_uuid)

            super(CinderDB, self).exec_update_sql(sql)

        return

    # 过期自动删除
    def volume_expire_list(self):
        sql = "select uuid as volume_uuid from volume where " \
              "update_time<CURRENT_TIMESTAMP - INTERVAL 3 day"

        return super(CinderDB, self).exec_select_sql(sql)

    # volume type
    def volume_type_create(self, type_uuid, name, description, extra_specs):
        sql = "insert into volume_type(uuid, name, " \
              "description, extra_specs) VALUES ('%s', '%s'," \
              "'%s', '%s')" % (type_uuid, name, description,
                               extra_specs)

        return super(CinderDB, self).exec_update_sql(sql)

    def volume_type_list(self):
        sql = "select uuid, name, description, extra_specs, is_public, " \
              "create_time from volume_type"

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_type_detail(self, type_uuid):
        sql = "select uuid, name, description, extra_specs, is_public," \
              "create_time from volume_type where uuid='%s'" % type_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_type_delete(self, type_uuid):
        sql = "delete from volume_type where uuid='%s'" % type_uuid
        return super(CinderDB, self).exec_update_sql(sql)

    def snapshot_create(self, snapshot_uuid, name, description, status,
                        metadata, size, volume_uuid, is_forced):

        sql = "insert into snapshot(uuid, name, description, status, " \
              "metadata, size, volume_uuid, is_forced) VALUES ('%s'," \
              "'%s', '%s', '%s', '%s', %d, '%s', '%s')" % (snapshot_uuid,
                                                           name,
                                                           description,
                                                           status,
                                                           metadata,
                                                           size,
                                                           volume_uuid,
                                                           is_forced)

        return super(CinderDB, self).exec_update_sql(sql)

    def snapshot_list(self):
        sql = "select uuid as snapshot_uuid, name, description, status, " \
              "metadata, size, volume_uuid, is_forced, create_time from " \
              "snapshot"

        return super(CinderDB, self).exec_select_sql(sql)

    def snapshot_detail(self, snapshot_uuid):
        sql = "select uuid as snapshot_uuid, name, description, status, " \
              "metadata, size, volume_uuid, is_forced, create_time from " \
              "snapshot where uuid='%s'" % snapshot_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def snapshot_delete(self, snapshot_uuid):
        # sql = "delete from snapshot where uuid='%s'" % snapshot_uuid
        sql = "update snapshot set is_show=0 where uuid='%s'" % snapshot_uuid
        return super(CinderDB, self).exec_update_sql(sql)
