# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>
# MariaDB init
# 注意，执行该初始化操作前需要先在数据库中创建相应用户和库。


sql_01 = "CREATE TABLE IF NOT EXISTS resources_acl ( \
          resource_uuid       VARCHAR(64) NULL DEFAULT NULL, \
          resource_type       VARCHAR(64) NULL DEFAULT NULL, \
          admin_uuid          VARCHAR(64) NULL DEFAULT NULL, \
          team_uuid           VARCHAR(64) NULL DEFAULT NULL, \
          project_uuid        VARCHAR(64) NULL DEFAULT NULL, \
          user_uuid           VARCHAR(64) NULL DEFAULT NULL, \
          create_time         DATETIME NULL DEFAULT NULL, \
          update_time         DATETIME NULL DEFAULT NULL, \
          PRIMARY KEY (resource_uuid) \
          ) \
          COLLATE='utf8_general_ci' \
          ENGINE=InnoDB"


sql_02 = "create index if not exists type_project_idx \
          on resources_acl(resource_type, project_uuid)"


sql_03 = "CREATE TABLE IF NOT EXISTS cloudhosts ( \
          vm_uuid             VARCHAR(64) NULL DEFAULT NULL, \
          vm_name             VARCHAR(64) NULL DEFAULT NULL, \
          image_name          VARCHAR(64) NULL DEFAULT NULL, \
          vm_ip               VARCHAR(512) NULL DEFAULT NULL, \
          floatip             VARCHAR(64) NULL DEFAULT NULL, \
          vm_cpu              INT(8) NULL DEFAULT NULL, \
          vm_mem              INT(8) NULL DEFAULT NULL, \
          vm_disk             VARCHAR(512) NULL DEFAULT NULL, \
          vm_nic              VARCHAR(512) NULL DEFAULT NULL, \
          availzone_uuid      VARCHAR(64) NULL DEFAULT NULL, \
          availzone_name      VARCHAR(32) NULL DEFAULT NULL, \
          login_way           VARCHAR(32) NULL DEFAULT NULL, \
          keys_name           VARCHAR(32) NULL DEFAULT NULL, \
          status              VARCHAR(32) NULL DEFAULT NULL, \
          create_time         DATETIME NULL DEFAULT NULL, \
          update_time         DATETIME NULL DEFAULT NULL, \
          PRIMARY KEY (vm_uuid) \
          ) \
          COLLATE='utf8_general_ci' \
          ENGINE=InnoDB"


sql_04 = "CREATE TABLE IF NOT EXISTS snapshots ( \
          snapshot_uuid       VARCHAR(64) NULL DEFAULT NULL, \
          snapshot_name       VARCHAR(64) NULL DEFAULT NULL, \
          vm_uuid             VARCHAR(64) NULL DEFAULT NULL, \
          vm_ip               VARCHAR(512) NULL DEFAULT NULL, \
          vm_cpu              INT(8) NULL DEFAULT NULL, \
          vm_mem              INT(8) NULL DEFAULT NULL, \
          vm_disk             VARCHAR(4096) NULL DEFAULT NULL, \
          vm_nic              VARCHAR(4096) NULL DEFAULT NULL, \
          disk_snapshot       VARCHAR(4096) NULL DEFAULT NULL, \
          availzone_uuid      VARCHAR(64) NULL DEFAULT NULL, \
          availzone_name      VARCHAR(32) NULL DEFAULT NULL, \
          comment             VARCHAR(512) NULL DEFAULT NULL, \
          status              VARCHAR(32) NULL DEFAULT NULL, \
          create_time         DATETIME NULL DEFAULT NULL, \
          update_time         DATETIME NULL DEFAULT NULL, \
          PRIMARY KEY (snapshot_uuid) \
          ) \
          COLLATE='utf8_general_ci' \
          ENGINE=InnoDB"


sql_05 = "insert into resources_acl \
          SELECT '%s', 'api', 'global', \
          '0', '0', '0', now(), now() \
          FROM dual WHERE NOT EXISTS \
          (SELECT resource_uuid FROM resources_acl \
           WHERE resource_uuid='%s')" \
         % ('cmp_cmp_adm_com', 'cmp_cmp_adm_com')


sql_06 = "insert into resources_acl \
          SELECT '%s', 'api', 'global', \
          'global', '0', '0', now(), now() \
          FROM dual WHERE NOT EXISTS \
          (SELECT resource_uuid FROM resources_acl \
           WHERE resource_uuid='%s')" \
         % ('cmp_cmp_tem_com', 'cmp_cmp_tem_com')


sql_07 = "insert into resources_acl \
          SELECT '%s', 'api', 'global', \
          'global', 'global', '0', now(), now() \
          FROM dual WHERE NOT EXISTS \
          (SELECT resource_uuid FROM resources_acl \
           WHERE resource_uuid='%s')" \
         % ('cmp_cmp_pro_com', 'cmp_cmp_pro_com')


sql_08 = "insert into resources_acl \
          SELECT '%s', 'api', 'global', \
          'global', 'global', 'global', now(), now() \
          FROM dual WHERE NOT EXISTS \
          (SELECT resource_uuid FROM resources_acl \
           WHERE resource_uuid='%s')" \
         % ('cmp_cmp_usr_com', 'cmp_cmp_usr_com')


init_sqls = [sql_01, sql_02, sql_03, sql_04,
             sql_05, sql_06, sql_07, sql_08]
