# Copyright 2004-2021 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# This file contains internal functions that are useful in test code
#
# Some useful functions are:
#  - patch_clientutils:
#    Decorator to be applied to test functions. This will patch the openstack
#    client libraries to return some default values

from __future__ import absolute_import

import os
import sys
import uuid
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

import heatclient
import six
from six import StringIO
from six.moves import filter
from six.moves.mock import Mock, PropertyMock, patch

from clusterondemand import const
from clusterondemand.command_runner import sys_argv
from clusterondemandconfig import BCM_VERSION, global_configuration, load_configuration_for_command
from clusterondemandconfig.determine_invoked_command import determine_invoked_command


def ipxe_plain_eth0():
    m = Mock(
        spec="",
        status=u"active",
        tags=[],
        container_format=u"bare",
        min_ram=0,
        updated_at=u"2018-03-17T21:46:33",
        visibility=u"public",
        owner=u"3b9bd8793720479f8bb341edc808a499",
        file=u"/v2/images/bba054ed-3ac7-4fcd-9401-ca115cae2eba/file",
        min_disk=0,
        virtual_size=None,
        id=u"bba054ed-3ac7-4fcd-9401-ca115cae2eba",
        size=8388608,
        checksum=u"3661bd33484e39c4e9d75d15fa61b0ea",
        created_at=u"2018-03-17T21:46:32",
        disk_format=u"raw",
        protected=False,
        direct_url=u"rbd://yadayada",
        schema=u"/v2/schemas/image"
    )
    # Weird trick because Mock uses the name attribute
    type(m).name = PropertyMock(return_value="iPXE-plain-eth0")
    return m


def bcmh_centos7u4():
    m = Mock(
        spec="",
        status=u"active",
        bcm_image_revision=u"278",
        tags=[u"MesosFailed",
              u"AzureExtensionOK",
              u"OpenStackExtensionOK",
              u"BasicTestsOK",
              u"AWSExtensionOK",
              u"OpenStackTestsFailed"],
        container_format=u"bare",
        min_ram=0,
        updated_at=u"2018-04-10T15:00:49",
        bcm_api_hash=u"e81c77691ab1cfc4bf7baffe7cd8079c",
        owner=u"962ab1fc6e4f4faea89dcfcb796d5d35",
        visibility=u"public",
        file=u"/v2/images/4c75d9eb-62c9-40b0-865c-eeba52d44b39/file",
        min_disk=0,
        bcm_image_type=u"headnode",
        virtual_size=None,
        id=u"4c75d9eb-62c9-40b0-865c-eeba52d44b39",
        bcm_distro=u"centos7u4",
        size=14289993728,
        bcm_cmd_revision=u"132465",
        bcm_image_id=f"centos7u4-{BCM_VERSION}",
        bcm_cmd_hash=u"af65b9f1435",
        bcm_cluster_tools_hash=u"ce3b53adad",
        bcm_cm_setup_hash=u"67557b1d0d2",
        bcm_cloud_type=u"openstack",
        bcm_created_at=u"2018-04-08T23:41:06",
        created_at=u"2018-04-08T23:41:06",
        disk_format=u"raw",
        protected=False,
        bcm_package_groups=u"",
        checksum=u"75f90cec8caf62f4fa1ba1111fa0c9f1",
        direct_url=u"rbd://yadayada",
        bcm_version=BCM_VERSION,
        schema=u"/v2/schemas/image"
    )
    type(m).name = PropertyMock(return_value=u"bcmh-centos7u4")
    return m


def ipxe_caas():
    m = Mock(
        spec="",
        status=u"active",
        tags=[],
        container_format=u"bare",
        min_ram=0,
        min_disk=0,
        visibility=u"public",
        id="c5c16f40-166c-4015-92c5-cc834534dd67",
        size=8388608,
        disk_format=u"raw",
        protected=False,
        created_at=u"2018-04-08T23:41:06",
        direct_url=u"rbd://yadayada",
        schema=u"/v2/schemas/image"
    )
    # Weird trick because Mock uses the name attribute
    type(m).name = PropertyMock(return_value="ipxe-caas")
    return m


def ipxe_plain_eth1():
    m = Mock(
        spec="",
        status=u"active",
        tags=[],
        container_format=u"bare",
        min_ram=0,
        min_disk=0,
        visibility=u"public",
        id="96db1397-7a50-4db5-b096-9698af282397",
        size=8388608,
        disk_format=u"raw",
        protected=False,
        created_at=u"2018-04-08T23:41:06",
        direct_url=u"rbd://yadayada",
        schema=u"/v2/schemas/image"
    )
    # Weird trick because Mock uses the name attribute
    type(m).name = PropertyMock(return_value="iPXE-plain-eth1")
    return m


FLAVOR_M1_XSMALL = Mock(get_keys=Mock(return_value={}),
                        disk=0,
                        ephemeral=0)
type(FLAVOR_M1_XSMALL).name = PropertyMock(return_value="m1.xsmall")

FLAVOR_M1_MEDIUM = Mock(get_keys=Mock(return_value={}),
                        disk=0,
                        ephemeral=0)
type(FLAVOR_M1_MEDIUM).name = PropertyMock(return_value="m1.medium")

FLAVOR_BAREMETAL = Mock(get_keys=Mock(return_value={
                        "cpu_arch": "x86_64"
                        }),
                        disk=0,
                        ephemeral=0)
type(FLAVOR_BAREMETAL).name = PropertyMock(return_value="baremetal")

FLAVOR_COD_MEDIUM = Mock(get_keys=Mock(return_value={}),
                         ram=4096,
                         vcpus=2,
                         disk=0,
                         ephemeral=0,
                         id="2e631454-bf1b-4f3b-b9c2-c15a11058784")
type(FLAVOR_COD_MEDIUM).name = PropertyMock(return_value="cod.medium")

FLAVOR_COD_XSMALL = Mock(get_keys=Mock(return_value={}),
                         ram=1024,
                         vcpus=1,
                         disk=0,
                         ephemeral=0,
                         id="a39c2730-6988-11e8-adc0-fa7ae01bbebc")
type(FLAVOR_COD_XSMALL).name = PropertyMock(return_value="cod.xsmall")

TESTNET = {
    "status": "ACTIVE",
    "id": "660e44f0-5037-4231-b9ff-35009d33b041",
    "name": "zz-cod-external"
}

TESTSUBNET = {
    "name": "zz-cod-external-sn",
    "id": "4dc39dda-68ba-11e8-adc0-fa7ae01bbebc",
    "cidr": "192.168.200.0/24",
    "ip_version": 4,
    "network_id": TESTNET["id"],
    "gateway_ip": "192.168.200.254",
    "enable_dhcp": True,
    "allocation_pools": [{"start": "192.168.200.128", "end": "192.168.200.253"}],
    "dns_nameservers": ["8.8.8.8"],
}

TESTROUTER = {
    "name": "zz-cod-router",
    "id": "d01063ee-92ee-426a-8d11-5e792a52b952",
    "external_gateway_info": {
        "network_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
    },
}

TESTPORT = {
    "device_id": TESTROUTER["id"],
    "fixed_ips": [
        {
            "subnet_id": TESTSUBNET["id"],
            "ip_address": TESTSUBNET["gateway_ip"],
        }
    ]
}


def patch_neutron(fake_networks=None, fake_subnets=None, fake_routers=None, fake_ports=None):
    def decorator_neutron(func):
        @patch("clusterondemandopenstack.clientutils.get_neutron_client")
        def wrapper_neutron(self, get_neutron_client):
            def return_networks_list(name=None):
                if fake_networks is None:
                    return {"networks": []}
                else:
                    return {
                        "networks": [network for network in fake_networks if name == network["name"] or name is None]
                    }

            def return_subnets_list(network_id=None):
                if fake_subnets is None:
                    return {"subnets": []}
                else:
                    return {
                        "subnets": [subnet for subnet in fake_subnets if subnet["network_id"] == network_id or
                                    network_id is None]
                    }

            def return_routers_list(name=None):
                if fake_routers is None:
                    return {"routers": []}
                else:
                    return {
                        "routers": [router for router in fake_routers if name == router["name"] or name is None]
                    }

            def return_ports_list(device_id=None):
                if fake_routers is None:
                    return {"ports": []}
                else:
                    return {
                        "ports": [port for port in fake_ports if device_id == port["device_id"] or port is None]
                    }

            def return_create_network(network):
                return {
                    "network": {
                        "name": network["network"]["name"]
                    }
                }

            def return_create_subnet(subnets):
                return {
                    "subnets": [
                        {
                            "name": subnets["subnets"][0]["name"]
                        }
                    ]
                }

            def return_create_router(router):
                return {
                    "router": {
                        "name": router["router"]["name"],
                        "id": "8d3e0d19-d088-46c0-b6da-9a4164286d75",
                    }
                }

            def return_add_interface_router(router_id, subnet_id):
                return

            get_neutron_client.return_value = Mock(list_networks=return_networks_list,
                                                   list_subnets=return_subnets_list,
                                                   list_routers=return_routers_list,
                                                   list_ports=return_ports_list,
                                                   create_network=return_create_network,
                                                   create_subnet=return_create_subnet,
                                                   create_router=return_create_router,
                                                   add_interface_router=return_add_interface_router,
                                                   )
            func(self)

        return wrapper_neutron
    return decorator_neutron


def patch_clientutils(func):
    """
    Return decorator to be used in a test method.

    This will override the clientutil functions to return Mocked objects.
    The current version is very simple, and will have to be improved in order to test
    more complex things.
    """
    @patch_neutron(fake_networks=[TESTNET], fake_subnets=[TESTSUBNET], fake_routers=[TESTROUTER], fake_ports=[TESTPORT])
    @patch("clusterondemandopenstack.clientutils.get_cinder_client")
    @patch("clusterondemandopenstack.clientutils.get_heat_client")
    @patch("clusterondemandopenstack.clientutils.get_glance_client")
    @patch("clusterondemandopenstack.clientutils.get_nova_client")
    def wrapper(self, get_nova_client, get_glance_client,
                get_heat_client, get_cinder_client, *args, **kwargs):
        def return_images_list(filters=None, page_size=25):
            filters = {} if filters is None else filters
            images_list = [ipxe_plain_eth0(), ipxe_plain_eth1(), bcmh_centos7u4(), ipxe_caas()]

            def filter_func(image):
                for k, v in six.iteritems(filters):
                    if k == "tag":
                        if v[0] not in image.tags:
                            return False
                        else:
                            continue

                    if not hasattr(image, k):
                        return False
                    if v not in getattr(image, k):
                        return False
                return True

            return iter(filter(filter_func, images_list))

        def return_servers_list(**kwargs):
            return []

        def return_flavors_list():
            flavors = [FLAVOR_M1_XSMALL, FLAVOR_M1_MEDIUM, FLAVOR_BAREMETAL,
                       FLAVOR_COD_MEDIUM, FLAVOR_COD_XSMALL]
            return flavors

        def return_volume_types():
            special_vol = Mock()
            type(special_vol).name = PropertyMock(return_value="special_vol")

            default_vol = Mock()
            type(default_vol).name = PropertyMock(return_value="default")

            return [special_vol, default_vol]

        def return_stacks_get_raise_exception_meaning_lack_of_stack(name):
            raise heatclient.exc.HTTPNotFound(
                "Stack not found (this is a custom "
                "string, should not matter for the tests)")

        get_glance_client.return_value = Mock(images=Mock(list=return_images_list))

        get_heat_client.return_value = \
            Mock(stacks=Mock(get=return_stacks_get_raise_exception_meaning_lack_of_stack))

        get_nova_client.return_value = Mock(servers=Mock(list=return_servers_list),
                                            flavors=Mock(list=return_flavors_list))

        get_cinder_client.return_value = Mock(volume_types=Mock(list=return_volume_types))

        func(self)

    return wrapper


class capture_output(object):
    """
    Capture stdout and make it available as StringIO.

    It can be used as a context manager:
    ```
    with capture_output() as output:
        pass
    ```

    or as a decorator:
    ```
    @capture_output()
    def f(arg1, arg2, output):
        pass
    f(arg1, arg2)
    ```
    """

    def __enter__(self):
        self.old_out, sys.stdout = sys.stdout, StringIO()
        return sys.stdout

    def __exit__(self, exception_type, exception_value, traceback):
        sys.stdout = self.old_out

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, output=sys.stdout, **kwargs)
        return wrapper


class environ(object):
    """Temporarily replace certain mappings of os.environ."""
    def __init__(self, new_mapping):
        self.old_mapping = {
            key: os.environ.get(key) for (key, _) in six.iteritems(new_mapping)
        }
        self.new_mapping = new_mapping

    def __enter__(self):
        for key, value in six.iteritems(self.new_mapping):
            os.environ[key] = value

    def __exit__(self, _exception_type, _exception_value, _traceback):
        for key, value in six.iteritems(self.old_mapping):
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value

    def __call__(self, func):
        def wrapper(_self, *args, **kwargs):
            with self:
                return func(_self, *args, **kwargs)
        return wrapper


def run_command(cli, command_context):
    with sys_argv(cli):
        command, clean_sys_argv = determine_invoked_command(command_context)

    with sys_argv(clean_sys_argv):
        config = load_configuration_for_command(command, system_config_files=[], enforcing_config_files=[])
    with global_configuration(config):
        command.run_command()


def gen_cod_stack(head_a_ip=None, head_b_ip=None, head_a_uuid=None, head_b_uuid=None, **kwargs):
    """Generate a Mock COD stack object.

    Any argument in kwargs will be used as attributes
    The required fields that were not specified will be set to values to make it a valid cod stack
    """
    stack = Mock()
    if not kwargs.get("stack_name"):
        kwargs["stack_name"] = "clustername"
    if not kwargs.get("id"):
        kwargs["id"] = str(uuid.uuid4())
    if not kwargs.get("tags"):
        kwargs["tags"] = []

    # Append tags to make it a valid cod
    required_tags = [
        const.COD_TAG,
        const.COD_TOOL_VERSION_TAG + "=" + str(const.COD_TOOL_VERSION)
    ]
    for tag in required_tags:
        if tag not in kwargs["tags"]:
            kwargs["tags"].append(tag)

    stack.outputs = []
    if head_a_ip is not None:
        stack.outputs.append({"output_key": "head_a_floating_ip", "output_value": head_a_ip})
    if head_b_ip is not None:
        stack.outputs.append({"output_key": "head_b_floating_ip", "output_value": head_b_ip})
    if head_a_uuid is not None:
        stack.outputs.append({"output_key": "head_a_uuid", "output_value": head_a_uuid})
    if head_b_uuid is not None:
        stack.outputs.append({"output_key": "head_b_uuid", "output_value": head_b_uuid})

    # Set attributes
    for attr, value in six.iteritems(kwargs):
        setattr(stack, attr, value)

    return stack


def decorate_test_methods_with(decorator):
    """Decorator for a TestCase class. Wrap every test method with the `decorator` parameter."""
    def class_decorator(decorated_class):
        for (name, member) in six.iteritems(decorated_class.__dict__):
            if name.startswith("test_") and callable(member):
                setattr(decorated_class, name, decorator(member))
        return decorated_class
    return class_decorator


@contextmanager
def temporary_file(content):
    """Creates a temporary file with a certain content."""
    with NamedTemporaryFile(mode="w+") as temp:
        temp.write(content)
        temp.flush()
        yield temp
