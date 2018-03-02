# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/24 14:15
from common.db.mysql_base import MysqlInit
from common.logs import logging as log
import uuid


class CinderDB(MysqlInit):

    def __init__(self):
        super(CinderDB, self).__init__()

    def volumes_list_get(self, user_uuid):
        sql = "SELECT * FROM volume WHERE user_uuid='%s'" % user_uuid

        log.info('operate the db sql is: %s' % sql)
        return super(CinderDB, self).exec_select_sql(sql)

    def volume_create(self, name, size, description, v_type, conn_to=None,
                      is_use_domain=None, is_start=0, is_secret=0,
                      user_uuid=None, volume_uuid=None):
        sql = "insert into volume(uuid, user_uuid, name, description, size, " \
              "status, type, conn_to, is_use_domain, is_start, is_secret) " \
              "VALUES ('%s', '%s', '%s', '%s', %d, %d, '%s', '%s', '%s', " \
              "%d, %d)" % (volume_uuid, user_uuid, name, description, size,
                           0, v_type, conn_to, is_use_domain, is_start,
                           is_secret)

        return super(CinderDB, self).exec_update_sql(sql)

    def volume_list(self, user_uuid):
        sql = "select uuid as volume_uuid, user_uuid, name, description, " \
              "size, status, type, conn_to, is_use_domain, is_start, " \
              "is_secret, create_time from volume where " \
              "user_uuid='%s'" % user_uuid

        return super(CinderDB, self).exec_select_sql(sql)

    def volume_detail(self, volume_uuid):
        sql = "select uuid as volume_uuid, user_uuid, name, description, " \
              "size, status, type, conn_to, is_use_domain, is_start, " \
              "is_secret, create_time from volume where " \
              "uuid='%s'" % volume_uuid

        return super(CinderDB, self).exec_select_sql(sql)

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
        sql = "delete from snapshot where uuid='%s'" % snapshot_uuid
        return super(CinderDB, self).exec_update_sql(sql)
