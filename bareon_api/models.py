# -*- coding: utf-8 -*-

#    Copyright 2015 Mirantis, Inc.
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

EXAMPLE_NODE_ID = 1


DISKS = {
    EXAMPLE_NODE_ID: [
        {'disk': 'disk/by-path/pci-0000:00:0b.0-virtio-pci-virtio2',
         'extra': ['disk/by-id/virtio-8140d936d3ee4b04a6b5'],
         'model': None,
         'name': 'vdc',
         'removable': '0',
         'size': 53687091200},
        {'disk': 'disk/by-path/pci-0000:00:0a.0-virtio-pci-virtio1',
         'extra': ['disk/by-id/virtio-eaa8cf22606c41868089'],
         'model': None,
         'name': 'vdb',
         'removable': '0',
         'size': 53687091200},
        {'disk': 'disk/by-path/pci-0000:00:09.0-virtio-pci-virtio0',
         'extra': ['disk/by-id/virtio-6a363e572c9e43e49ad7'],
         'model': None,
         'name': 'vda',
         'removable': '0',
         'size': 53687091200}
    ]
}


NODES = {
    EXAMPLE_NODE_ID: {
        'host': 'some-host',
        'ssh_key': 'some-ssh-key',
        'disks': DISKS[EXAMPLE_NODE_ID],
    },
}
