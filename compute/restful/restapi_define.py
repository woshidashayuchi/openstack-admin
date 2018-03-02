# -*- coding: utf-8 -*-
# Author: wxf<wangxiaofeng1@hualala.com>
# Time: 2018/3/1 9:55
import json
from flask import request
from flask_restful import Resource
from common.logs import logging as log
from common.request_result import request_result
from manager.compute_manager import CloudhostManager, CloudhostRouteManager


class CloudhostApi(Resource):

    def __init__(self):
        self.manager = CloudhostManager()

    def post(self):
        '''
        #: A list of dictionaries holding links relevant to this server.
        links = resource.Body('links')

        access_ipv4 = resource.Body('accessIPv4')
        access_ipv6 = resource.Body('accessIPv6')
        #: A dictionary of addresses this server can be accessed through.
        #: The dictionary contains keys such as ``private`` and ``public``,
        #: each containing a list of dictionaries for addresses of that type.
        #: The addresses are contained in a dictionary with keys ``addr``
        #: and ``version``, which is either 4 or 6 depending on the protocol
        #: of the IP address. *Type: dict*
        addresses = resource.Body('addresses', type=dict)
        #: Timestamp of when the server was created.
        created_at = resource.Body('created')
        #: The flavor reference, as a ID or full URL, for the flavor to use for
        #: this server.
        flavor_id = resource.Body('flavorRef')
        #: The flavor property as returned from server.
        flavor = resource.Body('flavor', type=dict)
        #: An ID representing the host of this server.
        host_id = resource.Body('hostId')
        #: The image reference, as a ID or full URL, for the image to use for
        #: this server.
        image_id = resource.Body('imageRef')
        #: The image property as returned from server.
        image = resource.Body('image', type=dict)
        #: Metadata stored for this server. *Type: dict*
        metadata = resource.Body('metadata', type=dict)
        #: While the server is building, this value represents the percentage
        #: of completion. Once it is completed, it will be 100.  *Type: int*
        progress = resource.Body('progress', type=int)
        #: The ID of the project this server is associated with.
        project_id = resource.Body('tenant_id')
        #: The state this server is in. Valid values include ``ACTIVE``,
        #: ``BUILDING``, ``DELETED``, ``ERROR``, ``HARD_REBOOT``, ``PASSWORD``,
        #: ``PAUSED``, ``REBOOT``, ``REBUILD``, ``RESCUED``, ``RESIZED``,
        #: ``REVERT_RESIZE``, ``SHUTOFF``, ``SOFT_DELETED``, ``STOPPED``,
        #: ``SUSPENDED``, ``UNKNOWN``, or ``VERIFY_RESIZE``.
        status = resource.Body('status')
        #: Timestamp of when this server was last updated.
        updated_at = resource.Body('updated')
        #: The ID of the owners of this server.
        user_id = resource.Body('user_id')
        #: The name of an associated keypair
        key_name = resource.Body('key_name')
        #: The disk configuration. Either AUTO or MANUAL.
        disk_config = resource.Body('OS-DCF:diskConfig')
        #: Indicates whether a configuration drive enables metadata injection.
        #: Not all cloud providers enable this feature.
        has_config_drive = resource.Body('config_drive')
        #: The name of the availability zone this server is a part of.
        availability_zone = resource.Body('OS-EXT-AZ:availability_zone')
        #: The power state of this server.
        power_state = resource.Body('OS-EXT-STS:power_state')
        #: The task state of this server.
        task_state = resource.Body('OS-EXT-STS:task_state')
        #: The VM state of this server.
        vm_state = resource.Body('OS-EXT-STS:vm_state')
        #: A list of an attached volumes. Each item in the list contains at
           least
        #: an "id" key to identify the specific volumes.
        attached_volumes = resource.Body(
            'os-extended-volumes:volumes_attached')
        #: The timestamp when the server was launched.
        launched_at = resource.Body('OS-SRV-USG:launched_at')
        #: The timestamp when the server was terminated (if it has been).
        terminated_at = resource.Body('OS-SRV-USG:terminated_at')
        #: A list of applicable security groups. Each group contains keys for
        #: description, name, id, and rules.
        security_groups = resource.Body('security_groups')
        #: When a server is first created, it provides the administrator
           password.
        admin_password = resource.Body('adminPass')
        #: The file path and contents, text only, to inject into the server at
        #: launch. The maximum size of the file path data is 255 bytes.
        #: The maximum limit is The number of allowed bytes in the decoded,
        #: rather than encoded, data.
        personality = resource.Body('personality')
        #: Configuration information or scripts to use upon launch.
        #: Must be Base64 encoded.
        user_data = resource.Body('OS-EXT-SRV-ATTR:user_data')
        #: Enables fine grained control of the block device mapping for an
        #: instance. This is typically used for booting servers from volumes.
        block_device_mapping = resource.Body('block_device_mapping_v2')
        #: The dictionary of data to send to the scheduler.
        scheduler_hints = resource.Body('OS-SCH-HNT:scheduler_hints',
                                        type=dict)
        #: A networks object. Required parameter when there are multiple
        #: networks defined for the tenant. When you do not specify the
        #: networks parameter, the server attaches to the only network
        #: created for the current tenant.
        networks = resource.Body('networks')
        #: The hypervisor host name. Appears in the response for administrative
        #: users only.
        hypervisor_hostname = resource.Body(
            'OS-EXT-SRV-ATTR:hypervisor_hostname')
        #: The instance name. The Compute API generates the instance name from
           the
        #: instance name template. Appears in the response for administrative
           users
        #: only.
        instance_name = resource.Body('OS-EXT-SRV-ATTR:instance_name')
        '''
        try:
            parameters = json.loads(request.get_data())

        except Exception, e:
            log.error('parameters error, reason is: %s' % e)
            return request_result(101)

        instance_name = parameters.get('instance_name')
        availability_zone = parameters.get('availability_zone')
        instance_num = parameters.get('instance_num')
        image = parameters.get('image')
        instance_cpu = parameters.get('instance_cpu')
        instance_mem = parameters.get('instance_mem')
        instance_type = parameters.get('instance_type')
        net = parameters.get('net')
        net_interface = parameters.get('net_interface')
        flavor_id = parameters.get('flavor_id')
        security_groups = parameters.get('security_groups')
        keypair = parameters.get('keypair')

        result = self.manager.create(instance_name=instance_name,
                                     availability_zone=availability_zone,
                                     instance_num=instance_num,
                                     image=image,
                                     instance_cpu=instance_cpu,
                                     instance_mem=instance_mem,
                                     instance_type=instance_type,
                                     net=net,
                                     net_interface=net_interface,
                                     flavor_id=flavor_id,
                                     security_groups=security_groups,
                                     keypair=keypair)
        log.info('create result is: %s' % result)
        return result

    def get(self):
        result = self.manager.list()
        return result


class ClouhostRouteApi(Resource):

    def __init__(self):
        self.manager = CloudhostRouteManager()

    def get(self, cloudhost_uuid):
        result = self.manager.detail(cloudhost_uuid)
        return result

    def delete(self, cloudhost_uuid):
        result = self.manager.delete(cloudhost_uuid)
        return result

    def put(self, cloudhost_uuid):
        result = self.manager.update(cloudhost_uuid)
        return result
