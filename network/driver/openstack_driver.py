# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:47
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
from common.connect import connection
from common.logs import logging as log
from common.request_result import request_result


class OpenstackDriver(object):
    def __init__(self):
        self.conn = connection()

    def network_create(self, name, description, is_admin_state_up=True,
                       is_shared=False):
        if self.conn is False:
            return request_result(701)

        try:
            op_result = self.conn.network.\
                create_network(name=name,
                               description=description,
                               is_admin_state_up=is_admin_state_up,
                               shared=is_shared
                               )
        except Exception, e:
            log.error('create the network(op) error, reason is: %s' % e)
            return request_result(1020)

        return request_result(200, op_result.id)

    def subnet_create(self, name, description, is_dhcp_enabled, network_id,
                      ip_version, gateway_ip, allocation_pools, cidr,
                      dns_nameservers=[], host_routes=[]):
        """

        :param name: 子网名称(string)eg：'test_subnet'
        :param description: 子网描述(string)
        :param is_dhcp_enabled: 是否激活dhcp(bool)eg: True
        :param network_id: 关联网络的id(string)
        :param ip_version: ip版本(int)(4/6)
        :param gateway_ip: 网关(String)eg:'172.2.0.1'
        :param allocation_pools: 分配地址池（list）eg:[{'start':'','end':''}]
        :param cidr: 网络地址(string)eg:172.20.2.0/24
        :param dns_nameservers: dns服务器(list)
        :param host_routes: 主机路由(list)
        :return:
        """
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.\
                create_subnet(name=name,
                              description=description,
                              is_dhcp_enabled=is_dhcp_enabled,
                              network_id=network_id,
                              ip_version=ip_version,
                              gateway_ip=gateway_ip,
                              allocation_pools=allocation_pools,
                              cidr=cidr,
                              dns_nameservers=dns_nameservers,
                              host_routes=host_routes)
        except Exception, e:
            log.error('create the subnet(op) error, reason is: %s' % e)
            return request_result(1030)

        return request_result(200, op_result)

    def network_get(self):
        if self.conn is False:
            return request_result(701)

        try:
            op_result = self.conn.network.get_subnet('testsubnet')
        except Exception, e:
            log.error('query the network message error, reason is: %s' % e)
            return request_result(1023)
        return request_result(200, op_result)


# test code
if __name__ == '__main__':
    op = OpenstackDriver()
    # 创建一个网络
    # print op.network_create(name='test111',
    #                         description='it is a test')
    # 创建子网并关联网络
    print op.subnet_create(name='for_test111',
                           description='happy test subnet',
                           is_dhcp_enabled=True,
                           network_id='3d763519-e1d9-4e9b-97c1-9ea6226c1184',
                           ip_version=4,
                           gateway_ip='172.20.2.2',
                           allocation_pools=[{'start': '172.20.2.100',
                                              'end': '172.20.2.105'}],
                           cidr='172.20.2.0/24',
                           dns_nameservers=[],
                           host_routes=[])
    # print op.network_get()
