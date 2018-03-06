# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:18

status_code = {
    200: 'ok',
    101: 'parameters error',
    301: 'login exception',
    302: 'title has exist',
    401: 'mysql database insert error',
    402: 'mysql database update error',
    403: 'mysql database select error',
    404: 'mysql database delete error',
    501: 'get token error',
    601: 'volume create error',
    602: 'volume update error',
    603: 'volume delete error',
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
    801: 'username or password error',
    901: 'volume type create error',
    902: 'volume type update error',
    903: 'volume type delete error',
    904: 'volume type select error',
    1001: 'snapshot create error',
    1002: 'snapshot update error',
    1003: 'snapshot delete error',
    1004: 'snapshot select error'
}


def request_result(code, ret={}):
    result = {
        "status": code,
        "msg": status_code[code],
        "result": ret
    }
    return result
