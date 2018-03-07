# -*- coding: utf-8 -*-
# Author: YanHua <yunshu360@163.com>

import api_define

from flask import Flask
from flask_restful import Api
from flask_cors import CORS


def rest_app_run(api_host, port, debug):

    app = Flask(__name__)
    CORS(app=app)
    api = Api(app)

    api.add_resource(api_define.CloudHostsApi,
                     '/api/v1.0/compute/cloudhosts')

    api.add_resource(api_define.CloudHostApi,
                     '/api/v1.0/compute/cloudhosts/<cloudhost_uuid>')

    api.add_resource(api_define.SnapShotsApi,
                     '/api/v1.0/compute/snapshots')

    api.add_resource(api_define.SnapShotApi,
                     '/api/v1.0/compute/snapshots/<snapshot_uuid>')

    app.run(threaded=True, host=api_host, port=port, debug=debug)
