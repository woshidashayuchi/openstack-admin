# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 9:55
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define

app = Flask(__name__)
CORS(app=app)
api = Api(app)


def app_run():
    api.add_resource(restapi_define.CloudhostApi,
                     '/api/v1.0/compute/cloudhosts')

    api.add_resource(restapi_define.ClouhostRouteApi,
                     '/api/v1.0/compute/cloudhosts/<cloudhost_uuid>')

    api.add_resource(restapi_define.KeypairApi,
                     '/api/v1.0/compute/keypairs')

    api.add_resource(restapi_define.KeypairRouteApi,
                     '/api/v1.0/compute/keypairs/<keypair_uuid>')

    api.add_resource(restapi_define.NetworkToServerApi,
                     '/api/v1.0/compute/others')

    # api.add_resource(restapi_define.PasswordApi,
    #                  '/api/v1.0/compute/password')
    app.run(host='0.0.0.0', port=9998, threaded=True, debug=True)