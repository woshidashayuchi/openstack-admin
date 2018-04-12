# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/22 14:11
from __future__ import unicode_literals
import sys
path1 = sys.path[0] + '/..'
path2 = sys.path[0] + '/../..'
sys.path.append(path1)
sys.path.append(path2)
reload(sys)
sys.setdefaultencoding('utf8')
from manager.volume_manager import volume_del_mark_clean


if __name__ == '__main__':
    volume_del_mark_clean()
