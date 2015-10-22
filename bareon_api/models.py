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
from fuel_agent import objects
from copy import deepcopy


class JsonifyMixin(object):
    """Allows to easily serialize fuel_agent's objects to JSON"""

    def __json__(self):
        return self.to_dict()


class FileSystem(JsonifyMixin, objects.FS):
    pass


class LogicalVolume(JsonifyMixin, objects.LV):
    pass


class Parted(JsonifyMixin, objects.Parted):
    pass


class Partition(JsonifyMixin, objects.Partition):
    pass


class PhysicalVolume(JsonifyMixin, objects.PV):
    pass


class VolumeGroup(JsonifyMixin, objects.VG):
    pass


EXAMPLE_NODE_ID = 1


DISKS_TEMPLATE = {
    'disk': 'disk/by-path/pci-0000:00:0b.0-virtio-pci-virtio2',
    'extra': ['disk/by-id/virtio-8140d936d3ee4b04a6b5'],
    'model': None,
    'name': 'sda',
    # TODO this information mustn't be hardcoded in the agent [1],
    # instead discovery should provide all required data as is
    # so after that service can determine which device is really
    # removable
    #
    # [1] https://github.com/openstack/fuel-nailgun-agent/blob
    #                       /abab45cf8c7344d43acd3858c02d7a648ef7fee6/agent#L41-L52
    'removable': '0',
    # TODO figure out what we should use internally, probably
    # megabytes, even if discovery provides bytes [1]
    #
    # [1] https://github.com/openstack/fuel-web/blob
    #                       /93a42ebbde6ecf8c5e36cdec06e59aa70e5f044b/nailgun/nailgun/objects/node.py#L349-L360
    'size': 40000
}


FS = {
    # ???(prmtl) now we identify file system by lablel
    # but should be considered to find a better way
    'kogut': FileSystem(
        device='/dev/kurnik/kogut',
        fs_label='kogut',
        fs_type='ext2',
        mount='/tmp/kogutek'
    ),
}

LV = {
    'kura': LogicalVolume(
        name='kura',
        size=69,
        vgname='kurnik'
    ),
    'kogut': LogicalVolume(
        name='kogut',
        size=96,
        vgname='kurnik'
    )
}

VG = {
    'kurnik': VolumeGroup(
        name='kurnik',
        pvnames=[
            '/dev/vdc1',
        ],
    )
}

PARTITION = {
    'vdc': {
        'vdc1': Partition(
            name='/dev/vdc1',
            device='/dev/vdc',
            count=1,
            partition_type='primary',
            begin=1,
            end=20000,
        )
    }
}

PARTED = {
    'vdc': Parted(
        label='gpt',
        name='/dev/vdc',
        partitions=PARTITION['vdc'].values()
    )
}


PV = {
    'vdc1': PhysicalVolume(
        name='/dev/vdc1',
        metadatacopies=2,
        metadatasize=28,
    )
}


def generate_nodes_disks(count):
    nodes = {}
    disks = {}
    for i in xrange(count):
        # Start indexes from 1
        idx = i + 1;

        disks[idx] = [deepcopy(DISKS_TEMPLATE)]
        nodes[idx] = {
            'host': 'some-host',
            'ssh_key': 'some-ssh-key',
            'disks': disks[idx],
        }

    return nodes, disks


def generate_spaces(nodes):
    fss = {}
    partitions = {}
    parteds = {}
    pvs = {}
    vgs = {}
    lvs = {}

    for idx in nodes.keys():
        fss[idx] = deepcopy(FS)
        partitions[idx] = deepcopy(PARTITION)
        parteds[idx] = deepcopy(PARTED)
        pvs[idx] = deepcopy(PV)
        vgs[idx] = deepcopy(VG)
        lvs[idx] = deepcopy(LV)

    return fss, partitions, parteds, pvs, vgs, lvs


NODES, DISKS = generate_nodes_disks(2)

FSS, PARTITIONS, PARTEDS, PVS, VGS, LVS = generate_spaces(NODES)
