define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc/main.js",
    "group": "E__program_network_doc_main_js",
    "groupTitle": "E__program_network_doc_main_js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/floatingips",
    "title": "3.1 申请弹性ip",
    "name": "create_floatingip",
    "group": "floatingip",
    "version": "1.0.0",
    "description": "<p>浮动ip</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": ""
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n\"network_id\": \"string\"       # 外网ip\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "floatingip",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"resource_uuid\": \"string\",\n        \"name\": \"string\",\n        \"description\": \"string\",\n        \"router_uuid\": \"string\",\n        \"fixed_ip_address\": \"string\",\n        \"floating_ip_address\": \"string\",\n        \"revision_number\": int,\n        \"port_id\": \"string\"\n    }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/api/v1.0/network/floatingapis/<floatingip_uuid>",
    "title": "3.4 释放弹性ip",
    "name": "floatingip_delete",
    "group": "floatingip",
    "version": "1.0.0",
    "description": "<p>浮动ip</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "floatingip",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"resource_uuid\": \"string\",\n        \"name\": \"string\",\n        \"description\": \"string\",\n        \"router_uuid\": \"string\",\n        \"fixed_ip_address\": \"string\",\n        \"floating_ip_address\": \"string\",\n        \"revision_number\": int,\n        \"port_id\": \"string\"\n    }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/network/floatingapis/<floatingip_uuid>",
    "title": "3.3 弹性ip详情",
    "name": "floatingip_detail",
    "group": "floatingip",
    "version": "1.0.0",
    "description": "<p>浮动ip</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "floatingip",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\":\n        {\n            \"description\": \"string\",                 # 弹性ip描述\n            \"fixed_ip_address\": \"string\",            # 弹性ip关联的固定ip地址\n            \"floating_ip_address\": \"string\",         # 弹性ip地址\n            \"floatingip_uuid\": \"string\",             # 弹性ip的id\n            \"name\": \"string\",                        # 弹性ip名称\n            \"port_id\": \"string\",                     # 绑定port的id\n            \"revision_number\": int,                  # 版本\n            \"router_uuid\": \"string\",                 # 绑定路由id\n            \"create_time\": \"YYYY-MM-DD HH:MM:SS\",    # 创建时间\n            \"update_time\": \"YYYY-MM-DD HH:MM:SS\"     # 更新时间\n        }\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/network/floatingips?page_num=a&page_size=b",
    "title": "3.2 弹性ip列表",
    "name": "floatingip_list",
    "group": "floatingip",
    "version": "1.0.0",
    "description": "<p>浮动ip</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "floatingip",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": [\n        {\n            \"description\": \"string\",\n            \"fixed_ip_address\": \"string\",\n            \"floating_ip_address\": \"string\",\n            \"floatingip_uuid\": \"string\",\n            \"name\": \"string\",\n            \"port_id\": \"string\",\n            \"revision_number\": int,\n            \"router_uuid\": \"string\",\n            \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n            \"update_time\": \"YYYY-MM-DD HH:MM:SS\"    \n        }\n        {\n            ···\n        }\n    ],\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/networks",
    "title": "1.1 创建网络",
    "name": "create",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": ""
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n     \"name\":\"string\",              # 网络名称，若同时选择创建子网，子网与名称相同\n     \"description\": \"string\",      # 网络描述 \n     \"is_admin_state_up\":int,      # 管理员状态\n     \"is_shared\": int              # 是否外部共享\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{ \"resource_uuid\": \"string\",\n  \"name\": \"string\",\n  \"description\": \"string\",\n  \"is_admin_state_up\": \"string\",\n  'is_shared': int\n  }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/networks",
    "title": "1.2 带子网部分创建网络",
    "name": "create_and_subnet",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": ""
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n     \"name\":\"string\",                  # 网络名称，若同时选择创建子网，子网与名称相同\n     \"description\": \"string\",          # 网络描述 \n     \"is_admin_state_up\": int,         # 管理员状态\n     \"is_shared\": int                  # 是否外部共享\n     \"is_dhcp_enabled\": int,           # 是否激活dhcp\n     \"ip_version\": int,                # ip地址版本，4（可选）\n     \"gateway_ip\":\"string\",            # 网关（可选） \n     \"cidr\":\"string\"                   # CIDR \n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{ \"resource_uuid\": \"string\",\n  \"name\": \"string\",\n  \"description\": \"string\",\n  \"is_admin_state_up\": \"string\",\n  'is_shared': int\n  }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/subnets",
    "title": "1.3 单独创建子网",
    "name": "create_subnet_only",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": ""
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n     \"name\":\"strng\",                 # 子网名称\n     \"description\":\"string\",         # 子网描述\n     \"is_dhcp_enabled\":int,          # 是否开启dhcp\n     \"network_uuid\":\"string\",        # 关联网络id\n     \"ip_version\":int,               # 版本\n     \"gateway_ip\":\"string\",          # 网关\n     \"cidr\":\"string\"                 # cidr\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"resource_uuid\": network_uuid\n        }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/api/v1.0/network/networks/<network_uuid>",
    "title": "1.7 网络删除",
    "name": "delete_network",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"resource_uuid\": network_uuid\n        }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/network/networks/<network_uuid>",
    "title": "1.5 网络详情",
    "name": "network_detail",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": " {\n    \"msg\": \"ok\",\n    \"result\": {\n        \"description\": \"string\",               # 描述\n        \"is_admin_state_up\": int,              # 是否启用管理员状态（1:启用，0:不启用）\n        \"is_router_external\": int,             # 外部是否可以访问\n        \"is_shared\": int,                      # 是否共享\n        \"name\": \"string\",                      # 网络名称\n        \"status\": \"string\",                    # 网络状态\n        \"subnet_name_and_cidr\": \"string\",      # 已连接的子网信息（\"名称 CIDR\"）\n        \"create_time\": \"YYYY-MM-DD HH:MM:SS\",  # 创建时间\n        \"update_time\": \"YYYY-MM-DD HH:MM:SS\"   # 最新更新时间\n    },\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/network/networks?page_num=a&page_size=b",
    "title": "1.4 网络列表",
    "name": "network_list",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": [\n        {\n            \"description\": \"string\",\n            \"is_admin_state_up\": int,\n            \"is_router_external\": int,\n            \"is_shared\": int,\n            \"name\": \"string\",\n            \"network_uuid\": \"string\",\n            \"status\": \"string\",\n            \"subnet_name_and_cidr\": \"string\"\n            \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n            \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n        }\n        \n        {\n            ······\n        }\n        {\n            ······\n        }\n    ],\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/network/networks/<network_uuid>",
    "title": "1.6 网络更新",
    "name": "update_network",
    "group": "network",
    "version": "1.0.0",
    "description": "<p>网络</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": "<p>{ &quot;name&quot;: &quot;string&quot;               # 名称 &quot;is_admin_state_up&quot;: int       # 是否启用管理员状态 }</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "network",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"resource_uuid\": network_uuid\n        }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/ports",
    "title": "4.1 创建port",
    "name": "port_create",
    "group": "port",
    "version": "1.0.0",
    "description": "<p>端口（即基于network创建的固定ip）</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": ""
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n \"network_uuid\":\"string\",  # 基于网络的uuid\n \"name\":\"string\",          # port名称\n \"description\":\"string\"    # port描述\n }",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "port",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": {\n        \"resource_uuid\": \"string\"  # port_uuid\n    },\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/api/v1.0/network/ports/<port_uuid>",
    "title": "4.3 删除port",
    "name": "port_delete",
    "group": "port",
    "version": "1.0.0",
    "description": "<p>删除port</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "port",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": {\n        \"resource_uuid\": \"string\"  # port_uuid\n    },\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/ports?network_uuid=<string>&page_num=<int>&page_size=<int>",
    "title": "4.2 port列表",
    "name": "ports_list",
    "group": "port",
    "version": "1.0.0",
    "description": "<p>port列表</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "port",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": [\n        {\n            \"description\": \"string\",\n            \"ip_address\": \"string\",\n            \"mac_address\": \"string\",\n            \"name\": \"string\",\n            \"port_uuid\": \"string\",\n            \"status\": \"DOWN\",\n            \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n            \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n        }\n        {\n            ···\n        }\n        {\n            ···\n        }\n    ],\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/network/routers",
    "title": "2.1 创建路由",
    "name": "create_router",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          },
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "body",
            "description": ""
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n    \"name\":\"string\",                # 名称\n    \"description\": \"string\",        # 路由描述\n    \"is_admin_state_up\": int        # 是否启动管理员状态\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{ \"resource_uuid\": \"string\",\n  \"name\": \"string\",\n  \"description\": \"string\",\n  \"is_admin_state_up\": int\n  }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/api/v1.0/network/routers/<router_uuid>",
    "title": "2.4 删除路由",
    "name": "router_delete",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"router_uuid\": \"string\"\n    }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/network/routers/<router_uuid>",
    "title": "2.3 路由详情",
    "name": "router_detail",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": {\n        \"description\": \"string\",                 # 路由描述\n        \"external_gateway_info\": \"string\",       # gateway连接的网络id\n        \"is_admin_state_up\": int,                # 管理员状态\n        \"name\": \"string\",                        # 路由名字\n        \"router_uuid\": \"string\",                 # 路由id\n        \"status\": \"string\"                       # 路由状态\n        \"create_time\": \"YYYY-MM-DD HH:MM:SS\",    # 创建时间\n        \"update_time\": \"YYYY-MM-DD HH:MM:SS\"     # 更新时间\n    },\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/network/routers/<router_uuid>？up_type=gateway",
    "title": "2.8 更新gateway",
    "name": "router_gateway",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n    \"network_uuid\": network_uuid # 去除网关时，network_uuid为\"\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"router_uuid\": \"string\"\n    }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/network/routers/<router_uuid>？up_type=interface",
    "title": "2.7 更新接口",
    "name": "router_interface",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n    \"rtype\":\"add\",  # 可为add/remove\n    \"subnet_uuid\":\"87b09620-c5e8-4a22-baf0-6ad23a643038\",\n    \"ip_address\":\"172.20.2.3\"  # 该格式为指定格式，也可不传该参数\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"router_uuid\": \"string\"\n    }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/network/routers/<router_uuid>？up_type=is_admin_state_up",
    "title": "2.6 更新管理员状态",
    "name": "router_isadminstatus_update",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n    \"is_admin_state_up\":0/1\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"router_uuid\": \"string\"\n    }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/network/routers?page_num=<int>&page_size=<int>",
    "title": "2.2 路由列表",
    "name": "router_list",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"msg\": \"ok\",\n    \"result\": [\n        {\n            \n            \"description\": \"string\",\n            \"name\": \"string\",\n            \"router_uuid\": \"string\",\n            \"status\": \"string\"\n            \"create_time\": \"YYYY-MM-DD HH:MM:SS\",\n            \"update_time\": \"YYYY-MM-DD HH:MM:SS\"\n        },\n        {\n            ···\n        },\n        {\n            ···\n        }\n    ],\n    \"status\": 0\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/network/routers/<router_uuid>？up_type=name",
    "title": "2.5 更新名称",
    "name": "router_name_update",
    "group": "router",
    "version": "1.0.0",
    "description": "<p>路由</p>",
    "permission": [
      {
        "name": "all"
      }
    ],
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "json",
            "optional": false,
            "field": "header",
            "description": "<p>{&quot;token&quot;: &quot;string&quot;}</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "body",
          "content": "{\n    \"name\":\"string\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "router",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\n        \"router_uuid\": \"string\"\n    }\n}",
          "type": "json"
        }
      ]
    }
  }
] });
