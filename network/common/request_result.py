# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:18

status_code = {
    0: 'ok',
    101: 'parameters error',
    201: 'Authentication failure',
    202: 'Operation denied',
    203: 'openstack Authentication failure',
    301: 'login exception',
    302: 'title has exist',
    401: 'mysql database insert error',
    402: 'mysql database update error',
    403: 'mysql database select error',
    404: 'mysql database delete error',
    405: 'delete forbid',
    501: 'get token error',
    598: 'rabbitmq exec error',
    601: 'volume create error',
    602: 'volume update error',
    603: 'volume delete error',
    604: 'volume delete forbid',
    605: 'volume detail select error',
    611: 'cloudhost create error',
    612: 'cloudhost update error',
    613: 'cloudhost delete error',
    621: 'keypair create error',
    622: 'keypair update error',
    623: 'keypair select error',
    624: 'keypair delete error',
    631: 'add floating ip to server error',
    632: 'remove floating from server error',
    701: 'system error',
    901: 'volume type create error',
    902: 'volume type update error',
    903: 'volume type delete error',
    999: 'system error',
    904: 'volume type select error',
    1001: 'snapshot create error',
    1002: 'snapshot update error',
    1003: 'snapshot delete error',
    1004: 'snapshot select error',
    1010: 'attachment create error',
    1011: 'attachment update error',
    1012: 'attachment delete error',
    1013: 'attachment select error',
    1020: 'network create error',
    1021: 'network update error',
    1022: 'network delete error',
    1023: 'network select error',
    1024: 'network unable use',
    1025: 'network add to vm error',
    1026: 'network remove from vm error',
    1030: 'subnet create error',
    1031: 'subnet update error',
    1032: 'subnet delete error',
    1033: 'subnet select error',
    1041: 'router create error',
    1042: 'router update error',
    1043: 'router delete error',
    1044: 'router select error',
    1051: 'floating ip create error',
    1052: 'floating ip update error',
    1053: 'floating ip delete error',
    1054: 'floating ip select error',
    1055: 'floating ip find error',
    1056: 'floating ip bind error',
    1057: 'floating ip unbind error',
    1058: 'floating ip using',
    1059: 'floating ip unable to use',
    1061: 'port create error',
    1062: 'port delete error',
    1063: 'port update error',
    1064: 'port select error',
    1065: 'port has be used',
    1081: 'add interface to vm error',
    1082: 'remove interface from vm error'
}


def request_result(code, ret={}):
    result = {
        "status": code,
        "msg": status_code[code],
        "result": ret
    }
    return result
