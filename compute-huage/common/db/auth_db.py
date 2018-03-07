# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

from conf import conf

from common.mysql_base import MysqlInit
from common.logs import logging as log


class AuthDB(MysqlInit):

    def __init__(self, service_name=None):

        if service_name in (None, 'ucenter', 'billing'):
            super(AuthDB, self).__init__()
        elif service_name == 'compute':
            super(AuthDB, self).__init__(db_user=conf.compute_db_user,
                                         db_passwd=conf.compute_db_passwd,
                                         database=conf.compute_database)
        elif service_name == 'storage':
            super(AuthDB, self).__init__(db_user=conf.storage_db_user,
                                         db_passwd=conf.storage_db_passwd,
                                         database=conf.storage_database)
        elif service_name == 'network':
            super(AuthDB, self).__init__(db_user=conf.network_db_user,
                                         db_passwd=conf.network_db_passwd,
                                         database=conf.network_database)

    def admin_acl_check(self, resource_uuid):

        sql = "select admin_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]

    def team_acl_check(self, resource_uuid):

        sql = "select team_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]

    def project_acl_check(self, resource_uuid):

        sql = "select project_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]

    def user_acl_check(self, resource_uuid):

        sql = "select user_uuid from resources_acl where resource_uuid = '%s'" \
              % (resource_uuid)

        return super(AuthDB, self).exec_select_sql(sql)[0][0]
