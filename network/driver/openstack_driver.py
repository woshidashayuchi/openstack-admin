# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:47
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
reload(sys)
sys.setdefaultencoding('utf-8')
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
        user_msg = {"auth": {"tenantName": conf.tenantName,
                             "passwordCredentials": {"username": user_name,
                                                     "password": password}}}
        try:
            ret = requests.post(url=conf.token_url, json=user_msg,
                                headers=header,
                                timeout=15)
        except Exception, e:
            log.error('get the token error, reason is: %s' % e)
            return request_result(501)
        if ret.status_code != 200:
            log.error('get the token error, get token result is: %s' % ret)
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
        return request_result(0, result)

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

        return request_result(0, op_result.id)

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

        return request_result(0, op_result)

    def subnet_delete(self, subnet_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.delete_subnet(subnet_uuid)
        except Exception, e:
            log.error('delete the subnet error, reason is: %s' % e)
            return request_result(1032)
        if op_result is not None:
            return request_result(1032)
        return request_result(0, {'resource_uuid': subnet_uuid})

    def network_delete(self, network_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.\
                delete_network(network_uuid)
        except Exception, e:
            log.error('delete the network(op) error, reason is: %s' % e)
            return request_result(1022)
        if op_result is not None:
            return request_result(1022)

        return request_result(0, op_result)

    def network_update(self, up_dict):
        """
        :param up_dict: eg:{'network_uuid':network_uuid, 'name':name,
                            'is_admin_state_up':1/0}
        :return:
        """
        op_token = self.get_token(self.op_user,
                                  self.op_pass)
        if op_token.get('status') != 0:
            return op_token
        token = op_token.get('result').get('token')
        net_url = conf.net_url + 'networks/' + up_dict['network_uuid']
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

        return request_result(
               0, {'resource_uuid': up_dict.get('network_uuid')}
               )

    def network_get(self):
        if self.conn is False:
            return request_result(701)

        try:
            op_result = self.conn.network.get_subnet('testsubnet')
        except Exception, e:
            log.error('query the network message error, reason is: %s' % e)
            return request_result(1023)
        return request_result(0, op_result)

    def subnet_delete(self, subnet_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.delete_subnet(subnet_uuid)
        except Exception, e:
            log.error('delete the subnet error, reason is: %s' % e)
            return request_result(1032)

        return request_result(0, op_result)

    def router_create(self, name, description, is_admin_state_up):
        if self.conn is False:
            return request_result(701)

        try:
            op_result = self.conn.network.create_router(
                            name=name,
                            description=description,
                            # external_gateway_info=''
                            # availability_zones=['nova'],
                            is_admin_state_up=is_admin_state_up,
                        )
        except Exception, e:
            log.error('router create(op) error, reason is: %s' % e)
            return request_result(1041)
        return request_result(0, op_result.id)

    def router_delete(self, router_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.delete_router(router_uuid)
        except Exception, e:
            log.error('router delete(op) error, reason is: %s' % e)
            return request_result(1043)
        if op_result is not None:
            return request_result(1043)
        return request_result(0, {'resource_uuid': router_uuid})

    def router_update(self, router_uuid, router_name=None,
                      is_admin_state_up=None, up_type='name'):
        op_token = self.get_token(self.op_user,
                                  self.op_pass)
        if op_token.get('status') != 0:
            return op_token
        token = op_token.get('result').get('token')
        net_url = conf.net_url + 'routers/' + router_uuid
        headers = {"X-Auth-Token": token}
        up_dict = {
            'router': {}
        }
        if is_admin_state_up == 0:
            is_admin_state_up = False
        else:
            is_admin_state_up = True
        try:
            if up_type == 'name':
                up_dict['router']['name'] = router_name
            if up_type == 'is_admin_state_up':
                up_dict['router']['admin_state_up'] = is_admin_state_up
            else:
                up_dict['router']['name'] = router_name
                up_dict['router']['admin_state_up'] = is_admin_state_up

            requests.put(url=net_url,
                         json=up_dict,
                         headers=headers,
                         timeout=10)
        except Exception, e:
            log.error('update the router(op) error, reason is: %s' % e)
            return request_result(1042)

        return request_result(0, {'resource_uuid': router_uuid})

    def gateway_to_router(self, router_uuid, network_uuid):
        """
        :param router_uuid:
        :param gateway: external_gateway_info: {'network_id': ''}
        :return:
        """
        """
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.add_gateway_to_router(router_uuid,
                                                                **gateway)
            print('---: %s' % op_result)
        except Exception, e:
            log.error('add the gateway to router(op) error, reason is: %s' % e)
            return request_result(1042)
        log.info('add the gateway to router , the result is: %s' % op_result)
        return request_result(0)
        """
        op_token = self.get_token(conf.op_user,
                                  conf.op_pass)
        if op_token.get('status') != 0:
            log.error('get the token of openstack error, '
                      'token result is: %s' % op_token)
        token = op_token.get('result').get('token')
        net_url = conf.net_url + 'routers/' + router_uuid
        headers = {"X-Auth-Token": token}
        # add
        if network_uuid is not None and network_uuid != '':
            up_dict = {
                "router":
                    {
                        "external_gateway_info":
                            {
                                "network_id":
                                    network_uuid
                            }
                    }
            }
        else:
            up_dict = {
                "router":
                    {
                        "external_gateway_info":
                            {}
                    }
            }
        result = requests.put(url=net_url, json=up_dict, headers=headers,
                              timeout=10)
        if result.status_code != 200:
            return request_result(1042)
        else:
            return request_result(0, {'resource_uuid': router_uuid})

    # def remove_gateway_from_router(self, router_uuid, network_uuid):
    #     if self.conn is False:
    #         return request_result(701)
    #     try:
    #         op_result = self.conn.network.remove_gateway_from_router(
    #                          router_uuid,
    #                          **network_uuid)
    #     except Exception, e:
    #         log.error('remove the gateway from router(op) '
    #                   'error, reason is: %s' % e)
    #         return request_result(1042)
    #     log.info('remove gateway from router result is: %s' % op_result)
    #     return request_result(0)

    def add_interface_to_router(self, router_uuid, subnet_uuid=None,
                                port_uuid=None):
        if self.conn is False:
            return request_result(701)
        try:
            self.conn.network.add_interface_to_router(router_uuid, subnet_uuid,
                                                      port_uuid)
        except Exception, e:
            log.error('add interface to router(op) error, reason is: %s' % e)
            return request_result(1042)
        return request_result(0, {'resource_uuid': router_uuid})

    def remove_interface_from_router(self, router_uuid, subnet_uuid=None,
                                     port_uuid=None):
        if self.conn is False:
            return request_result(701)
        try:
            self.conn.network.remove_interface_from_router(router_uuid,
                                                           subnet_uuid,
                                                           port_uuid)
        except Exception, e:
            log.error('remove interface from router(op) error, '
                      'reason is: %s' % e)
            return request_result(1042)
        return request_result(0, {'resource_uuid': router_uuid})

    # 随机生成IP
    def port_create(self, network_uuid, name=None, description=None,
                    device_id=None, device_owner=None, ip_address=None,
                    fixed_ips=None, is_admin_state_up=None,
                    mac_address=None, subnet_uuid=None):

        log.info('port name is: %s, description is: %s' % (name, description))

        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.create_port(network_id=network_uuid)
        except Exception, e:
            log.error('create the port error, reason is: %s' % e)
            return request_result(1061)

        return request_result(0, op_result)

    def port_delete(self, port_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            self.conn.network.delete_port(port_uuid)
        except Exception, e:
            log.error('delete the port error, reason is: %s' % e)
            return request_result(1062)

        return request_result(0)

    def get_port(self, port_uuid):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.get_port(port_uuid)
        except Exception, e:
            log.error('get the detail of the port(op) error, '
                      'reason is: %s' % e)
            return request_result(1064)
        return op_result

    def add_ip_to_port(self, port_uuid, ip):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.add_ip_to_port(port=port_uuid,
                                                         ip=ip)
        except Exception, e:
            log.error('add ip to port(op) error, reason is: %s' % e)
            return request_result(1063)
        log.info('add ip to port result is: %s' % op_result)
        return request_result(0, op_result)

    def remove_ip_from_port(self, ip):
        if self.conn is False:
            return request_result(701)
        try:
            op_result = self.conn.network.remove_ip_from_port(ip)
        except Exception, e:
            log.error('remove the ip from port(op) error, reason is: %s' % e)
            return request_result(1063)

        return request_result(0, op_result)

    # floating IP about
    def find_available_floating_ip(self):
        try:
            op_result = self.conn.network.find_available_ip()
        except Exception, e:
            log.error('find a available floating ip error, reason is: %s' % e)
            return request_result(1055)
        return request_result(0, op_result)

    def floating_ip_pools(self):
        try:
            op_result = self.conn.network.ips()
        except Exception, e:
            log.error('list the floating ip pools error, reason is: %s' % e)
            return request_result(1055)
        return request_result(0, op_result)

    def floating_ip_create(self, floating_network_id):
        """
        :param floating_network_id: 外网id
        :return:
        """
        try:
            op_result = self.conn.network.create_ip(
                            # name='testyyy',
                            # desription='test',
                            # fixed_ip_address=None,
                            # floating_ip_address=None,
                            floating_network_id=floating_network_id
                            # port_id=None,
                            # qos_policy_id=None,
                            # revision_number=4,
                            # router_id=''
            )
        except Exception, e:
            log.error('create the floating ip(op) error, reason is: %s' % e)
            return request_result(1051)

        return request_result(0, op_result)

    def floating_ip_delete(self, floatingip_uuid):
        try:
            self.conn.network.delete_ip(floatingip_uuid, ignore_missing=False)
            # ignore_missing:
            # When set to False ResourceNotFound will be raised when the
            # floating ip does not exist. When set to True, no exception
            # will be set when attempting to delete a nonexistent ip.
        except Exception, e:
            log.error('delete the floating ip(op) error, reason is: %s' % e)
            return request_result(1053)

        return request_result(0, {'resource_uuid': floatingip_uuid})

    def floatip_bind(self, vm_uuid, floatip, fixed_address=None):
        """
        :param vm_uuid:
        :param floatip:
        :param fixed_address:
        :return: None
        """
        try:
            self.conn.compute.add_floating_ip_to_server(
                server=vm_uuid,
                address=floatip,
                fixed_address=fixed_address
            )
        except Exception, e:
            log.error('add the floating ip to server(op) error, reason is: '
                      '%s' % e)
            return request_result(1056)

        return request_result(0)

    def floatip_unbind(self, vm_uuid, floatip):
        try:
            self.conn.compute.remove_floating_ip_from_server(
                server=vm_uuid,
                address=floatip
            )
        except Exception, e:
            log.error('remove the floating ip from server(op) error, '
                      'reason is: %s' % e)
            return request_result(1059)

        return request_result(0)

    def add_os_interface(self, vm_uuid, port_uuid):
        op_token = self.get_token(conf.op_user,
                                  conf.op_pass)
        if op_token.get('status') != 0:
            log.error('get the token of openstack error, '
                      'token result is: %s' % op_token)
            return request_result(1081)
        token = op_token.get('result').get('token')
        nova_url = conf.compute_url + vm_uuid + '/os-interface'
        log.info('>>>>>>>>>>url: %s' % nova_url)
        headers = {"X-Auth-Token": token}

        data = {
            "interfaceAttachment": {
                "port_id": port_uuid
            }
        }
        try:
            op_result = requests.post(nova_url,
                                      headers=headers,
                                      json=data,
                                      timeout=20)
            if op_result.status_code != 200:
                return request_result(1081)
        except Exception, e:
            log.error('add interface to vm error, reason is: %s' % e)
            return request_result(1081)

        return request_result(0)

    def remove_os_interface(self, vm_uuid, port_uuid):
        op_token = self.get_token(conf.op_user,
                                  conf.op_pass)
        if op_token.get('status') != 0:
            log.error('get the token of openstack error, '
                      'token result is: %s' % op_token)
            return request_result(1082)
        token = op_token.get('result').get('token')
        nova_url = conf.compute_url + vm_uuid + '/os-interface/' + port_uuid
        headers = {"X-Auth-Token": token}
        try:
            op_result = requests.delete(nova_url,
                                        headers=headers,
                                        timeout=20)
            if op_result.status_code != 202:
                return request_result(1082)
        except Exception, e:
            log.error('remove interface from vm error, reason is: %s' % e)
            return request_result(1082)

        return request_result(0)


if __name__ == '__main__':
    op = OpenstackDriver()
    # print op.port_create(network_uuid='7a94ac97-0c67-4455-89de-7ffd4e70cb39',
    #                      name='test',
    #                      description='test')
    # port = op.get_port('4219d572-3931-4364-a4cb-6b620a9be799')
    # print port
    # print op.add_ip_to_port(port, [{'ip_address':'172.20.2.12'}])
    # print op.add_os_interface('c12db4ae-0ef2-41c7-bd3e-4bc459b3cd9c',
    #                           '32debd06-dc60-446c-953f-a182e2d2f553')
    print op.remove_os_interface('c12db4ae-0ef2-41c7-bd3e-4bc459b3cd9c',
                                 '56f9ea45-81e9-496c-98a7-8c94bbaab3a7')
