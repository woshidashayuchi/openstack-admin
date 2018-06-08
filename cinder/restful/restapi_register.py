# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/2/26 9:16
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define


def app_run():
    
    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)
    
    api.add_resource(restapi_define.CinderApi,
                     '/api/v1.0/storage/volumes')

    api.add_resource(restapi_define.CinderRouteApi,
                     '/api/v1.0/storage/volumes/<volume_uuid>')

    api.add_resource(restapi_define.TypeApi,
                     '/api/v1.0/storage/types')

    api.add_resource(restapi_define.TypeRouteApi,
                     '/api/v1.0/storage/types/<type_uuid>')

    api.add_resource(restapi_define.SnapshotApi,
                     '/api/v1.0/storage/snapshots')

    api.add_resource(restapi_define.SnapshotRouteApi,
                     '/api/v1.0/storage/snapshots/<snapshot_uuid>')

    api.add_resource(restapi_define.AttachmentApi,
                     '/api/v1.0/storage/attachments')

    api.add_resource(restapi_define.AttachmentRouteApi,
                     '/api/v1.0/storage/attachments/<volume_uuid>')

    api.add_resource(restapi_define.TempletApi,
                     '/api/v1.0/storage/templets')

    api.add_resource(restapi_define.TempletRouteApi,
                     '/api/v1.0/storage/templets/<templet_uuid>')

    app.run(host='0.0.0.0', port=9999, threaded=True, debug=True)
