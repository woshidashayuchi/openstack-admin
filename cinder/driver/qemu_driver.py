# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/5/18 16:04
from common import conf
from common.ssh import exec_cmd


class QemuDriver(object):
    def __init__(self):
        self.vms_pool = conf.vms_pool
        self.volume_pool = conf.volume_pool

    def os_snap_create(self, vm_uuid, snap_name):
        statement = "qemu-img snapshot -c %s rbd:%s/%s_disk" % (
                    snap_name,
                    self.vms_pool,
                    vm_uuid)

        exec_cmd(statement)

    def os_snap_detail(self, vm_uuid):
        statement = "qemu-img snapshot -l rbd:%s/%s_disk" % (
                    self.vms_pool,
                    vm_uuid
        )
        return exec_cmd(statement)

    def os_snap_delete(self, snap_name, vm_uuid):
        statement = "qemu-img snapshot -d %s rbd:%s/%s_disk" % (
                    snap_name,
                    self.vms_pool,
                    vm_uuid
        )
        exec_cmd(statement)

    def os_snap_revert(self, snap_name, vm_uuid):
        statement = "qemu-img snapshot -a %s rbd:%s/%s_disk" % (
            snap_name,
            self.vms_pool,
            vm_uuid
        )
        exec_cmd(statement)

    def snap_revert(self, snapshot_uuid, volume_uuid):
        statement = "qemu-img snapshot -a %s rbd:%s/volume-%s" % (
            'snapshot-' + snapshot_uuid,
            self.volume_pool,
            volume_uuid
        )
        exec_cmd(statement)
