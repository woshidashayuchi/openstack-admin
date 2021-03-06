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
    "filename": "./docs/main.js",
    "group": "E__program_op_cinder_docs_main_js",
    "groupTitle": "E__program_op_cinder_docs_main_js",
    "name": ""
  },
  {
    "type": "delete",
    "url": "/api/v1.0/cinder/snapshots/<snapshot_uuid>?logic=1/0",
    "title": "2 解绑",
    "name": "delete",
    "group": "attachment",
    "version": "1.0.0",
    "description": "<p>接触卷绑定</p>",
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
            "field": "args",
            "description": ""
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "attachment",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": attachment_uuid}\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/cinder/volumes",
    "title": "1 绑定卷到实例",
    "name": "post",
    "group": "attachment",
    "version": "1.0.0",
    "description": "<p>attachment</p>",
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
          "content": "{\n     \"server_uuid\": server_uuid, \n     \"volume_uuid\": volume_uuid\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "attachment",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": attachment_uuid}\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/api/v1.0/cinder/snapshots/<snapshot_uuid>?logic=1/0",
    "title": "5 删除存储卷",
    "name": "delete",
    "group": "snapshot",
    "version": "1.0.0",
    "description": "<p>删除</p>",
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
            "field": "args",
            "description": ""
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "snapshot",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": anapshot_uuid}\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/cinder/snapshots/<snapshot_uuid>",
    "title": "3 获取快照详情",
    "name": "detail",
    "group": "snapshot",
    "version": "1.0.0",
    "description": "<p>详情</p>",
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
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "snapshot",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n   \"status\": 0,\n   \"msg\": \"OK\",\n   \"result\": {\n       'snapshot_uuid': snapshot_uuid\n       'name': name\n       'description': description\n       'status': status\n       'metadata': metadata\n       'size': size\n       'volume_uuid': volume_uuid\n       'is_forced': is_forced\n       'create_time': create_time\n   }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/cinder/snapshots?page_num=<page_num>&page_size=<page_size>",
    "title": "2 获取快照列表",
    "name": "list",
    "group": "snapshot",
    "version": "1.0.0",
    "description": "<p>存储</p>",
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
          },
          {
            "group": "Parameter",
            "type": "tuple",
            "optional": false,
            "field": "args",
            "description": ""
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "snapshot",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n            {'snapshot_uuid': snapshot_uuid,\n             'name': name,\n             'description': description,\n             'status': status,\n             'metadata': metadata,\n             'size': size,\n             'volume_uuid': volume_uuid,\n             'is_forced': is_forced,\n             'create_time': create_time},\n             ...\n             {'snapshot_uuid': snapshot_uuid,\n             'name': name,\n             'description': description,\n             'status': status,\n             'metadata': metadata,\n             'size': size,\n             'volume_uuid': volume_uuid,\n             'is_forced': is_forced,\n             'create_time': create_time},\n             ...\n        }",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/cinder/snapshots",
    "title": "1 创建卷快照",
    "name": "post",
    "group": "snapshot",
    "version": "1.0.0",
    "description": "<p>快照</p>",
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
          "content": "{\n    \"name\":\"xxxx-yyyy\", \n    \"volume_uuid\":\"e9b35f2b-aeb2-491f-b537-2aab69864457\",\n    \"description\":\"xxxx-yyyy snap for volume\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "snapshot",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": anapshot_uuid}\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/cinder/snapshots/<snapshot_uuid>",
    "title": "4 更新快照",
    "name": "update",
    "group": "snapshot",
    "version": "1.0.0",
    "description": "<p>更新</p>",
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
          "content": "{\n    \"name\":\"xxxx-zzzzz\",\n    \"description\":\"bind token test 2\",\n    \"up_type\":\"可选参数，当要恢复逻辑删除的存储卷时可设置其值为recovery\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "snapshot",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": anapshot_uuid}\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "delete",
    "url": "/api/v1.0/cinder/volumes/<volume_uuid>?logic=1/0",
    "title": "5 删除存储卷",
    "name": "delete",
    "group": "volume",
    "version": "1.0.0",
    "description": "<p>删除</p>",
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
            "field": "args",
            "description": ""
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "volume",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": volume_uuid}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/cinder/volumes/<volume_uuid>",
    "title": "3 获取存储卷详情",
    "name": "detail",
    "group": "volume",
    "version": "1.0.0",
    "description": "<p>详情</p>",
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
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "volume",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n   \"status\": 0,\n   \"msg\": \"OK\",\n   \"result\": {\n       'volume_uuid': volume_uuid\n       'name'= name\n       'description'= description\n       'size'= size\n       'status'= status\n       'v_type'= type\n       'conn_to'= conn_to\n       'is_use_domain': is_use_domain\n       'is_start': 1/0\n       'is_secret'= volume[9]\n       'snapshot_uuid' = volume[10]\n       'source_volume_uuid' = volume[11]\n       'image_uuid'= volume[12]\n       'create_time'= time_diff(volume[13]\n   }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "get",
    "url": "/api/v1.0/cinder/volumes?page_num=<page_num>&page_size=<page_size>",
    "title": "2 获取存储卷列表",
    "name": "list",
    "group": "volume",
    "version": "1.0.0",
    "description": "<p>存储</p>",
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
          },
          {
            "group": "Parameter",
            "type": "tuple",
            "optional": false,
            "field": "args",
            "description": ""
          }
        ]
      }
    },
    "filename": "./apidoc.py",
    "groupTitle": "volume",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\": {\n        {'volume_uuid': volume_uuid,\n         'name': name,\n         'description': description,\n         'size': size,\n         'status': status,\n         'v_type': v_type,\n         'conn_to': conn_to,\n         'snapshot_uuid': snapshot_uuid,\n         'source_volume_uuid': source_volume_uuid,\n         'image_uuid': image_uuid,\n         'is_use_domain': is_use_domain,\n         'is_start': is_start,\n         'is_secret': is_secret,\n         'create_time': create_time},\n               ...\n        {'volume_uuid': volume_uuid,\n         'name': name,\n         'description': description,\n         'size': size,\n         'status': status,\n         'v_type': v_type,\n         'conn_to': conn_to,\n         'snapshot_uuid': snapshot_uuid,\n         'source_volume_uuid': source_volume_uuid,\n         'image_uuid': image_uuid,\n         'is_use_domain': is_use_domain,\n         'is_start': is_start,\n         'is_secret': is_secret,\n         'create_time': create_time},\n              ...\n    }\n}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "post",
    "url": "/api/v1.0/cinder/volumes",
    "title": "1 创建存储卷",
    "name": "post",
    "group": "volume",
    "version": "1.0.0",
    "description": "<p>存储</p>",
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
          "content": "{\n     \"name\":\"xxxx-zzzzz\",\n      \"size\":1,\n      \"v_type\":\"lvm\",\n      \"description\":\"bind token test 2\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "volume",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": volume_uuid}",
          "type": "json"
        }
      ]
    }
  },
  {
    "type": "put",
    "url": "/api/v1.0/cinder/volumes/<volume_uuid>",
    "title": "4 更新存储卷",
    "name": "update",
    "group": "volume",
    "version": "1.0.0",
    "description": "<p>更新</p>",
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
          "content": "{\n    \"name\":\"xxxx-zzzzz\",\n    \"description\":\"bind token test 2\",\n    \"up_type\":\"可选参数，当要恢复逻辑删除的存储卷时可设置其值为recovery\"\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./apidoc.py",
    "groupTitle": "volume",
    "success": {
      "examples": [
        {
          "title": "返回",
          "content": "{\n    \"status\": 0,\n    \"msg\": \"OK\",\n    \"result\":{\"resource_uuid\": volume_uuid}",
          "type": "json"
        }
      ]
    }
  }
] });
