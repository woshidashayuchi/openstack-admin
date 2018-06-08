# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/21 10:16
"""
this is the network api doc
"""
"""
@apiDefine CODE_NET_POST_1
@apiSuccessExample 返回
{ "resource_uuid": "string",
  "name": "string",
  "description": "string",
  "is_admin_state_up": "string",
  'is_shared': int
  }
"""
"""
@apiDefine CODE_NET_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":{
        "resource_uuid": network_uuid
        }
}
"""
"""
@apiDefine CODE_NET_DETAIL_0
@apiSuccessExample 返回
 {
    "msg": "ok",
    "result": {
        "description": "string",               # 描述
        "is_admin_state_up": int,              # 是否启用管理员状态（1:启用，0:不启用）
        "is_router_external": int,             # 外部是否可以访问
        "is_shared": int,                      # 是否共享
        "name": "string",                      # 网络名称
        "status": "string",                    # 网络状态
        "subnet_name_and_cidr": "string",      # 已连接的子网信息（"名称 CIDR"）
        "create_time": "YYYY-MM-DD HH:MM:SS",  # 创建时间
        "update_time": "YYYY-MM-DD HH:MM:SS"   # 最新更新时间
    },
    "status": 0
}
"""
"""
@apiDefine CODE_NET_LIST_0
@apiSuccessExample 返回
{
    "msg": "ok",
    "result": {
        "count": int,
        "network_list":[
        {
            "description": "string",
            "is_admin_state_up": int,  
            "is_router_external": int,
            "is_shared": int,
            "name": "string",
            "network_uuid": "string",
            "status": "string",
            "subnet_name_and_cidr": "string"
            "create_time": "YYYY-MM-DD HH:MM:SS",
            "update_time": "YYYY-MM-DD HH:MM:SS"
        }
        
        {
            ······
        }
        {
            ······
        }
    ],
    "status": 0
}
"""
"""
@apiDefine CODE_ROUTER_POST_1
@apiSuccessExample 返回
{ "resource_uuid": "string",
  "name": "string",
  "description": "string",
  "is_admin_state_up": int
  }
"""
"""
@apiDefine CODE_ROUTER_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":{
        "router_uuid": "string"
    }
}
"""
"""
@apiDefine CODE_ROUTER_LIST_0
@apiSuccessExample 返回
{
    "msg": "ok",
    
    "result": {
        "count": int,
        "network_list": [
        {
            
            "description": "string",
            "name": "string",
            "router_uuid": "string",
            "status": "string"
            "create_time": "YYYY-MM-DD HH:MM:SS",
            "update_time": "YYYY-MM-DD HH:MM:SS"
        },
        {
            ···
        },
        {
            ···
        }
    ],
    "status": 0
}
"""
"""
@apiDefine CODE_ROUTER_DETAIL_0
@apiSuccessExample 返回
{
    "msg": "ok",
    "result": {
        "description": "string",                 # 路由描述
        "external_gateway_info": "string",       # gateway连接的网络id
        "is_admin_state_up": int,                # 管理员状态
        "name": "string",                        # 路由名字
        "router_uuid": "string",                 # 路由id
        "status": "string"                       # 路由状态
        "create_time": "YYYY-MM-DD HH:MM:SS",    # 创建时间
        "update_time": "YYYY-MM-DD HH:MM:SS"     # 更新时间
    },
    "status": 0
}
"""
"""
@apiDefine CODE_FLOAT_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":{
        "resource_uuid": "string",
        "name": "string",
        "description": "string",
        "router_uuid": "string",
        "fixed_ip_address": "string",
        "floating_ip_address": "string",
        "revision_number": int,
        "port_id": "string"
    }
"""
"""
@apiDefine CODE_FLOAT_DETAIL_0
@apiSuccessExample 返回
{
    "msg": "ok",
    "result":
        {
            "description": "string",                 # 弹性ip描述
            "fixed_ip_address": "string",            # 弹性ip关联的固定ip地址
            "floating_ip_address": "string",         # 弹性ip地址
            "floatingip_uuid": "string",             # 弹性ip的id
            "name": "string",                        # 弹性ip名称
            "port_id": "string",                     # 绑定port的id
            "revision_number": int,                  # 版本
            "router_uuid": "string",                 # 绑定路由id
            "create_time": "YYYY-MM-DD HH:MM:SS",    # 创建时间
            "update_time": "YYYY-MM-DD HH:MM:SS"     # 更新时间
        }
    "status": 0
}
"""
"""
@apiDefine CODE_FLOAT_LIST_0
@apiSuccessExample 返回
{
    "msg": "ok",
    "result": {
        "count": int,
        "floatingip_list":[
        {
            "description": "string",
            "fixed_ip_address": "string",
            "floating_ip_address": "string",
            "floatingip_uuid": "string",
            "name": "string",
            "port_id": "string",
            "revision_number": int,
            "router_uuid": "string",
            "create_time": "YYYY-MM-DD HH:MM:SS",
            "update_time": "YYYY-MM-DD HH:MM:SS"    
        }
        {
            ···
        }
    ],
    "status": 0
}
"""
"""
@apiDefine CODE_PORT_POST_0
@apiSuccessExample 返回
{
    "msg": "ok",
    "result": {
        "resource_uuid": "string"  # port_uuid
    },
    "status": 0
}
"""
"""
@apiDefine CODE_PORT_LIST_0
@apiSuccessExample 返回
{
    "msg": "ok",
    "result": {
         "count": int
         "ports_list": [
            {
                "name": "string",
                "description": "string",
                "ip_address": "string",
                "mac_address": "string",
                "port_uuid": "string",
                "vm_uuid": "string",
                "status": "string",   # in-use or available
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
            {
                ···
            }
            {
                ···
            }
        ],
        "status": 0
}
"""
"""
@apiDefine CODE_PORT_LIST_1
@apiSuccessExample 返回
{
    "msg": "ok",
    "result": {
         "count": int
         "ports_list": [
            {
                "name": "string",
                "description": "string",
                "ip_address": "string",
                "mac_address": "string",
                "port_uuid": "string",
                "network_uuid": "string",
                "vm_uuid": "string",
                "status": "string",   # in-use or available
                "create_time": "YYYY-MM-DD HH:MM:SS",
                "update_time": "YYYY-MM-DD HH:MM:SS"
            }
            {
                ···
            }
            {
                ···
            }
        ],
        "status": 0
}
"""
"""
@api {post} /api/v1.0/network/networks 1.1 创建网络
@apiName create
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
     "name":"string",              # 网络名称，若同时选择创建子网，子网与名称相同
     "description": "string",      # 网络描述 
     "is_admin_state_up":int,      # 管理员状态
     "is_shared": int              # 是否外部共享
}
@apiUse CODE_NET_POST_1
"""
"""
@api {post} /api/v1.0/network/networks 1.2 带子网部分创建网络
@apiName create_and_subnet
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
     "name":"string",                  # 网络名称，若同时选择创建子网，子网与名称相同
     "description": "string",          # 网络描述 
     "is_admin_state_up": int,         # 管理员状态
     "is_shared": int                  # 是否外部共享
     "is_dhcp_enabled": int,           # 是否激活dhcp
     "ip_version": int,                # ip地址版本，4（可选）
     "gateway_ip":"string",            # 网关（可选） 
     "cidr":"string"                   # CIDR 
}
@apiUse CODE_NET_POST_1
"""
"""
@api {post} /api/v1.0/network/subnets 1.3 单独创建子网
@apiName create_subnet_only
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
     "name":"strng",                 # 子网名称
     "description":"string",         # 子网描述
     "is_dhcp_enabled":int,          # 是否开启dhcp
     "network_uuid":"string",        # 关联网络id
     "ip_version":int,               # 版本
     "gateway_ip":"string",          # 网关
     "cidr":"string"                 # cidr
}
@apiUse CODE_NET_POST_0
"""
"""
@api {get} /api/v1.0/network/networks?page_num=a&page_size=b 1.4 网络列表
@apiName network_list
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_NET_LIST_0
"""
"""
@api {get} /api/v1.0/network/networks/<network_uuid> 1.5 网络详情
@apiName network_detail
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_NET_DETAIL_0
"""
"""
@api {put} /api/v1.0/network/networks/<network_uuid> 1.6 网络更新
@apiName update_network
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
{
    "name": "string"               # 名称
    "is_admin_state_up": int       # 是否启用管理员状态
}
@apiUse CODE_NET_POST_0
"""
"""
@api {delete} /api/v1.0/network/networks/<network_uuid> 1.7 网络删除
@apiName delete_network
@apiGroup network
@apiVersion 1.0.0
@apiDescription 网络
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_NET_POST_0
"""
"""
@api {post} /api/v1.0/network/routers 2.1 创建路由
@apiName create_router
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "name":"string",                # 名称
    "description": "string",        # 路由描述
    "is_admin_state_up": int        # 是否启动管理员状态
}
@apiUse CODE_ROUTER_POST_1
"""
"""
@api {get} /api/v1.0/network/routers?page_num=<int>&page_size=<int> 2.2 路由列表
@apiName router_list
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_ROUTER_LIST_0
"""
"""
@api {get} /api/v1.0/network/routers/<router_uuid> 2.3 路由详情
@apiName router_detail
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_ROUTER_DETAIL_0
"""
"""
@api {delete} /api/v1.0/network/routers/<router_uuid> 2.4 删除路由
@apiName router_delete
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_ROUTER_POST_0
"""
"""
@api {put} /api/v1.0/network/routers/<router_uuid>？up_type=name 2.5 更新名称
@apiName router_name_update
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParamExample body
{
    "name":"string"
}
@apiUse CODE_ROUTER_POST_0
"""
"""
@api {put} /api/v1.0/network/routers/<router_uuid>？up_type=is_admin_state_up 2.6 更新管理员状态
@apiName router_isadminstatus_update
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParamExample body
{
    "is_admin_state_up":0/1
}
@apiUse CODE_ROUTER_POST_0
"""
"""
@api {put} /api/v1.0/network/routers/<router_uuid>？up_type=interface 2.7 更新接口
@apiName router_interface
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParamExample body
{
    "rtype":"add",  # 可为add/remove
    "subnet_uuid":"87b09620-c5e8-4a22-baf0-6ad23a643038",
    "ip_address":"172.20.2.3"  # 该格式为指定格式，也可不传该参数
}
@apiUse CODE_ROUTER_POST_0
"""
"""
@api {put} /api/v1.0/network/routers/<router_uuid>？up_type=gateway 2.8 更新gateway
@apiName router_gateway
@apiGroup router
@apiVersion 1.0.0
@apiDescription 路由
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParamExample body
{
    "network_uuid": network_uuid # 去除网关时，network_uuid为""
}
@apiUse CODE_ROUTER_POST_0
"""
"""
@api {post} /api/v1.0/network/floatingips 3.1 申请弹性ip
@apiName create_floatingip
@apiGroup floatingip
@apiVersion 1.0.0
@apiDescription 浮动ip
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
"network_id": "string"       # 外网ip
}
@apiUse CODE_FLOAT_POST_0
"""

"""
@api {get} /api/v1.0/network/floatingips?page_num=a&page_size=b 3.2 弹性ip列表
@apiName floatingip_list
@apiGroup floatingip
@apiVersion 1.0.0
@apiDescription 浮动ip
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_FLOAT_LIST_0
"""
"""
@api {get} /api/v1.0/network/floatingapis/<floatingip_uuid> 3.3 弹性ip详情
@apiName floatingip_detail
@apiGroup floatingip
@apiVersion 1.0.0
@apiDescription 浮动ip
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_FLOAT_DETAIL_0
"""
"""
@api {delete} /api/v1.0/network/floatingapis/<floatingip_uuid> 3.4 释放弹性ip
@apiName floatingip_delete
@apiGroup floatingip
@apiVersion 1.0.0
@apiDescription 浮动ip
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_FLOAT_POST_0
"""
"""
@api {post} /api/v1.0/network/ports 4.1 创建port
@apiName port_create
@apiGroup port
@apiVersion 1.0.0
@apiDescription 端口（即基于network创建的固定ip）
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
 "network_uuid":"string",  # 基于网络的uuid
 "name":"string",          # port名称
 "description":"string"    # port描述
 }
@apiUse CODE_PORT_POST_0
"""
"""
@api {get} /api/v1.0/network/ports?network_uuid=<string>&page_num=<int>&page_size=<int> 4.2 port列表
@apiName ports_list_network
@apiGroup port
@apiVersion 1.0.0
@apiDescription port列表(某网络)
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_PORT_LIST_0
"""
"""
@api {get} /api/v1.0/network/ports?page_num=<int>&page_size=<int> 4.3 port列表
@apiName ports_list
@apiGroup port
@apiVersion 1.0.0
@apiDescription port列表(全部)
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_PORT_LIST_1
"""
"""
@api {delete} /api/v1.0/network/ports/<port_uuid> 4.4 删除port
@apiName port_delete
@apiGroup port
@apiVersion 1.0.0
@apiDescription 删除port
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiUse CODE_PORT_POST_0
"""
