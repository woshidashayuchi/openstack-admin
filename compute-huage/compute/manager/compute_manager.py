# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

from conf import conf
from common.logs import logging as log
from common.code import request_result
from common.acl import acl_check
from common.parameters import parameter_check
from common.token_ucenterauth import token_auth

import cloudhost_manager
import snapshot_manager


class ComputeManagerAPI(object):

    def __init__(self):

        self.billing_check = conf.billing
        self.cloudhost_manager = cloudhost_manager.CloudHostManager()
        self.snapshot_manager = snapshot_manager.SnapShotManager()

    @acl_check('compute')
    def cloudhost_create(self, context, parameters=None):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            availzone_uuid = parameters.get('availzone_uuid')
            image_uuid = parameters.get('image_uuid')
            vm_name = parameters.get('vm_name')
            vm_cpu = parameters.get('vm_cpu')
            vm_mem = parameters.get('vm_mem')
            disk_list = parameters.get('disk_list')
            nic_list = parameters.get('nic_list')
            password = parameters.get('password')
            cost = parameters.get('cost')

            availzone_uuid = parameter_check(availzone_uuid, ptype='pstr')
            image_uuid = parameter_check(image_uuid, ptype='pstr')
            vm_name = parameter_check(vm_name, ptype='pnam')
            vm_cpu = parameter_check(vm_cpu, ptype='pint')
            vm_mem = parameter_check(vm_mem, ptype='pint')
            password = parameter_check(password, ptype='ppwd')
            if self.billing_check is True:
                cost = parameter_check(cost, ptype='pflt')
                if float(cost) < 0:
                    raise(Exception('Parameter cost error, '
                                    'cost must greater than 0'))
            else:
                cost = parameter_check(cost, ptype='pflt', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_create(
                    team_uuid, project_uuid, user_uuid,
                    availzone_uuid, image_uuid, vm_name,
                    vm_cpu, vm_mem, disk_list, nic_list,
                    password, cost, token=token,
                    source_ip=source_ip)

    @acl_check('compute')
    def cloudhost_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_list(
                    user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv)

    @acl_check('compute')
    def cloudhost_info(self, context, parameters):

        try:
            vm_uuid = context['resource_uuid']

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_info(vm_uuid)

    @acl_check('compute')
    def cloudhost_power_on(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_power_on(
                    vm_uuid, token=token, source_ip=source_ip,
                    resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_power_off(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_power_off(
                    vm_uuid, token=token, source_ip=source_ip,
                    resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_cpu_update(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_cpu = parameters.get('vm_cpu')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            vm_cpu = parameter_check(vm_cpu, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_cpu_update(
                    vm_uuid, vm_cpu, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_mem_update(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_mem = parameters.get('vm_mem')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            vm_mem = parameter_check(vm_mem, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_mem_update(
                    vm_uuid, vm_mem, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_disk_mount(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            disk_uuid = parameters.get('disk_uuid')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            disk_uuid = parameter_check(disk_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_disk_mount(
                    vm_uuid, disk_uuid, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_disk_umount(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            disk_uuid = parameters.get('disk_uuid')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            disk_uuid = parameter_check(disk_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_disk_umount(
                    vm_uuid, disk_uuid, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_nic_attach(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vnic_uuid = parameters.get('vnic_uuid')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            vnic_uuid = parameter_check(vnic_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_nic_attach(
                    vm_uuid, vnic_uuid, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_nic_unattach(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vnic_uuid = parameters.get('vnic_uuid')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            vnic_uuid = parameter_check(vnic_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_nic_unattach(
                    vm_uuid, vnic_uuid, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_floatip_bind(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            lan_ip = parameters.get('lan_ip')
            floatip = parameters.get('floatip')
            start_port = parameters.get('start_port')
            end_port = parameters.get('end_port')

            lan_ip = parameter_check(lan_ip, ptype='pnip')
            floatip = parameter_check(floatip, ptype='pnip')
            start_port = parameter_check(start_port, ptype='pint',
                                         exist='no')
            end_port = parameter_check(end_port, ptype='pint',
                                       exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_floatip_bind(
                    vm_uuid, lan_ip, floatip, start_port,
                    end_port, token=token, source_ip=source_ip,
                    resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_floatip_unbind(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_floatip_unbind(
                    vm_uuid, token=token, source_ip=source_ip,
                    resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_password_change(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            password = parameters.get('password')

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
            password = parameter_check(password, ptype='ppwd')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_password_change(
                    vm_uuid, password, token=token,
                    source_ip=source_ip, resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_delete(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_delete(
                    vm_uuid, token=token, source_ip=source_ip,
                    resource_uuid=vm_uuid)

    @acl_check('compute')
    def cloudhost_recovery(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            vm_uuid = context['resource_uuid']

            vm_uuid = parameter_check(vm_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.cloudhost_recovery(
                    vm_uuid, token=token, source_ip=source_ip,
                    resource_uuid=vm_uuid)

    @acl_check('compute')
    def snapshot_create(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            cloudhost_uuid = parameters.get('cloudhost_uuid')
            snapshot_name = parameters.get('snapshot')
            comment = parameters.get('comment')

            cloudhost_uuid = parameter_check(cloudhost_uuid, ptype='pstr')
            snapshot_name = parameter_check(snapshot_name, ptype='pnam')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.snapshot_create(
                    team_uuid, project_uuid, user_uuid,
                    cloudhost_uuid, snapshot_name, comment,
                    token=token, source_ip=source_ip,
                    resource_name=snapshot_name)

    @acl_check('compute')
    def snapshot_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            team_priv = user_info.get('team_priv')
            project_uuid = user_info.get('project_uuid')
            project_priv = user_info.get('project_priv')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.snapshot_list(
                    user_uuid, team_uuid, team_priv,
                    project_uuid, project_priv)

    @acl_check('compute')
    def snapshot_info(self, context, parameters):

        try:
            snapshot_uuid = context['resource_uuid']

            snapshot_uuid = parameter_check(snapshot_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.snapshot_info(snapshot_uuid)

    @acl_check('compute')
    def snapshot_restore(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            snapshot_uuid = context['resource_uuid']

            snapshot_uuid = parameter_check(snapshot_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.snapshot_restore(
                    snapshot_uuid, token=token,
                    source_ip=source_ip,
                    resource_uuid=snapshot_uuid)

    @acl_check('compute')
    def snapshot_delete(self, context, parameters):

        try:
            token = context['token']
            source_ip = context.get('source_ip')
            snapshot_uuid = context['resource_uuid']

            snapshot_uuid = parameter_check(snapshot_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, '
                        'parameters=%s, reason=%s'
                        % (context, parameters, e))
            return request_result(101)

        return self.cloudhost_manager.snapshot_delete(
                    snapshot_uuid, token=token,
                    source_ip=source_ip,
                    resource_uuid=snapshot_uuid)
