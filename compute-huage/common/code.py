# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com.com>

# v1.0状态码说明
# 程序执行状态码定义,分类说明如下：
# 0      OK 只有返回码为0才有result值。
# 1xx    API接口自身错误，如参数错误、接口已停用、找不到接口。
# 2xx    认证或权限错误
# 3xx    逻辑错误，如名称冲突，资源超过限额等。
# 4xx    数据库错误
# 5xx    驱动层错误
# 6xx    系统级别错误


status_code = {
    0:   "OK",
    101: "Parameters error",
    102: "RPC API routing error",
    103: "Http requests error",
    201: "Authentication failure",
    202: "Operation denied",
    301: "Resource name already exists",
    302: "Balance not enough",
    303: "Limit denied",
    401: "Database insert failure",
    402: "Database delete failure",
    403: "Database update failure",
    404: "Database select failure",
    501: "Driver execute failure",
    502: "Openstack execute failure",
    999: "System error",

    611: 'cloudhost create error',
    612: 'cloudhost update error',
    613: 'cloudhost delete error',
    631: 'add floating ip to server error',
    632: 'remove floating from server error'
}


def request_result(code, ret={}):

    result = {
                 "status": code,
                 "msg": status_code.get(code),
                 "result": ret
             }

    return result
