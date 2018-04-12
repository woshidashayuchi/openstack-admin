** cinder(openstack)相关
*** 1 volume type的相关操作
        Cinder中的卷类型，是卷的一种标识，各个OpenStack的发行者可根据自身对系统的
    约束来定义卷类型的使用。G版的Cinder中与卷类型相关的两种资源：type和extra_specs，
    对应的API操作有：
        创建type
        查询（单个/批量）type
        删除type
        创建type的extra_specs
        删除type的extra_specs
        查询（单个/批量）type的extra_specs
        更新type的extra_specs

*** 2 使用命令行
        type-create         Create a new volume type.
        type-delete         Delete a specific volume type
        type-key            Set or unset extra_spec for a volume type.
        type-list           Print a list of available 'volume types'.
        extra-specs-list    Print a list of current 'volume types and extra specs'

*** 3 cinder基本命令
        http://blog.csdn.net/ztejiagn/article/details/8894895