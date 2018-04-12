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

    api.add_resource(restapi_define.SubnetRoutApi,
                     '/api/v1.0/network/subnets/<subnet_uuid>')

    api.add_resource(restapi_define.RouterApi,
                     '/api/v1.0/network/routers')

    api.add_resource(restapi_define.RouterRouteApi,
                     '/api/v1.0/network/routers/<router_uuid>')

    api.add_resource(restapi_define.PortApi,
                     '/api/v1.0/network/ports')

    api.add_resource(restapi_define.PortRouteApi,
                     '/api/v1.0/network/ports/<port_uuid>')

    api.add_resource(restapi_define.FloatingipApi,
                     '/api/v1.0/network/floatingips')

    api.add_resource(restapi_define.FloatingipRouteApi,
                     '/api/v1.0/network/floatingips/<floatingip_uuid>')

    app.run(host='0.0.0.0', port=9990, threaded=True, debug=True)
