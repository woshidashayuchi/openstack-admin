# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 14:03
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import restapi_define

app = Flask(__name__)
CORS(app=app)


def app_run():
    api = Api(app)
    api.add_resource(restapi_define.NetworkApi,
                     '/api/v1.0/network/networks')

    api.add_resource(restapi_define.NetworkRouteApi,
                     '/api/v1.0/network/networks/<network_uuid>')

    api.add_resource(restapi_define.SubNetApi,
                     '/api/v1.0/network/subnets')

    app.run(host='0.0.0.0', port=9998, threaded=True, debug=True)
