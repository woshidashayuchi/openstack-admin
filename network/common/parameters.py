# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>
from __future__ import unicode_literals
import sys
import re
from common.logs import logging as log
from netaddr import *

def rpc_data(api, context, parameters=None):

    return {'api': api,
            'context': context,
            'parameters': parameters}


def context_data(token=None, resource_uuid=None,
                 action=None, source_ip=None):

    return {
               "token": token,
               "resource_uuid": resource_uuid,
               "action": action,
               "source_ip": source_ip
           }


def parameter_check(parameter, ptype='pstr', exist='yes'):

    if (parameter is None) and (exist == 'no'):
        return parameter
    if (parameter is None) and (exist == 'yes'):
        raise(Exception('Parameter is not allow to be None'))
    if ptype == 'ncid':
        IPNetwork(parameter)
        return parameter
    if exist == 'not_essential':
        if parameter is None:
            return parameter
        else:
            if ptype == 'ndes':
                return parameter
    para_format = {
        "pstr": "[A-Za-z0-9-_]{1,60}$",
        "pnam": "[A-Za-z]{1}[A-Za-z0-9-_]{4,19}$",  # name
        "psiz": "[1-9]\d*",  # size

        "psnm": "[A-Za-z]{1}[A-Za-z0-9-_]{2,19}$",
        "pint": "-{0,1}[0-9]{1,24}$",
        "pflt": "-{0,1}[0-9]{1,15}[.]{0,1}[0-9]{0,6}$",
        "peml": ("[A-Za-z1-9]{1,1}[A-Za-z0-9-_]{2,30}"
                 "@[A-Za-z0-9]{1,1}[A-Za-z0-9-_.]{1,20}"
                 "[.]{1,1}[A-Za-z]{1,5}$"),
        "puid": ("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-"
                 "[a-z0-9]{4}-[a-z0-9]{12}$"),
        "pver": "[A-Za-z]{1}[A-Za-z0-9-_.]{2,19}$",
        "pdat": "20{1}[0-9]{2}.[0-9]{2}.[0-9]{2}$",
        "pnip": "[1-9]{1}[0-9]{0,2}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$",
        "pdsk": "/dev/[s|v]{1}d[a-z]{1}[0-9]{1,2}$",
        "pmac": ("[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:"
                 "[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}$"),
        "ppwd": ".{6,60}",

        "nname": "[A-Za-z]{1}[A-Za-z0-9-_]{3,19}$",
        "n01": "^[01]$",
        "n04": "^[46]$",
        "nnum": "^\+?[1-9][0-9]*$",
        "nip": "((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]"
               "|2[0-4]\d|((1\d{2})|([1-9]?\d)))",
    }

    m = re.match(para_format[ptype], str(parameter))
    if m is None:
        log.warning('Parameter format error, parameter=%s, ptype=%s, exist=%s'
                    % (str(parameter), ptype, exist))
        raise(Exception('Parameter format error'))

    return parameter


def allocation_pools_conform(allocation_pools):
    """
    :param allocation_pools: "172.20.2.1,172.20.20.x;172.20..."
    :return:
    """
    result = []
    if allocation_pools is not None and allocation_pools != "":
        for allocation in [pool for pool in allocation_pools.split(';')]:
            result.append({'start': allocation.split(',')[0],
                           'end': allocation.split(',')[1]})

    return result

def dns_nameservers_conform(dns_nameservers):
    # 源数据格式 x.x.x.x,y.y.y.y
    result = []
    if dns_nameservers is not None:
        for dns_server in dns_nameservers.split(','):
            result.append(dns_server)

    return result

def gateway_ip_create(cidr):
    f = cidr.split('/')[0].split('.')
    gateway_ip = f[0]+'.'+f[1]+'.'+f[2]+'.'+'1'
    return gateway_ip
    


if __name__ == "__main__":

    parameter = sys.argv[1]
    ptype = sys.argv[2]
    exist = sys.argv[3]

    try:
        parameter = parameter_check(parameter, ptype, exist)
        print('parameter check success, parameter=%s' % parameter)
    except Exception, e:
        print('parameter error, reason=%s' % e)
