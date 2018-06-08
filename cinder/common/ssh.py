# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/5/18 10:45
import conf
import paramiko
from common.logs import logging as log


def ssh():
    client = paramiko.SSHClient()
    try:
        # 第一次ssh远程时会提示输入yes或者no
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(conf.snap_ip, 22,
                       username=conf.snap_user,
                       password=conf.snap_pwd,
                       allow_agent=False,
                       look_for_keys=False,
                       timeout=10)
    except Exception, e:
        log.error('ssh connect to node error, reason is: %s' % e)
        return False

    return client


def exec_cmd(cmds):
    client = ssh()
    try:
        if client is False:
            raise Exception('ssh connect error')
        stdin, stdout, stderr = client.exec_command(cmds)
        log.info('exec the cmd(%s) result: %s' % (cmds, stdout.readlines()))
        log.info('exec the cmd(%s) stderr is: %s' % (cmds, stderr))
        return stdout.readlines()
    except Exception, e:
        log.error('ssh exec the command error, reason is: %s' % e)
        raise Exception(e)
    finally:
        client.close()
