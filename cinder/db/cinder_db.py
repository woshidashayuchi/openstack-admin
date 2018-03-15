# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/24 14:15
from common.db.mysql_base import MysqlInit
from common.logs import logging as log


class CinderDB(MysqlInit):

    def __init__(self):
        super(CinderDB, self).__init__()

    def data_init(self):
        # volume api acl db init
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

        # sanpshot api acl db init
        sql5 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'0', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('vol_snap_adm_com', 'vol_snap_adm_com')

        sql6 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('vol_snap_tem_com', 'vol_snap_tem_com')

        sql7 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', '0', now(), now() FROM dual WHERE NOT " \
               "EXISTS (SELECT resource_uuid FROM resources_acl " \
               "WHERE resource_uuid='%s')" % ('vol_snap_pro_com',
                                              'vol_snap_pro_com')

        sql8 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', 'global', now(), now() FROM dual WHERE " \
               "NOT EXISTS (SELECT resource_uuid FROM resources_acl WHERE " \
               "resource_uuid='%s')" % ('vol_snap_usr_com', 'vol_snap_usr_com')

        # attachment api acl db init
        sql9 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'0', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('vol_attach_adm_com', 'vol_attach_adm_com')

        sql10 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', '0', '0', now(), now() FROM dual WHERE NOT EXISTS " \
               "(SELECT resource_uuid FROM resources_acl WHERE resource_" \
               "uuid='%s')" % ('vol_attach_tem_com', 'vol_attach_tem_com')

        sql11 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', '0', now(), now() FROM dual WHERE NOT " \
               "EXISTS (SELECT resource_uuid FROM resources_acl " \
               "WHERE resource_uuid='%s')" % ('vol_attach_pro_com',
                                              'vol_attach_pro_com')

        sql12 = "insert into resources_acl SELECT '%s', 'api', 'global', " \
               "'global', 'global', 'global', now(), now() FROM dual WHERE " \
               "NOT EXISTS (SELECT resource_uuid FROM resources_acl WHERE " \
               "resource_uuid='%s')" % ('vol_attach_usr_com',
                                        'vol_attach_usr_com')

        return super(CinderDB, self).exec_update_sql(sql1, sql2, sql3, sql4,
                                                     sql5, sql6, sql7, sql8,
                                                     sql9, sql10, sql11, sql12)

    def volumes_list_get(self, user_uuid):
        sql = "SELECT * FROM volume WHERE user_uuid='%s'" % user_uuid

        log.info('operate the db sql is: %s' % sql)
        return super(CinderDB, self).exec_select_sql(sql)

    def volume_create(self, name, size, description, v_type, conn_to=None,
                      snapshot_uuid=None, is_use_domain=None, is_start=0,
                      is_secret=0, user_uuid=None, volume_uuid=None,
                      project_uuid=None, team_uuid=None,
                      source_volume_uuid=None, image_uuid=None):

        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (volume_uuid,
                                                              'volume',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

        sql = "insert into volume(uuid, " \
              "name, description, size, status, type, conn_to, " \
              "snapshot_uuid, source_volume_uuid, image_uuid, is_use_domain, is_start, " \
              "is_secret) VALUES " \
              "('%s', '%s', '%s', %d, '%s', '%s', '%s', " \
              "'%s', '%s', '%s', '%s', %d, %d)" % (volume_uuid,
                                                   name,
                                                   description,
                                                   size,
                                                   'creating',
                                                   v_type,
                                                   conn_to,
                                                   snapshot_uuid,
                                                   source_volume_uuid,
                                                   image_uuid,
                                                   is_use_domain,
                                                   is_start,
                                                   is_secret)

        return super(CinderDB, self).exec_update_sql(sql_acl, sql)

    def volume_list(self, team_uuid, project_uuid, user_uuid, page_size,
                    page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as volume_uuid, a.name, a.description, " \
              "a.size, a.status, a.type, a.conn_to, a.is_use_domain, " \
              "a.is_start, a.is_secret, a.snapshot_uuid, " \
              "a.source_volume_uuid, a.image_uuid, a.create_time " \
              "from volume a, resources_acl b where a.is_show=1 " \
              "and b.user_uuid='%s' " \
              "and b.project_uuid='%s' and " \
              "b.team_uuid='%s' and " \
              "a.uuid=b.resource_uuid limit %d, %d" % (user_uuid,
                                                       project_uuid,
                                                       team_uuid,
                                                       start_position,
                                                       page_size)
        log.info('-----sql----: %s' % sql)
        return super(CinderDB, self).exec_select_sql(sql)

    def volume_list_project(self, team_uuid, project_uuid, page_size,
                            page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as volume_uuid, a.name, a.description, " \
              "a.size, a.status, a.type, a.conn_to, a.is_use_domain, " \
              "a.is_start, a.is_secret, a.snapshot_uuid, " \
              "a.source_volume_uuid, a.image_uuid, a.create_time " \
              "from volume a, resources_acl b where a.is_show=1 and " \
              "b.project_uuid='%s' and b.team_uuid='%s' and " \
              "a.uuid=b.resource_uuid limit %d, %d" % (project_uuid,
                                                       team_uuid,
                                                       start_position,
                                                       page_size)

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_detail(self, volume_uuid):
        sql = "select uuid as volume_uuid, name, description, " \
              "size, status, type, conn_to, is_use_domain, is_start, " \
              "is_secret, snapshot_uuid, source_volume_uuid, image_uuid," \
              "create_time from volume where " \
              "uuid='%s'" % volume_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_if_can_delete(self, volume_uuid):
        sql = "select count(uuid) as snapshot_uuid from snapshot where " \
              "volume_uuid='%s'" % volume_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_logic_update(self, volume_uuid):
        sql = "update volume set is_show=0, " \
              "update_time=(select now() from dual) " \
              "where uuid='%s'" % volume_uuid
        return super(CinderDB, self).exec_update_sql(sql)

    def volume_delete(self, volume_uuid):
        # delete volume
        sql1 = "delete from volume WHERE uuid='%s'" % volume_uuid
        # delete acl
        sql2 = "delete from resources_acl where resource_uuid='%s'" % \
               volume_uuid
        return super(CinderDB, self).exec_update_sql(sql1, sql2)

    def volume_update(self, up_dict, volume_uuid):
        if up_dict.get('up_type') == 'recovery':
            sql = "update volume set is_show=1 where uuid='%s'" % volume_uuid
            return super(CinderDB, self).exec_update_sql(sql)

        up_columns = up_dict.keys()
        for column in up_columns:
            if column == 'volume_uuid':
                continue
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
                        metadata, size, volume_uuid, is_forced, user_uuid,
                        project_uuid, team_uuid):
        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values ('%s','%s','%s','%s','%s','%s')" % (snapshot_uuid,
                                                              'snapshot',
                                                              '0',
                                                              team_uuid,
                                                              project_uuid,
                                                              user_uuid)

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

        return super(CinderDB, self).exec_update_sql(sql_acl, sql)

    def snap_list_project(self, team_uuid, project_uuid, page_size,
                          page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as snapshot_uuid, a.name, a.description, " \
              "a.status, a.metadata, a.size, a.volume_uuid, a.is_forced, " \
              "a.create_time from snapshot a, resources_acl b where " \
              "b.team_uuid='%s' and b.project_uuid='%s' and a.is_show=1 " \
              "and a.uuid=b.resource_uuid " \
              "order by a.create_time desc limit %d, %d" % (team_uuid,
                                                            project_uuid,
                                                            start_position,
                                                            page_size)

        return super(CinderDB, self).exec_select_sql(sql)

    def snapshot_list(self, team_uuid, project_uuid, user_uuid, page_size,
                    page_num):
        start_position = (page_num - 1) * page_size
        sql = "select a.uuid as snapshot_uuid, a.name, a.description, " \
              "a.status, a.metadata, a.size, a.volume_uuid, a.is_forced, " \
              "a.create_time from snapshot a, resources_acl b where " \
              "a.is_show=1 and b.project_uuid='%s' and b.team_uuid='%s' " \
              "and b.user_uuid='%s' and a.uuid=b.resource_uuid  " \
              "order by a.create_time desc limit %d, %d" % (project_uuid,
                                                            team_uuid,
                                                            user_uuid,
                                                            start_position,
                                                            page_size)

        return super(CinderDB, self).exec_select_sql(sql)

    def snapshot_detail(self, snapshot_uuid):
        sql = "select uuid as snapshot_uuid, name, description, status, " \
              "metadata, size, volume_uuid, is_forced, create_time from " \
              "snapshot where uuid='%s'" % snapshot_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def snapshot_delete(self, snapshot_uuid):
        sql = "delete from snapshot where uuid='%s'" % snapshot_uuid
        # sql = "update snapshot set is_show=0 where uuid='%s'" % snapshot_uuid
        sql_acl = "delete from resources_acl where resource_uuid='%s'" \
                  % snapshot_uuid
        return super(CinderDB, self).exec_update_sql(sql, sql_acl)

    def snapshot_logic_delete(self, snapshot_uuid):
        sql = "update snapshot set is_show=0 where uuid='%s'" % snapshot_uuid

        return super(CinderDB, self).exec_update_sql(sql)

    def snapshot_update(self, up_dict, snapshot_uuid):
        up_columns = up_dict.keys()
        for column in up_columns:
            if column == 'snapshot_uuid':
                continue
            sql = "update snapshot set %s='%s' " \
                  "where uuid='%s'" % (column, up_dict[column], snapshot_uuid)

            super(CinderDB, self).exec_update_sql(sql)

        return

    # 状态监控查询需求
    def volume_status_monitor(self):
        sql = "select uuid as volume_uuid, status from volume"

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_status_update(self, volume_uuid, status):
        sql = "update volume set status='%s' where uuid='%s'" % (status,
                                                                 volume_uuid)

        return super(CinderDB, self).exec_update_sql(sql)

    # attachment
    def attachment_create(self, attachment_uuid, server_uuid, volume_uuid,
                          device, team_uuid, project_uuid, user_uuid):
        sql_acl = "insert into resources_acl(resource_uuid, resource_type," \
                  "admin_uuid, team_uuid, project_uuid, user_uuid) " \
                  "values('%s', '%s', '%s', '%s', '%s', " \
                  "'%s',)" % (attachment_uuid,
                              'attach',
                              '0',
                              team_uuid,
                              project_uuid,
                              user_uuid)

        sql = "insert into attachment(uuid, server_uuid, " \
              "volume_uuid, device) values ('%s', '%s', " \
              "'%s', '%s')" % (attachment_uuid,
                               server_uuid,
                               volume_uuid,
                               device)

        sql_volume_conn = "update volume set conn_to='%s' " \
                          "where uuid='%s'" % (server_uuid,
                                               volume_uuid)

        return super(CinderDB, self).exec_update_sql(sql_acl,
                                                     sql,
                                                     sql_volume_conn)

    def attachment_delete(self, attachment_uuid, conn_to):
        sql_volume = "update volume set conn_to='%s' where " \
                     "uuid=(select volume_uuid from attachment " \
                     "where uuid='%s' )" % (conn_to, attachment_uuid)

        sql = "delete from attachment where uuid='%s'" % attachment_uuid

        sql_acl = "delete from resources_acl where resource_" \
                  "uuid='%s'" % (attachment_uuid)

        return super(CinderDB, self).exec_update_sql(sql_volume,
                                                     sql,
                                                     sql_acl)
