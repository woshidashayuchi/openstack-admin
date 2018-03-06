# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 9:50
from common import conf
from common.logs import logging as log
from sqlalchemy import MetaData, Table, create_engine, func, \
                       String, Column, Integer, DateTime, TIMESTAMP, Text


class DBInit(object):
    def __init__(self):
        pass
    db_config = {
        'host': conf.db_server01,
        'user': conf.db_compute_user,
        'passwd': conf.db_compute_passwd,
        'db': conf.compute_database,
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
    cloudhost = Table('cloudhost', metadata,
                      Column('uuid', String(64), primary_key=True),
                      Column('instance_name', String(64)),
                      Column('availability_zone', String(64)),
                      Column('access_ipv4', String(64)),
                      Column('instance_num', Integer),
                      Column('image', String(64)),
                      Column('instance_cpu', Integer),
                      Column('instance_mem', Integer),
                      Column('instance_type', String(64)),
                      Column('net', String(64)),
                      Column('net_interface', String(64)),
                      Column('security_groups', String(64)),
                      Column('keypair', String(64)),
                      Column('status', String(64)),
                      Column('power_state', String(64)),
                      Column('create_time', TIMESTAMP(True)),
                      Column('update_time', TIMESTAMP(True), nullable=False))

    keypair = Table('keypair', metadata,
                    Column('uuid', String(64), primary_key=True),
                    Column('fingerprint', String(128)),
                    Column('keypair_name', String(64)),
                    Column('private_key', Text()),
                    Column('public_key', Text()),
                    Column('create_time', TIMESTAMP(True),
                           server_default=func.now(), nullable=False))
                    # Column('update_time', TIMESTAMP(True),
                    #        server_default=func.now(), nullable=False))

    metadata.create_all(engine)
    Table('cloudhost', metadata, autoload=True)
    Table('keypair', metadata, autoload=True)
