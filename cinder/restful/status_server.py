# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/13 14:47
from __future__ import unicode_literals
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
from manager.volume_manager import volume_status_monitor

if __name__ == '__main__':
    # 当存储状态有变化的时候更新数据库
    volume_status_monitor()
