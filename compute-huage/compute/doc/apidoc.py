# -*- coding:utf8 -*-
# Date:2017-07-31
# Author: YanHua


"""
@apiDefine CODE_DELETE_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {}
}
"""


"""
@apiDefine CODE_CLOUDHOST_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "vm_uuid": "string",
        "vm_name": "string",
        "vm_cpu": "string",
        "vm_mem": "string",
        "availzone_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_CLOUDHOST_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "cloudhost_list": [
            {
                "vm_uuid": "string",
                "vm_name": "string",
                "image_name": "string",
                "vm_ip": list,
                "floatip": "string",
                "vm_cpu": int,
                "vm_mem": int,
                "availzone_uuid": "string",
                "availzone_name": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                ......
            },
            {
                ......
            }
        ]
    }
}
"""


"""
@apiDefine CODE_CLOUDHOST_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "vm_uuid": "string",
        "vm_name": "string",
        "image_name": "string",
        "vm_ip": list,
        "floatip": "string",
        "vm_cpu": int,
        "vm_mem": int,
        "vm_disk": list,
        "vm_nic": list,
        "availzone_uuid": "string",
        "login_way": "keys/password",
        "keys_name": "string",
        "status": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_CLOUDHOST_RECOVERY_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "vm_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_CLOUDHOST_PUT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "vm_uuid": "string",
        "vm_cpu": int,
        "vm_mem": int,
        "vm_disk": list,
        "vm_nic": list
    }
}
"""


"""
@apiDefine CODE_SNAPSHOT_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "snapshot_uuid": "string",
        "snapshot_name": "string",
        "vm_uuid": "string",
        "vm_name": "string",
        "availzone_uuid": "string"
    }
}
"""


"""
@apiDefine CODE_SNAPSHOT_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "count": int,
        "snapshot_list": [
            {
                "snapshot_uuid": "string",
                "snapshot_name": "string",
                "vm_uuid": "string",
                "vm_name": "string",
                "status": "string",
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            },
            {
                ......
            },
            {
                ......
            }
        ]
    }
}
"""


"""
@apiDefine CODE_SNAPSHOT_INFO_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "snapshot_uuid": "string",
        "snapshot_name": "string",
        "vm_uuid": "string",
        "vm_name": "string",
        "availzone_uuid": "string",
        "status": "string",
        "comment": "string",
        "create_time": "YYYY-MM-DD HH:MM:SS",
        "update_time": "YYYY-MM-DD HH:MM:SS"
    }
}
"""


"""
@apiDefine CODE_SNAPSHOT_REVERT_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "snapshot_uuid": "string",
        "snapshot_name": "string",
        "vm_uuid": "string",
        "vm_name": "string",
        "availzone_uuid": "string"
    }
}
"""


###################################################################
#                       计算服务接口定义                          #
###################################################################


"""
@api {post} /api/v1.0/compute/cloudhosts 1.1 云主机创建
@apiName cloudhost create
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 用户创建云主机
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "availzone_uuid": "string",
    "image_uuid": "string",
    "vm_name": "string",
    "vm_cpu": int,
    "vm_mem": int,
    "disk_list": list,     # 示例：[{"disk_type": "ssd/hdd", "disk_size": int}]
    "nic_list": list,      # 示例: [vswitch01_uuid, vswitch02_uuid]
    "login_way": "keys/password",
    "keys_name": "string",
    "password": "string",
    "create_num": int,
    "cost": float
}
@apiUse CODE_CLOUDHOST_POST_0
"""


"""
@api {get} /api/v1.0/compute/cloudhosts?page_size=<int>&page_num=<int> 1.2 云主机列表
@apiName cloudhost list
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 用户可用云主机列表查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLOUDHOST_LIST_0
"""


"""
@api {get} /api/v1.0/compute/cloudhosts/<cloudhost_uuid> 1.3 云主机信息
@apiName cloudhost info
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机详细信息查询
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLOUDHOST_INFO_0
"""


"""
@api {delete} /api/v1.0/compute/cloudhosts/<cloudhost_uuid> 1.4 云主机删除
@apiName cloudhost delete
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 逻辑删除云主机并放入回收站中
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<recovery> 1.5.1.1 云主机恢复
@apiName recovery cloudhost
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 恢复回收站中的云主机
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLOUDHOST_RECOVERY_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<power_on> 1.5.2.1 云主机开机
@apiName cloudhost power on
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机开机
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<power_off> 1.5.2.2 云主机关机
@apiName cloudhost power off
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机关机
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<cpu> 1.5.3.1 云主机CPU调整
@apiName cloudhost cpu update
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机CPU调整
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "vm_cpu": int
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<mem> 1.5.4.1 云主机内存调整
@apiName cloudhost mem update
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机内存调整
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "vm_mem": int
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<disk_mount> 1.5.5.1 云主机磁盘挂载
@apiName cloudhost mount disk
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机挂载磁盘
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "disk_uuid": "string"
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<disk_umount> 1.5.5.2 云主机磁盘卸载
@apiName cloudhost umount disk
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机卸载磁盘
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "disk_uuid": "string"
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<nic_attach> 1.5.6.1 云主机网卡连接
@apiName cloudhost attach nic
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机连接网卡
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "nic_uuid": "string"
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<nic_unattach> 1.5.6.2 云主机网卡卸载
@apiName cloudhost unattach nic
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机卸载网卡
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "nic_uuid": "string"
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<floatip_bind> 1.5.7.1 云主机弹性IP绑定
@apiName cloudhost bind floatip
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机绑定弹性IP
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "floatip": "string",
    "lan_ip": "string",
    "start_port": int,
    "end_port": int
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<floatip_unbind> 1.5.7.2 云主机弹性IP解绑
@apiName cloudhost unbind floatip
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 云主机解绑弹性IP
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "floatip": "string"
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {put} /api/v1.0/compute/cloudhosts/<cloudhost_uuid>?update=<password_change> 1.5.8.1 云主机密码修改
@apiName cloudhost change login password
@apiGroup 1 cloudhost
@apiVersion 1.0.0
@apiDescription 修改云主机登录密码
@apiPermission user and organization
@apiParam {json} header {"token": "string"} 
@apiParam {json} body
@apiParamExample body
{
    "password": "string"
}
@apiUse CODE_CLOUDHOST_PUT_0
"""


"""
@api {post} /api/v1.0/compute/snapshots 2.1 快照创建
@apiName snapshot create
@apiGroup 2 snapshots
@apiVersion 1.0.0
@apiDescription 创建实例快照
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "snapshot_name": "string",
    "cloudhost_uuid": "string",
    "comment": "string"
}
@apiUse CODE_SNAPSHOT_POST_0
"""


"""
@api {get} /api/v1.0/compute/snapshots?&page_size=<int>&page_num=<int> 2.2 快照列表
@apiName snapshot list
@apiGroup 2 snapshots
@apiVersion 1.0.0
@apiDescription 查看快照列表
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_SNAPSHOT_LIST_0
"""


"""
@api {get} /api/v1.0/compute/snapshots/<snapshot_uuid> 2.3 快照信息
@apiName snapshot info
@apiGroup 2 snapshots
@apiVersion 1.0.0
@apiDescription 查看快照详细信息
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_SNAPSHOT_INFO_0
"""


"""
@api {put} /api/v1.0/compute/snapshots/<snapshot_uuid> 2.4 快照恢复
@apiName snapshot revert
@apiGroup 2 snapshots
@apiVersion 1.0.0
@apiDescription 将实例恢复到快照状态
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_SNAPSHOT_REVERT_0
"""


"""
@api {delete} /api/v1.0/compute/snapshots/<snapshot_uuid> 2.5 快照删除
@apiName snapshot delete
@apiGroup 2 snapshots
@apiVersion 1.0.0
@apiDescription 快照删除
@apiPermission user and organization
@apiParam {json} header {"token": "string"}
@apiUse CODE_DELETE_0
"""
