# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

import json

from conf import conf
from common.mysql_base import MysqlInit
from common.logs import logging as log
from common.json_encode import CJsonEncoder
from common.redis_base import RedisCache

from compute_init import init_sqls


class ComputeDB(MysqlInit):

    def __init__(self):

        super(ComputeDB, self).__init__(db_user=conf.compute_db_user,
                                        db_passwd=conf.compute_db_passwd,
                                        database=conf.compute_database)

        self.redis_cache = RedisCache()

        for sql in init_sqls:
            super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_create(self, vm_uuid, vm_name, image_name,
                         vm_ip, vm_cpu, vm_mem, vm_disk, vm_nic,
                         availzone_uuid, availzone_name,
                         login_way, keys_name,
                         team_uuid, project_uuid, user_uuid):

        vm_ip = ";".join(str(x) for x in vm_ip)
        vm_disk = ";".join([json.dumps(x) for x in vm_disk])
        vm_nic = ";".join([json.dumps(x) for x in vm_nic])

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'cloudhost', '0', '%s', '%s', '%s', now(), now())" \
                 % (vm_uuid, team_uuid, project_uuid, user_uuid)

        sql_02 = "insert into cloudhosts(vm_uuid, vm_name, image_name, \
                  vm_ip, floatip, vm_cpu, vm_mem, vm_disk, vm_nic, \
                  availzone_uuid, availzone_name, login_way, keys_name, \
                  status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', 'None', '%s', '%s', '%s', \
                  '%s', '%s', '%s', '%s', '%s', 'off', now(), now())" \
                 % (vm_uuid, vm_name, image_name, vm_ip, vm_cpu,
                    vm_mem, vm_disk, vm_nic, availzone_uuid,
                    availzone_name, login_way, keys_name)

        return super(ComputeDB, self).exec_update_sql(sql_01, sql_02)

    def cloudhost_list_team(self, team_uuid):

        sql = "select a.vm_uuid from cloudhosts a join resources_acl b \
               where a.vm_uuid=b.resource_uuid \
               and b.team_uuid='%s' and a.status!='delete'" \
              % (team_uuid)

        cloudhosts_list_info = super(ComputeDB, self).exec_select_sql(sql)

        result_list = []
        for cloudhost_info in cloudhosts_list_info:
            vm_uuid = cloudhost_info[0]

            v_result = {"vm_uuid": vm_uuid}
            result_list.append(v_result)

        return {"cloudhost_list": result_list}

    def cloudhost_list_project(self, team_uuid, project_uuid,
                               page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.vm_uuid, a.vm_name, a.image_name, a.vm_ip, \
                  a.floatip, a.vm_cpu, a.vm_mem, a.availzone_uuid, \
                  a.availzone_name, a.status, a.create_time, a.update_time \
                  from cloudhosts a join resources_acl b \
                  where a.vm_uuid=b.resource_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and a.status!='delete'" \
                 % (team_uuid, project_uuid)

        sql_02 = "select count(*) from cloudhosts a join resources_acl b \
                  where a.vm_uuid=b.resource_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and a.status!='delete'" \
                 % (team_uuid, project_uuid)

        cloudhosts_list_info = super(ComputeDB, self).exec_select_sql(sql_01)
        count = super(ComputeDB, self).exec_select_sql(sql_02)[0][0]

        result_list = []
        for cloudhost_info in cloudhosts_list_info:
            vm_uuid = cloudhost_info[0]
            vm_name = cloudhost_info[1]
            image_name = cloudhost_info[2]
            vm_ip = cloudhost_info[3]
            floatip = cloudhost_info[4]
            vm_cpu = cloudhost_info[5]
            vm_mem = cloudhost_info[6]
            availzone_uuid = cloudhost_info[7]
            availzone_name = cloudhost_info[8]
            status = cloudhost_info[9]
            create_time = cloudhost_info[10]
            update_time = cloudhost_info[11]

            vm_ip = [str(x) for x in vm_ip.split(";")]

            v_result = {
                           "vm_uuid": vm_uuid,
                           "vm_name": vm_name,
                           "image_name": image_name,
                           "vm_ip": vm_ip,
                           "floatip": floatip,
                           "vm_cpu": vm_cpu,
                           "vm_mem": vm_mem,
                           "availzone_uuid": availzone_uuid,
                           "availzone_name": availzone_name,
                           "status": status,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        return {
                   "cloudhost_list": result_list,
                   "count": count
               }

    def cloudhost_list_user(self, team_uuid, project_uuid,
                            user_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.vm_uuid, a.vm_name, a.image_name, a.vm_ip, \
                  a.floatip, a.vm_cpu, a.vm_mem, a.availzone_uuid, \
                  a.availzone_name, a.status, a.create_time, a.update_time \
                  from cloudhosts a join resources_acl b \
                  where a.vm_uuid=b.resource_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s' and a.status!='delete'" \
                 % (team_uuid, project_uuid, user_uuid)

        sql_02 = "select count(*) from cloudhosts a join resources_acl b \
                  where a.vm_uuid=b.resource_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s' and a.status!='delete'" \
                 % (team_uuid, project_uuid, user_uuid)

        cloudhosts_list_info = super(ComputeDB, self).exec_select_sql(sql)
        count = super(ComputeDB, self).exec_select_sql(sql_02)[0][0]

        result_list = []
        for cloudhost_info in cloudhosts_list_info:
            vm_uuid = cloudhost_info[0]
            vm_name = cloudhost_info[1]
            image_name = cloudhost_info[2]
            vm_ip = cloudhost_info[3]
            floatip = cloudhost_info[4]
            vm_cpu = cloudhost_info[5]
            vm_mem = cloudhost_info[6]
            availzone_uuid = cloudhost_info[7]
            availzone_name = cloudhost_info[8]
            status = cloudhost_info[9]
            create_time = cloudhost_info[10]
            update_time = cloudhost_info[11]

            vm_ip = [str(x) for x in vm_ip.split(";")]

            v_result = {
                           "vm_uuid": vm_uuid,
                           "vm_name": vm_name,
                           "image_name": image_name,
                           "vm_ip": vm_ip,
                           "floatip": floatip,
                           "vm_cpu": vm_cpu,
                           "vm_mem": vm_mem,
                           "availzone_uuid": availzone_uuid,
                           "availzone_name": availzone_name,
                           "status": status,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        return {
                   "cloudhost_list": result_list,
                   "count": count
               }

    def cloudhost_list_dead(self):

        sql = "select vm_uuid, vm_name \
               from cloudhosts where status='delete' \
               and update_time<date_sub(now(), interval 7 day)"

        cloudhosts_list_info = super(ComputeDB, self).exec_select_sql(sql)

        result_list = []
        for cloudhost_info in cloudhosts_list_info:
            vm_uuid = cloudhost_info[0]
            vm_name = cloudhost_info[1]

            v_result = {
                           "vm_uuid": vm_uuid,
                           "vm_name": vm_name
                       }
            result_list.append(v_result)

        return {"cloudhost_list": result_list}

    def cloudhost_list_on(self):

        # 虚拟机状态维护时需要用到

        sql = "select vm_uuid from cloudhosts where status='on'"

        cloudhosts_list_info = super(ComputeDB, self).exec_select_sql(sql)

        result_list = []
        for cloudhost_info in cloudhosts_list_info:
            vm_uuid = cloudhost_info[0]

            v_result = {"vm_uuid": vm_uuid}
            result_list.append(v_result)

        return {"cloudhost_list": result_list}

    def cloudhost_info(self, vm_uuid):

        sql = "select vm_name, image_name, vm_ip, floatip, \
               vm_cpu, vm_mem, vm_disk, vm_nic, availzone_uuid, \
               availzone_name, login_way, keys_name, \
               status, create_time, update_time \
               from cloudhosts where vm_uuid='%s'" \
              % (vm_uuid)

        cloudhost_info = super(ComputeDB, self).exec_select_sql(sql)

        vm_name = cloudhost_info[0][0]
        image_name = cloudhost_info[0][1]
        vm_ip = cloudhost_info[0][2]
        floatip = cloudhost_info[0][3]
        vm_cpu = cloudhost_info[0][4]
        vm_mem = cloudhost_info[0][5]
        vm_disk = cloudhost_info[0][6]
        vm_nic = cloudhost_info[0][7]
        availzone_uuid = cloudhost_info[0][8]
        availzone_name = cloudhost_info[0][9]
        login_way = cloudhost_info[0][10]
        keys_name = cloudhost_info[0][11]
        status = cloudhost_info[0][12]
        create_time = cloudhost_info[0][13]
        update_time = cloudhost_info[0][14]

        vm_ip = [str(x) for x in vm_ip.split(";")]
        vm_disk = [json.loads(x) for x in vm_disk.split(";")]
        vm_nic = [json.loads(x) for x in vm_nic.split(";")]

        v_result = {
                       "vm_uuid": vm_uuid,
                       "vm_name": vm_name,
                       "image_name": image_name,
                       "vm_ip": vm_ip,
                       "floatip": floatip,
                       "vm_cpu": vm_cpu,
                       "vm_mem": vm_mem,
                       "vm_disk": vm_disk,
                       "vm_nic": vm_nic,
                       "availzone_uuid": availzone_uuid,
                       "availzone_name": availzone_name,
                       "login_way": login_way,
                       "keys_name": keys_name,
                       "status": status,
                       "create_time": create_time,
                       "update_time": update_time
                   }

        v_result = json.dumps(v_result, cls=CJsonEncoder)
        result = json.loads(v_result)

        return {"cloudhost_info": result}

    def cloudhost_init_info(self, vm_mac):

        mac = r'%' + vm_mac + r'%'

        sql = "select vm_uuid, vm_name, vm_nic, password \
               from cloudhosts where vm_nic like '%s'" \
              % (mac)

        cloudhost_info = super(ComputeDB, self).exec_select_sql(sql)

        vm_uuid = cloudhost_info[0][0]
        vm_name = cloudhost_info[0][1]
        vm_nic = cloudhost_info[0][2]
        password = cloudhost_info[0][3]

        vm_nic = [json.loads(x) for x in vm_nic.split(";")]

        result = {
                     "vm_uuid": vm_uuid,
                     "vm_name": vm_name,
                     "vm_nic": vm_nic,
                     "password": password
                 }

        return {"cloudhost_info": result}

    def cloudhost_status_update(self, vm_uuid, status):

        # 更新时，先从redis中获取该vm状态值进行比对，
        # 不一致时才进行数据库更新，并更新redis缓存值。
        try:
            status_cached = self.redis_cache.get_data(vm_uuid)
            self.redis_cache.set_data(vm_uuid, status, 60)
            if status == status_cached:
                return
        except Exception, e:
            log.warning('redis operation failure, reason=%s' % (e))

        sql = "update cloudhosts set status='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (status, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_cpu_update(self, vm_uuid, vm_cpu):

        sql = "update cloudhosts set vm_cpu='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (vm_cpu, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_mem_update(self, vm_uuid, vm_mem):

        sql = "update cloudhosts set vm_mem='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (vm_mem, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_disk_update(self, vm_uuid, vm_disk):

        vm_disk = ";".join([json.dumps(x) for x in vm_disk])

        sql = "update cloudhosts set vm_disk='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (vm_disk, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_vnic_update(self, vm_uuid, vm_ip, vm_nic):

        vm_ip = ";".join(str(x) for x in vm_ip)
        vm_nic = ";".join([json.dumps(x) for x in vm_nic])

        sql = "update cloudhosts set vm_ip='%s', vm_nic='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (vm_ip, vm_nic, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_floatip_update(self, vm_uuid, floatip):

        sql = "update cloudhosts set floatip='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (floatip, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def cloudhost_delete(self, vm_uuid):

        sql_01 = "delete from cloudhosts where vm_uuid='%s'" \
                 % (vm_uuid)

        sql_02 = "delete from resources_acl where resource_uuid='%s'" \
                 % (vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql_01, sql_02)

    def snapshot_name_check(self, snapshot_name,
                            project_uuid, cluster_uuid):

        sql = "select count(*) from snapshots a join resources_acl b \
               where a.snapshot_uuid=b.resource_uuid \
               and a.snapshot_name='%s' and a.cluster_uuid='%s' \
               and b.project_uuid='%s'" \
               % (snapshot_name, cluster_uuid, project_uuid)

        name_check = super(ComputeDB, self).exec_select_sql(sql)[0][0]

        return {"name_check": name_check}

    def snapshot_create(self, snapshot_uuid, snapshot_name,
                        vm_uuid, vm_ip, vm_cpu, vm_mem,
                        vm_disk, vm_nic, disk_snapshot,
                        availzone_uuid, availzone_name, comment,
                        team_uuid, project_uuid, user_uuid):

        vm_ip = ";".join(str(x) for x in vm_ip)
        vm_disk = ";".join([json.dumps(x) for x in vm_disk])
        vm_nic = ";".join([json.dumps(x) for x in vm_nic])
        disk_snapshot = ";".join(json.dumps(x) for x in disk_snapshot)

        sql_01 = "insert into resources_acl(resource_uuid, resource_type, \
                  admin_uuid, team_uuid, project_uuid, user_uuid, \
                  create_time, update_time) \
                  values('%s', 'snapshot', '0', '%s', '%s', '%s', now(), now())" \
                 % (snapshot_uuid, team_uuid, project_uuid, user_uuid)

        sql_02 = "insert into snapshots(snapshot_uuid, snapshot_name, \
                  vm_uuid, vm_ip, vm_cpu, vm_mem, vm_disk, vm_nic, \
                  disk_snapshot, availzone_uuid, availzone_name, comment, \
                  status, create_time, update_time) \
                  values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                  '%s', '%s', '%s', '%s', 'on', now(), now())" \
                 % (snapshot_uuid, snapshot_name, vm_uuid, vm_ip,
                    vm_cpu, vm_mem, vm_disk, vm_nic, disk_snapshot,
                    availzone_uuid, availzone_name, comment)

        return super(ComputeDB, self).exec_update_sql(sql_01, sql_02)

    def snapshot_list_project(self, team_uuid, project_uuid,
                              page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.snapshot_uuid, a.snapshot_name, a.vm_uuid, \
                  a.availzone_uuid, a.availzone_name, a.comment, \
                  a.status, a.create_time, a.update_time, c.vm_name \
                  from snapshots a join resources_acl b join cloudhosts c \
                  where a.snapshot_uuid=b.resource_uuid \
                  and a.vm_uuid=c.vm_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and a.status!='delete' \
                  limit %d,%d" \
                 % (team_uuid, project_uuid,
                    start_position, page_size)

        sql_02 = "select count(*) from snapshots a join resources_acl b \
                  where a.snapshot_uuid=b.resource_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and a.status!='delete'" \
                 % (team_uuid, project_uuid)

        snapshots_list = super(ComputeDB, self).exec_select_sql(sql_01)
        count = super(ComputeDB, self).exec_select_sql(sql_02)[0][0]

        result_list = []
        for snapshot_info in snapshots_list:
            snapshot_uuid = snapshot_info[0]
            snapshot_name = snapshot_info[1]
            vm_uuid = snapshot_info[2]
            availzone_uuid = snapshot_info[3]
            availzone_name = snapshot_info[4]
            comment = snapshot_info[5]
            status = snapshot_info[6]
            create_time = snapshot_info[7]
            update_time = snapshot_info[8]
            vm_name = snapshot_info[9]

            v_result = {
                           "snapshot_uuid": snapshot_uuid,
                           "snapshot_name": snapshot_name,
                           "vm_uuid": vm_uuid,
                           "vm_name": vm_name,
                           "availzone_uuid": availzone_uuid,
                           "availzone_name": availzone_name,
                           "comment": comment,
                           "status": status,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        return {
                   "snapshot_list": result_list,
                   "count": count
               }

    def snapshot_list_user(self, team_uuid, project_uuid,
                           user_uuid, page_size, page_num):

        page_size = int(page_size)
        page_num = int(page_num)
        start_position = (page_num - 1) * page_size

        sql_01 = "select a.snapshot_uuid, a.snapshot_name, a.vm_uuid, \
                  a.availzone_uuid, a.availzone_name, a.comment, \
                  a.status, a.create_time, a.update_time, c.vm_name \
                  from snapshots a join resources_acl b join cloudhosts c \
                  where a.snapshot_uuid=b.resource_uuid \
                  and a.vm_uuid=c.vm_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s' \
                  and a.status!='delete' \
                  limit %d,%d" \
                 % (team_uuid, project_uuid,
                    user_uuid, start_position, page_size)

        sql_02 = "select count(*) from snapshots a join resources_acl b \
                  where a.snapshot_uuid=b.resource_uuid \
                  and b.team_uuid='%s' and b.project_uuid='%s' \
                  and b.user_uuid='%s' \
                  and a.status!='delete'" \
                 % (team_uuid, project_uuid, user_uuid)

        snapshots_list = super(ComputeDB, self).exec_select_sql(sql_01)
        count = super(ComputeDB, self).exec_select_sql(sql_02)[0][0]

        result_list = []
        for snapshot_info in snapshots_list:
            snapshot_uuid = snapshot_info[0]
            snapshot_name = snapshot_info[1]
            vm_uuid = snapshot_info[2]
            availzone_uuid = snapshot_info[3]
            availzone_name = snapshot_info[4]
            comment = snapshot_info[5]
            status = snapshot_info[6]
            create_time = snapshot_info[7]
            update_time = snapshot_info[8]
            vm_name = snapshot_info[9]

            v_result = {
                           "snapshot_uuid": snapshot_uuid,
                           "snapshot_name": snapshot_name,
                           "vm_uuid": vm_uuid,
                           "vm_name": vm_name,
                           "availzone_uuid": availzone_uuid,
                           "availzone_name": availzone_name,
                           "comment": comment,
                           "status": status,
                           "create_time": create_time,
                           "update_time": update_time
                       }

            v_result = json.dumps(v_result, cls=CJsonEncoder)
            v_result = json.loads(v_result)
            result_list.append(v_result)

        return {
                   "snapshot_list": result_list,
                   "count": count
               }

    def snapshot_info(self, snapshot_uuid):

        sql = "select snapshot_name, vm_uuid, vm_ip, vm_cpu, vm_mem, \
               vm_disk, vm_nic, disk_snapshot, availzone_uuid, \
               availzone_name, comment, status, create_time, update_time \
               from snapshots where snapshot_uuid='%s'" \
              % (snapshot_uuid)

        snapshot_info = super(ComputeDB, self).exec_select_sql(sql)

        snapshot_name = snapshot_info[0][0]
        vm_uuid = snapshot_info[0][1]
        vm_ip = snapshot_info[0][2]
        vm_cpu = snapshot_info[0][3]
        vm_mem = snapshot_info[0][4]
        vm_disk = snapshot_info[0][5]
        vm_nic = snapshot_info[0][6]
        disk_snapshot = snapshot_info[0][7]
        availzone_uuid = snapshot_info[0][8]
        availzone_name = snapshot_info[0][9]
        comment = snapshot_info[0][10]
        status = snapshot_info[0][11]
        create_time = snapshot_info[0][12]
        update_time = snapshot_info[0][13]

        vm_ip = [str(x) for x in vm_ip.split(";")]
        vm_disk = [json.loads(x) for x in vm_disk.split(";")]
        vm_nic = [json.loads(x) for x in vm_nic.split(";")]
        disk_snapshot = [json.loads(x) for x in disk_snapshot.split(";")]

        v_result = {
                       "snapshot_uuid": snapshot_uuid,
                       "snapshot_name": snapshot_name,
                       "vm_uuid": vm_uuid,
                       "vm_ip": vm_ip,
                       "vm_cpu": vm_cpu,
                       "vm_mem": vm_mem,
                       "vm_disk": vm_disk,
                       "vm_nic": vm_nic,
                       "disk_snapshot": disk_snapshot,
                       "availzone_uuid": availzone_uuid,
                       "availzone_name": availzone_name,
                       "comment": comment,
                       "status": status,
                       "create_time": create_time,
                       "update_time": update_time
                   }

        v_result = json.dumps(v_result, cls=CJsonEncoder)

        result = json.loads(v_result)

        return {"snapshot_info": result}

    def snapshot_revert(self, vm_uuid, vm_ip, vm_cpu,
                        vm_mem, vm_disk, vm_nic):

        vm_ip = ";".join(str(x) for x in vm_ip)
        vm_disk = ";".join([json.dumps(x) for x in vm_disk])
        vm_nic = ";".join([json.dumps(x) for x in vm_nic])

        sql = "update cloudhosts set vm_ip='%s', vm_cpu='%s', \
               vm_mem='%s', vm_disk='%s', vm_nic='%s', \
               update_time=now() where vm_uuid='%s'" \
              % (vm_ip, vm_cpu, vm_mem, vm_disk, vm_nic, vm_uuid)

        return super(ComputeDB, self).exec_update_sql(sql)

    def snapshot_delete(self, snapshot_uuid):

        sql_01 = "delete from resources_acl where resource_uuid='%s'" \
                 % (snapshot_uuid)

        sql_02 = "delete from snapshots where snapshot_uuid='%s'" \
                 % (snapshot_uuid)

        return super(ComputeDB, self).exec_update_sql(sql_01, sql_02)
