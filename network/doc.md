接口相关：
post http://localhost:9990/api/v1.0/network/networks?subnet=1 (默认不创建子网)

add interface:
put http://localhost:9990/api/v1.0/network/routers/d6cd9ba3-4bd0-4579-b481-5c0354c24429?up_type=interface
{"router_uuid":"d6cd9ba3-4bd0-4579-b481-5c0354c24429","network_uuid": "d6c7a852-f509-4c4a-83cc-907a38da8a82", "rtype":"add","subnet_uuid":"87b09620-c5e8-4a22-baf0-6ad23a643038","ip_address":"172.20.2.3"}

subnet创建参数示例：
    {"name":"for_test444","description":"happy test subnet",
    "is_dhcp_enabled":1,"network_uuid":"d4ca9465-62bc-4d4d-9296-c93c821aa7bf",
    "ip_version":4,"gateway_ip":"172.20.2.2","cidr":"172.20.2.0/24"}
network创建参数示例：
    {"name":"testaaa","description": "description","is_admin_state_up":1,
    "is_shared":0}
router创建参数示例：
    {"name":"test111","description": "description", "is_admin_state_up":1}
router更新参数：
    ?up_type='name' or up_type=is_admin_state_up
    {"name":"xxx"}
    or
    {"is_admin_state_up": 0/1}
floatingip创建示例:
    {"network_id": ""}

gateway:
添加： {"network_uuid": network_uuid}
删除:
      {"network_uuid": ""}

interface:
add: {"subnet_uuid":"","rtype":"add"}
remove: {"subnet_uuid":"", "rtype":"remove"}

port:
create: {"network_uuid":"f23415a1-3216-493a-936e-c2b6157f7f82","name":"","description":""}


代码相关：
查询network列表sql：
select a.name, b.name as subnet_name, b.cidr, a.description, a.is_shared,
a.is_router_external, a.size, a.status, a.is_admin_state_up, a.create_time
from network a, subnet b, resources_acl c where a.is_show=1 and
a.uuid=b.network_uuid and a.uuid=c.resource_uuid and
c.project_uuid='13f89779-0656-4808-b726-2b18afa5b268' and
c.team_uuid='b46179e2-eb30-49bf-bee4-e97e67631465'
union
select a.name, '' as subnet_name, '' as cidr, a.description, a.is_shared,
a.is_router_external, a.size, a.status, a.is_admin_state_up,
a.create_time from network a, subnet b, resources_acl c where a.is_show=1
and a.uuid=c.resource_uuid and
c.project_uuid='13f89779-0656-4808-b726-2b18afa5b268'
and c.team_uuid='b46179e2-eb30-49bf-bee4-e97e67631465'
order by create_time desc limit 0, 1;

OpenStack里的浮动ip
缺省情况下实例会被赋予固定ip，这时并不能保证实例会马上可以从外面访问到，一般来说需要配置防火墙
来允许公共ip，然后建立一条NAT规则从公共ip到私有ip的映射。OpenStack引入了一个叫浮动ip的概念，
浮动ip是一些可以从外部访问的ip列表，通常从isp哪里买来的。浮动ip缺省不会自动赋给实例，用户需要
手动从地址池里抓取然后赋给实例。一旦用户抓去后，他就变成这个ip的所有者，可以随意赋给自己拥有的
其他实例。如果实例死掉了的话，用户也不会失去这个浮动ip，可以随时赋给其他实例。暂时不支持为了负
载均衡多实例共享一个浮动ip。而对于固定ip来说，实例启动后获得的ip也是自动的，不能指定某一个。
所以当一个VM歇菜了，再启动也许固定ip就换了一个。系统管理员可以配置多个浮动ip池，这个ip池不能
指定租户，每个用户都可以去抓取。多浮动ip池是为了考虑不同的isp服务提供商，免得某一个isp出故障
带来麻烦。如果运行的是企业云，浮动ip池就是那些openstack外的数据中心都能访问到的ip。
浮动ip机制给云用户提供了很多灵活性，也给系统管理员减少了安全风险，尽量只让OpenStack软件去改
防火墙会安全些。


########################
***工作完成情况概述
   ****网络、子网的创建功能完善与完成。
   ****路由相关功能的实现与完成（创建、删除、修改、查询、gateway的增加与删除，interface的增加与删除(gateway与interface暂未全部完成)）
   ****浮动ip创建、释放（还有关联与解关  还有待实现）
