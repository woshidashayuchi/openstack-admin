# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/23 17:03

from common import conf
import logging

logging.basicConfig(
    level=logging.INFO,
    filename=conf.log_dir,
    format=('%(asctime)s '
            '[%(levelname)s] '
            '[%(filename)s line:%(lineno)d] '
            '%(message)s'),
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='a'
    )

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(
    ('{"time": \"%(asctime)s\", '
     '"level": \"%(levelname)s\", '
     '"file": \"%(filename)s line:%(lineno)d\", '
     '"log": \"%(message)s\"}'),
    datefmt='%Y-%m-%d %H:%M:%S')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
