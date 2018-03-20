# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/19 9:41
"""
this is the api doc
"""
"""
@apiDefine CODE_VOL_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":{"resource_uuid": volume_uuid}
"""
"""
@apiDefine CODE_SNAPSHOT_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":{"resource_uuid": anapshot_uuid}
}
"""
"""
@apiDefine CODE_ATTACHMENT_POST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result":{"resource_uuid": attachment_uuid}
}
"""
"""
@apiDefine CODE_VOL_DETAIL_0
@apiSuccessExample 返回
 {
    "status": 0,
    "msg": "OK",
    "result": {
        'volume_uuid': volume_uuid
        'name'= name
        'description'= description
        'size'= size
        'status'= status
        'type'= type
        'conn_to'= conn_to
        'is_use_domain': is_use_domain
        'is_start': 1/0
        'is_secret'= volume[9]
        'snapshot_uuid' = volume[10]
        'source_volume_uuid' = volume[11]
        'image_uuid'= volume[12]
        'create_time'= time_diff(volume[13]
    }
 }
"""
"""
@apiDefine CODE_VOL_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
        "status": 0,
        "msg": "OK",
        "result":{{'volume_uuid': volume_uuid,
                   'name': name,
                   'description': description,
                   'size': size,
                   'status': status,
                   'type': v_type,
                   'conn_to': conn_to,
                   'snapshot_uuid': snapshot_uuid,
                   'source_volume_uuid': source_volume_uuid,
                   'image_uuid': image_uuid,
                   'is_use_domain': is_use_domain,
                   'is_start': is_start,
                   'is_secret': is_secret,
                   'create_time': create_time},
                   ...
                   {'volume_uuid': volume_uuid,
                   'name': name,
                   'description': description,
                   'size': size,
                   'status': status,
                   'type': v_type,
                   'conn_to': conn_to,
                   'snapshot_uuid': snapshot_uuid,
                   'source_volume_uuid': source_volume_uuid,
                   'image_uuid': image_uuid,
                   'is_use_domain': is_use_domain,
                   'is_start': is_start,
                   'is_secret': is_secret,
                   'create_time': create_time},
                   ...
    }
"""
"""
@apiDefine CODE_SNAPSHOT_LIST_0
@apiSuccessExample 返回
{
    "status": 0,
    "msg": "OK",
    "result": {
            {'snapshot_uuid': snapshot_uuid,
             'name': name,
             'description': description,
             'status': status,
             'metadata': metadata,
             'size': size,
             'volume_uuid': volume_uuid,
             'is_forced': is_forced,
             'create_time': create_time},
             ...
             {'snapshot_uuid': snapshot_uuid,
             'name': name,
             'description': description,
             'status': status,
             'metadata': metadata,
             'size': size,
             'volume_uuid': volume_uuid,
             'is_forced': is_forced,
             'create_time': create_time},
             ...
        }
"""
"""
@apiDefine CODE_SNAPSHOT_DETAIL_0
@apiSuccessExample 返回
 {
    "status": 0,
    "msg": "OK",
    "result": {
        'snapshot_uuid': snapshot_uuid
        'name': name
        'description': description
        'status': status
        'metadata': metadata
        'size': size
        'volume_uuid': volume_uuid
        'is_forced': is_forced
        'create_time': create_time
    }
 }
"""
"""
@api {post} /api/v1.0/cinder/volumes 1 创建存储卷
@apiName post
@apiGroup volume
@apiVersion 1.0.0
@apiDescription 存储
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
     "name":"xxxx-zzzzz",
      "size":1,
      "v_type":"lvm",
      "description":"bind token test 2"
}
@apiUse CODE_VOL_POST_0
"""
"""
@api {get} /api/v1.0/cinder/volumes?page_num=<page_num>&page_size=<page_size> 2 获取存储卷列表
@apiName list
@apiGroup volume
@apiVersion 1.0.0
@apiDescription 存储
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParam {tuple} args
@apiUse CODE_VOL_LIST_0
"""
"""
@api {get} /api/v1.0/cinder/volumes/<volume_uuid> 3 获取存储卷详情
@apiName detail
@apiGroup volume
@apiVersion 1.0.0
@apiDescription 详情
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiUse CODE_VOL_DETAIL_0
"""

"""
@api {put} /api/v1.0/cinder/volumes/<volume_uuid> 4 更新存储卷
@apiName update
@apiGroup volume
@apiVersion 1.0.0
@apiDescription 更新
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "name":"xxxx-zzzzz",
    "description":"bind token test 2",
    "up_type":"可选参数，当要恢复逻辑删除的存储卷时可设置其值为recovery"
}
@apiUse CODE_VOL_POST_0
"""

"""
@api {delete} /api/v1.0/cinder/volumes/<volume_uuid>?logic=1/0 5 删除存储卷
@apiName delete
@apiGroup volume
@apiVersion 1.0.0
@apiDescription 删除
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} args
@apiUse CODE_VOL_POST_0
"""

"""
@api {post} /api/v1.0/cinder/snapshots 1 创建卷快照
@apiName post
@apiGroup snapshot
@apiVersion 1.0.0
@apiDescription 快照
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "name":"xxxx-yyyy", 
    "volume_uuid":"e9b35f2b-aeb2-491f-b537-2aab69864457",
    "description":"xxxx-yyyy snap for volume"
}
@apiUse CODE_SNAPSHOT_POST_0
"""
"""
@api {get} /api/v1.0/cinder/snapshots?page_num=<page_num>&page_size=<page_size> 2 获取快照列表
@apiName list
@apiGroup snapshot
@apiVersion 1.0.0
@apiDescription 存储
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParam {tuple} args
@apiUse CODE_SNAPSHOT_LIST_0
"""
"""
@api {get} /api/v1.0/cinder/snapshots/<snapshot_uuid> 3 获取快照详情
@apiName detail
@apiGroup snapshot
@apiVersion 1.0.0
@apiDescription 详情
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiUse CODE_SNAPSHOT_DETAIL_0
"""
"""
@api {put} /api/v1.0/cinder/snapshots/<snapshot_uuid> 4 更新快照
@apiName update
@apiGroup snapshot
@apiVersion 1.0.0
@apiDescription 更新
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
    "name":"xxxx-zzzzz",
    "description":"bind token test 2",
    "up_type":"可选参数，当要恢复逻辑删除的存储卷时可设置其值为recovery"
}
@apiUse CODE_SNAPSHOT_POST_0
"""
"""
@api {delete} /api/v1.0/cinder/snapshots/<snapshot_uuid>?logic=1/0 5 删除存储卷
@apiName delete
@apiGroup snapshot
@apiVersion 1.0.0
@apiDescription 删除
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} args
@apiUse CODE_SNAPSHOT_POST_0
"""
"""
@api {post} /api/v1.0/cinder/volumes 1 绑定卷到实例
@apiName post
@apiGroup attachment
@apiVersion 1.0.0
@apiDescription attachment
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} body
@apiParamExample body
{
     "server_uuid": server_uuid, 
     "volume_uuid": volume_uuid
}
@apiUse CODE_ATTACHMENT_POST_0
"""
"""
@api {delete} /api/v1.0/cinder/snapshots/<snapshot_uuid>?logic=1/0 2 解绑
@apiName delete
@apiGroup attachment
@apiVersion 1.0.0
@apiDescription 接触卷绑定
@apiPermission all
@apiParam {json} header {"token": "string"}
@apiParam {json} args
@apiUse CODE_ATTACHMENT_POST_0
"""