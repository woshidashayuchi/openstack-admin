# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>


# global config

db_server01 = '127.0.0.1'
db_server02 = '127.0.0.1'
db_port = 3306
db_user = 'cloud'
db_passwd = 'cloud'
database = 'compute'

api_server = '0.0.0.0'
api_debug = True

log_level = 'INFO'
log_file = '/var/log/compute.log'

keystone = 'http://controller:5000/v3'
billing = False

# compute config

compute_port = 8201

compute_db_user = 'cloud'
compute_db_passwd = 'cloud'
compute_database = 'compute'
