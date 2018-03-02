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

db_compute_user = 'compute'
db_compute_passwd = 'qwe123'
compute_database = 'compute'
cinder_url = "http://controller02:8776/v2/"