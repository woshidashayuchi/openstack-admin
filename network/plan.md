搭建及使用K8s集群
1. 机器准备
host name	ip
master	192.168.6.39
node1	192.168.6.163
node2	192.168.6.94
2. 需要在所有机器上执行
2.1 关闭 && 禁用 防火墙、安装 && 启用 ntpd
#systemctl stop firewalld
#systemctl disable firewalld
#yum -y install ntp
#systemctl start ntpd
#systemctl enable ntpd

2.2 同步所有集群节点host文件
# cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.6.39 master 
192.168.6.163 node1
192.168.6.94 node2 
172.18.1.10     docker.hbg.io

#mkdir batch_edit_host
#cd batch_edit_host

#touch iplist.txt 
# cat iplist.txt 
192.168.6.39 master 
192.168.6.163 node1
192.168.6.94 node2

#touch synhost.sh 
# cat synhost.sh 
#!/bin/bash

user='root' //root还是少用的好，虽然都这么说，但还是喜欢直接用它
passwd='' //你的密码
for ip in $(awk -F' ' '{print $1}' iplist.txt); do
(
    /usr/bin/expect<<EOF
    set timeout -1
    spawn ssh-copy-id  $user@$ip
    expect {
    "*yes/no" { send "yes\r";exp_continue }
    "password:" { send "$passwd\r"}
    }
    expect eof

EOF
)
        name=`grep $ip iplist.txt| awk -F' ' '{print $2}'`
        ssh $user@$ip "/usr/bin/hostnamectl set-hostname $name"
        scp /etc/hosts $user@$ip:/etc/hosts
done

#chmod 777 *
./synhost.sh

3. Kubernetes Master节点的安装与配置
3.1 安装 etcd、docker和Kubernetes
yum -y install etcd  docker kubernetes
1
3.2 编辑配置文件/etc/etcd/etcd.conf
ETCD_NAME=default  
ETCD_DATA_DIR="/var/lib/etcd/default.etcd"  
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379";  
ETCD_ADVERTISE_CLIENT_URLS="http://localhost:2379";  

3.3 编辑配置文件/etc/kubernetes/config
# cat /etc/kubernetes/config

KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow-privileged=false"
KUBE_MASTER="--master=http://master:8080"

KUBE_MASTER=”–master=http://master:8080“是将Kubernetes的apiserver进程的服务地址告诉Kubernetes的controller-manager, scheduler和proxy进程。

3.4 编辑配置文件/etc/kubernetes/apiserver
# cat  /etc/kubernetes/apiserver
###
# kubernetes system config
#
# The following values are used to configure the kube-apiserver
#

# The address on the local server to listen to.
KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"

# The port on the local server to listen on.
KUBE_API_PORT="--port=8080"

# Port minions listen on
# KUBELET_PORT="--kubelet-port=10250"

# Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd-servers=http://127.0.0.1:2379"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# default admission control policies
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,SecurityContextDeny,ResourceQuota"

# Add your own!
KUBE_API_ARGS=""

KUBE_ADMISSION_CONTROL 要去掉 ServiceAccount, 
这些配置让apiserver进程在8080端口上监听所有网络接口，并告诉apiserver进程etcd服务的地址。

3.5 启动master
现在，启动Kubernetes Master节点上的etcd, docker, apiserver, controller-manager和scheduler进程并查看其状态：

# for SERVICES in etcd docker kube-apiserver kube-controller-manager kube-scheduler; do
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES
    done

3.6 在etcd里定义flannel网络配置
# etcdctl mk /atomic.io/network/config '{"Network":"172.17.0.0/16"}'
1
在随后Kubernetes的Node节点搭建和配置时，我们可以看到，etcd里的/atomic.io/network/config节点会被Node节点上的flannel用来创建网络的iptables 
现在我们可以使用kubectl get nodes命令来查看，当然，目前还没有Node节点加入到该Kubernetes集群，所以命令的执行结果是空的：

# kubectl get nodes
No resources found.

4. Kubernetes Node节点的安装与配置
4.1 安装 etcd、docker和Kubernetes
# yum -y install flannel docker kubernetes
1
4.2 编辑配置文件/etc/sysconfig/flanneld
# cat /etc/sysconfig/flanneld
# Flanneld configuration options  

# etcd url location.  Point this to the server where etcd runs
FLANNEL_ETCD_ENDPOINTS="http://master:2379"

# etcd config key.  This is the configuration key that flannel queries
# For address range assignment
FLANNEL_ETCD_PREFIX="/atomic.io/network"

# Any additional options that you want to pass
#FLANNEL_OPTIONS=""

配置信息告诉flannel进程etcd服务的位置以及在etcd上网络配置信息的节点位置

4.2 编辑配置文件/etc/kubernetes/config
对Node节点上的Kubernetes进行配置，两台Node节点上的配置文件/etc/kubernetes/config内容和Master节点相同，内容如下：

# cat /etc/kubernetes/config

KUBE_LOGTOSTDERR="--logtostderr=true"
KUBE_LOG_LEVEL="--v=0"
KUBE_ALLOW_PRIV="--allow-privileged=false"
KUBE_MASTER="--master=http://master:8080"

KUBE_MASTER=”–master=http://master:8080“是将Kubernetes的apiserver进程的服务地址告诉Kubernetes的controller-manager, scheduler和proxy进程。

4.3 编辑配置文件/etc/kubernetes/kubelet
两台Node节点上的/etc/kubernetes/kubelet配置文件内容略微有点不同,不同之处就是 
KUBELET_HOSTNAME=”–hostname-override=node1” 
KUBELET_HOSTNAME=”–hostname-override=node2”

 cat /etc/kubernetes/kubelet
###
# kubernetes kubelet (minion) config

# The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
KUBELET_ADDRESS="--address=0.0.0.0"

# The port for the info server to serve on
KUBELET_PORT="--port=10250"

# You may leave this blank to use the actual hostname
KUBELET_HOSTNAME="--hostname-override=node1"

# location of the api-server
KUBELET_API_SERVER="--api-servers=http://master:8080"

# pod infrastructure container
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest"

# Add your own!
KUBELET_ARGS=""

4.4 启动node
分别在两个Kubernetes Node节点上启动kube-proxy kubelet docker和flanneld进程并查看其状态： 
启动有可能有点慢，如果一直没反应可把 master 和 node1 node2 机器重启试试

# for SERVICES in kube-proxy kubelet docker flanneld; do
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES
done

5. 验证
在master上执行以下命令

# kubectl get nodes
NAME      STATUS    AGE
node1     Ready     10m
node2     Ready     5m

如果看到两个节点都是ready 证明部署成功。

6. 快速启动脚本
在master 可启动node 
代码如下：

# cat start_k8s_master.sh 
 for SERVICES in etcd docker kube-apiserver kube-controller-manager kube-scheduler; do
systemctl restart $SERVICES
systemctl enable $SERVICES
systemctl status $SERVICES
done

# cat start_k8s_nodes.sh 
#!/bin/bash  

#变量定义  
ip_array=("192.168.6.148" "192.168.6.149")  
user="root"  
remote_cmd="/root/start_k8s_node.sh"  

#本地通过ssh执行远程服务器的脚本  
for ip in ${ip_array[*]}  
do  
    if [ $ip = "192.168.1.1" ]; then  
        port="7777"  
    else  
        port="22"  
    fi  
    ssh -t -p $port $user@$ip "$remote_cmd"  
done  

在node的/root/下创建以下

# cat start_k8s_node.sh 
for SERVICES in kube-proxy kubelet docker flanneld; do
systemctl restart $SERVICES
systemctl enable $SERVICES
systemctl status $SERVICES
done