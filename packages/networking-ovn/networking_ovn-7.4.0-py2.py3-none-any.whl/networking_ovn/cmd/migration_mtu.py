# Copyright 2018 Red Hat, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys

from openstack import connection

# TODO(dalvarez): support also GRE
GENEVE_TO_VXLAN_OVERHEAD = 8


def get_connection():
    user_domain_id = os.environ.get('OS_USER_DOMAIN_ID', 'default')
    project_domain_id = os.environ.get('OS_PROJECT_DOMAIN_ID', 'default')
    conn = connection.Connection(auth_url=os.environ['OS_AUTH_URL'],
                                 project_name=os.environ['OS_PROJECT_NAME'],
                                 username=os.environ['OS_USERNAME'],
                                 password=os.environ['OS_PASSWORD'],
                                 user_domain_id=user_domain_id,
                                 project_domain_id=project_domain_id)
    return conn


def verify_network_mtu():
    print("Verifying the tenant network mtu's")
    conn = get_connection()
    success = True
    for network in conn.network.networks():
        if network.provider_physical_network is None and (
            network.provider_network_type == 'vxlan') and (
                'adapted_mtu' not in network.tags):
            print("adapted_mtu tag is not set for the Network "
                  "[" + str(network.name) + "]")
            success = False

    if success:
        print("All the networks are set to expected mtu value")
    else:
        print("Some tenant networks need to have their MTU updated to a "
              "lower value.")
    return success


def update_network_mtu():
    print("Updating the tenant network mtu")
    conn = get_connection()
    for network in conn.network.networks():
        try:
            if network.provider_physical_network is None and (
                    network.provider_network_type == 'vxlan') and (
                        'adapted_mtu' not in network.tags):
                print("Updating the mtu and the tag 'adapted_mtu"
                      " of the network - " + str(network.name))
                new_tags = list(network.tags)
                new_tags.append('adapted_mtu')
                conn.network.update_network(
                    network,
                    mtu=int(network.mtu) - GENEVE_TO_VXLAN_OVERHEAD)
                conn.network.set_tags(network, new_tags)
        except Exception as e:
            print("Exception occured while updating the MTU:" + str(e))
            return False
    return True


def print_usage():
    print('Invalid options:')
    print('Usage: %s <update|verify> mtu' % sys.argv[0])


def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    retval = 1
    if sys.argv[1] == "update" and sys.argv[2] == "mtu":
        if update_network_mtu():
            retval = 0
    elif sys.argv[1] == "verify" and sys.argv[2] == "mtu":
        if verify_network_mtu():
            retval = 0
    else:
        print_usage()

    sys.exit(retval)


if __name__ == "__main__":
    main()
