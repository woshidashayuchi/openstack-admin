# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:03

log_dir = 'E:\log\op_cinder.log'
#  linux下
# log_dir = '/var/log/op_cinder.log'

token_url = "http://172.20.2.12:5000/v2.0/tokens"
db_server01 = '172.16.32.140'
db_server02 = '172.16.32.140'
db_port = 3306
db_user = 'cinder'
db_passwd = 'qwe123'
database = 'network'

net_url = "http://172.20.2.12:9696/v2.0/"
compute_url = "http://172.20.2.12:8774/v2.1/servers/"
# ucenter_api = "https://center.tjiyun.com"
ucenter_api = "http://172.16.32.197:8101"

conn_cloud = 'demo'
conn_cloud_admin = 'admin'
tenantName = 'demo'
op_user = 'demo'
op_pass = 'qwe123'

mq_server01 = 'rabbitmq01'
mq_server02 = 'rabbitmq02'
mq_port = 5672
