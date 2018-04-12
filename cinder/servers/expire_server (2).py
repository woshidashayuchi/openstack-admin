# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/9 11:51
from __future__ import unicode_literals
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
from manager.volume_manager import volume_expire_delete

if __name__ == '__main__':
    # 删除过期或者账户余额不足的存储卷
    volume_expire_delete()