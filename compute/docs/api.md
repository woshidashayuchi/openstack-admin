## 接口与参数说明
   ### 1 创建云主机
   ###   参考参数：没有networks的情况下，需要环境只有一个网络，op会自动关联
         {"instance_name":"aaa",
          "availability_zone":"nova",
          "instance_num":1,
          "instance_cpu":0.5,
          "instance_mem":1,
          "flavor_id":"2",
          "image":"aafad1da-b3e8-4384-ae6a-93829cde4d33",
          "security_groups":[{"name": "default"}],
          "keypair":"testkey"}