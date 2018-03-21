# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:03

log_dir = 'E:\log\op_cinder.log'
#  linux下
# log_dir = '/var/log/op_cinder.log'

token_url = "http://172.20.2.12:5000/v2.0/tokens"
db_server01 = '172.20.2.41'
db_server02 = '172.20.2.41'
db_port = 3306
db_user = 'cinder'
db_passwd = 'qwe123'
database = 'storage'
network_database = 'network'

db_compute_user = 'compute'
db_compute_passwd = 'qwe123'
compute_database = 'compute'
cinder_url = "http://controller02:8776/v3/c5aea850b5f344e5828c103fc9a02b1a/"

storage_db_user = 'cinder'
storage_db_passwd = 'qwe123'
storage_database = 'storage'


# ucenter_api = "https://center.tjiyun.com"
ucenter_api = "http://172.16.32.197:8101"

conn_cloud = 'demo'
conn_cloud_admin = 'admin'

op_user = 'demo'
op_pass = 'qwe123'

mq_server01 = '172.20.2.41'
mq_server02 = '172.20.2.41'
mq_port = 5672
