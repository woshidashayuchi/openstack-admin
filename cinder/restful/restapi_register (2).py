# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/26 9:16
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define

app = Flask(__name__)
CORS(app=app)
api = Api(app)


def app_run():
    # 存储
    api.add_resource(restapi_define.CinderApi,
                     '/api/v1.0/cinder/volumes')

    api.add_resource(restapi_define.CinderRouteApi,
                     '/api/v1.0/cinder/volumes/<volume_uuid>')

    # 类型
    api.add_resource(restapi_define.TypeApi,
                     '/api/v1.0/cinder/types')

    api.add_resource(restapi_define.TypeRouteApi,
                     '/api/v1.0/cinder/types/<type_uuid>')

    # 快照
    api.add_resource(restapi_define.SnapshotApi,
                     '/api/v1.0/cinder/snapshots')

    api.add_resource(restapi_define.SnapshotRouteApi,
                     '/api/v1.0/cinder/snapshots/<snapshot_uuid>')

    # 绑定与解绑
    api.add_resource(restapi_define.AttachmentApi,
                     '/api/v1.0/cinder/attachments')

    api.add_resource(restapi_define.AttachmentRouteApi,
                     '/api/v1.0/cinder/attachments/<volume_uuid>')

    # 镜像

    app.run(host='0.0.0.0', port=9999, threaded=True, debug=True)
