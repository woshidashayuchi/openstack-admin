# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/15 10:54
import sys
p_path = sys.path[0] + '/..'
p_path1 = sys.path[0] + '/../..'
sys.path.insert(1, p_path)
sys.path.insert(1, p_path1)
from time import sleep
from multiprocessing import Pool
import cinder_register
from common.logs import logging as log
from common.rabbitmq_server import RabbitmqServer


def server_start(n):

    queue = 'cinder_api'

    while True:
        try:
            log.info('Starting RPC Call API Server, topic=%s'
                     % queue)
            rbtmq = RabbitmqServer(60)
            rbtmq.rpc_call_server(queue, cinder_register)
        except Exception, e:
            log.error(
                'RPC Call API Server running error, queue=%s, '
                'reason=%s' % (queue, e))
        sleep(10)


def service_start(workers=4):
    pool = Pool(workers)
    pool.map(server_start, range(workers))


if __name__ == "__main__":
    service_start()
