# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:47
# import sys
# path1 = sys.path[0] + '/..'
# path2 = sys.path[0] + '/../..'
# sys.path.append(path1)
# sys.path.append(path2)
from common.connect import connection
from common.logs import logging as log
from common.request_result import request_result
import json
import requests
from common import conf


class OpenstackDriver(object):
    def __init__(self):
        self.conn = connection()
        self.op_user = conf.op_user
        self.op_pass = conf.op_pass

    @staticmethod
    def get_token(user_name, password):
        header = {"Content-Type": "application/json",
                  "Accept": "application/json"}
        user_msg = {"auth": {"tenantName": "demo",
                             "passwordCredentials": {"username": user_name,
                                                     "password": password}}}
        try:
            ret = requests.post(url=conf.token_url, json=user_msg,
                                headers=header,
                                timeout=5)
        except Exception, e:
            log.error('get the token error, reason is: %s' % e)
            return request_result(501)
        if ret.status_code != 200:
            return request_result(501)
        log.debug('get the projectID and token(op) result is: %s' % ret.text)
        try:
            token = json.loads(ret.text).get('access').get('token').get('id')
            user_uuid = json.loads(ret.text).get('access').get('user').get(
                'id')
        except Exception, e:
            log.error('get the token from openstack error, reason is: %s' % e)
            return request_result(203)

        result = {'token': token, 'user_uuid': user_uuid}
        return request_result(200, result)

    def network_create(self, name, description, is_admin_state_up=True,
                       is_shared=False):
        """

        :param name: 名称
        :param description: 描述
        :param is_admin_state_up: 是否管理员状态1/0
        :param is_shared: 是否外部共享
        :return:
        """
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
                      dns_nameservers, host_routes):
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

    def network_delete(self, network_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.\
                delete_network(network_uuid)
        except Exception, e:
            log.error('delete the network(db) error, reason is: %s' % e)
            return request_result(1022)
        if op_result is not None:
            return request_result(1022)

        return request_result(200, op_result)

    def network_update(self, up_dict):
        """
        :param up_dict: eg:{'network_uuid':network_uuid, 'name':name,
                            'is_admin_state_up':1/0}
        :return:
        """
        op_token = self.get_token(self.op_user,
                                  self.op_pass)
        if op_token.get('status') != 200:
            return op_token
        token = op_token.get('result').get('token')
        net_url = conf.net_url + up_dict['network_uuid']
        parameters_dict = {
            "network": {
                "name": up_dict['name']
                # "dns_domain": "my-domain.org.",
                # "name": "",
                #  "qos_policy_id": "6a8454ade8b2e",
                #  "mtu": 1300
            }
        }
        headers = {"X-Auth-Token": token}
        try:
            op_result = requests.put(url=net_url,
                                     json=parameters_dict,
                                     headers=headers,
                                     timeout=10)
        except Exception, e:
            log.error('update the network(op) error, reason is: %s' % e)
            return request_result(1021)
        if op_result.status_code != 200:
            log.error('update the network(op) error, '
                      'the op_result is: %s' % op_result)
            return request_result(1021)

        return request_result(200, {'resource_uuid':
                                    up_dict.get('network_uuid')})

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
    # print op.subnet_create(name='for_test111',
    #                        description='happy test subnet',
    #                        is_dhcp_enabled=True,
    #                        network_id='3d763519-e1d9-4e9b-97c1-9ea6226c1184',
    #                        ip_version=4,
    #                        gateway_ip='172.20.2.2',
    #                        allocation_pools=[{'start': '172.20.2.100',
    #                                           'end': '172.20.2.105'}],
    #                        cidr='172.20.2.0/24',
    #                        dns_nameservers=[],
    #                        host_routes=[])
    print op.network_get()
    # print op.network_delete('d4ca9465-62bc-4d4d-9296-c93c821aa7bf')
