# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:57
from common import conf
from common.logs import logging as log
from network_db import NetworkDB
from sqlalchemy import MetaData, Table, create_engine, func
from sqlalchemy import String, Column, Integer, TIMESTAMP, text


class DBInit(object):

    db_config = {
        'host': conf.db_server01,
        'user': conf.db_user,
        'passwd': conf.db_passwd,
        'db': conf.database,
        'charset': 'UTF8',
        'port': conf.db_port
    }
    try:
        engine = create_engine('mysql://%s:%s@%s:%s/%s?charset=%s' % (
            db_config['user'],
            db_config['passwd'],
            db_config['host'],
            db_config['port'],
            db_config['db'],
            db_config['charset'],
        ), echo=True)
    except Exception, e:
        log.error('engine db error, reason is: %s' % e)
        raise Exception(e)
    metadata = MetaData(engine)
    resources_acl = Table('resources_acl', metadata,
                          Column('resource_uuid', String(64),
                                 primary_key=True),
                          Column('resource_type', String(64)),
                          Column('admin_uuid', String(64)),
                          Column('team_uuid', String(64)),
                          Column('project_uuid', String(64)),
                          Column('user_uuid', String(64)),
                          Column('create_time', TIMESTAMP(True),
                                 server_default=func.now(), nullable=False),
                          Column('update_time', TIMESTAMP(True),
                                 nullable=False,
                                 server_default=text('CURRENT_TIMESTAMP '
                                                     'ON UPDATE '
                                                     'CURRENT_TIMESTAMP')
                                 ))

    network = Table('network', metadata,
                    Column('uuid', String(64), primary_key=True),
                    Column('name', String(64)),
                    Column('description', String(128)),
                    Column('is_shared', Integer),
                    Column('is_router_external', Integer),
                    Column('size', Integer),
                    Column('status', String(64)),
                    Column('is_admin_state_up', Integer),
                    Column('yuliu1', String(64), server_default=None),
                    Column('yuliu2', String(64), server_default=None),
                    Column('yuliu3', String(64), server_default=None),
                    Column('create_time', TIMESTAMP(True),
                           server_default=func.now(), nullable=False),
                    Column('update_time', TIMESTAMP(True), nullable=False,
                           server_default=text('CURRENT_TIMESTAMP '
                                               'ON UPDATE CURRENT_TIMESTAMP')
                           )
                    )

    subnet = Table('subnet', metadata,
                   Column('uuid', String(64), primary_key=True),
                   Column('network_uuid', String(64)),
                   Column('name', String(64)),
                   Column('description', String(128)),
                   Column('is_dhcp_enabled', Integer),
                   Column('ip_version', Integer),
                   Column('gateway_ip', String(32)),
                   Column('allocation_pools', String(64)),
                   Column('cidr', String(32)),
                   Column('dns_nameservers', String(32), server_default=None),
                   Column('host_routes', String(64), server_default=None),
                   Column('create_time', TIMESTAMP(True),
                          server_default=func.now(), nullable=False),
                   Column('update_time', TIMESTAMP(True), nullable=False,
                          server_default=text('CURRENT_TIMESTAMP '
                                              'ON UPDATE CURRENT_TIMESTAMP'))
                   )

    metadata.create_all(engine)

    # 初始化数据(acl 表数据)
    net_db = NetworkDB()
    try:
        net_db.data_init()
    except Exception, e:
        log.error('data init error ,reason is: %s' % e)
        raise Exception('resources_acl init error')
