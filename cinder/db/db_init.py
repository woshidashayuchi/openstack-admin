# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/24 16:12
from common import conf
from common.logs import logging as log
from sqlalchemy import MetaData, Table, create_engine, func
from sqlalchemy import String, Column, Integer, TIMESTAMP


class DBInit(object):
    def __init__(self):
        pass
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
    volume = Table('volume', metadata,
                   Column('uuid', String(64), primary_key=True),
                   Column('team_uuid', String(64)),
                   Column('project_uuid', String(64)),
                   Column('user_uuid', String(64)),
                   Column('name', String(128)),
                   Column('description', String(256)),
                   Column('size', Integer),
                   Column('status', Integer),
                   Column('type', String(32)),
                   Column('conn_to', String(64)),
                   Column('is_use_domain', String(64)),
                   Column('is_start', Integer),
                   Column('is_secret', Integer),
                   Column('create_time', TIMESTAMP(True),
                          server_default=func.now(), nullable=False))

    volume_type = Table('volume_type', metadata,
                        Column('uuid', String(64), primary_key=True),
                        Column('project_uuid', String(64)),
                        Column('name', String(64)),
                        Column('description', String(256)),
                        Column('extra_specs', String(64)),
                        Column('is_public', Integer),
                        Column('create_time', TIMESTAMP(True),
                               server_default=func.now(), nullable=False))

    snapshot = Table('snapshot', metadata,
                     Column('uuid', String(64), primary_key=True),
                     Column('name', String(64)),
                     Column('description', String(256)),
                     Column('status', String(32)),
                     Column('metadata', String(128)),
                     Column('size', Integer),
                     Column('volume_uuid', String(64)),
                     Column('is_forced', String(32)),
                     Column('is_show', Integer),
                     Column('create_time', TIMESTAMP(True),
                            server_default=func.now(), nullable=False))

    resources_acl = Table('resources_acl', metadata,
                          Column('resource_uuid', String(64),
                                 primary_key=True),
                          Column('resource_type', String(64)),
                          Column('admin_uuid', String(64)),
                          Column('team_uuid', String(64)),
                          Column('project_uuid', String(64)),
                          Column('user_uuid', String(64)),
                          Column('create_time', TIMESTAMP(True),
                                 nullable=False),
                          Column('update_time', TIMESTAMP(True),
                                 server_default=func.now(), nullable=False))

    metadata.create_all(engine)

    Table('volume', metadata, autoload=True)
    Table('volume_type', metadata, autoload=True)
    Table('snapshot', metadata, autoload=True)
    Table('resources_acl', metadata, autoload=True)
