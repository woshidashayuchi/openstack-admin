# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/6 15:39
from openstack.network.v2.network import Network

def new_network():
    obj_network = Network()
    obj_network.name = 'lan01'
    obj_network.id = '65989d42-8827-44c7-a1ed-838321e4941a'
    print type(obj_network)
    return obj_network
