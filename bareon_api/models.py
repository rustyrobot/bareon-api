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
from copy import deepcopy
import random

from fuel_agent import objects
import requests

from bareon_api.common.config import CONF


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


def make_lv(vg):
    return {
        'kura': LogicalVolume(
            name='kura',
            size=69,
            vgname=vg.name,
        ),
        'kogut': LogicalVolume(
            name='kogut',
            size=96,
            vgname=vg.name,
        )
    }


def make_vg(pvs):
    return {
        'kurnik': VolumeGroup(
            name='kurnik',
            pvnames=[pv.name for pv in pvs],
        )
    }


def make_parted_and_partitions(disk):
    device = disk['device']
    partitions = {
        device: {
            '{0}1'.format(device): Partition(
                name='/dev/{0}1'.format(device),
                device='/dev/{0}'.format(device),
                count=1,
                partition_type='primary',
                begin=1,
                end=20000,
            )
        }
    }
    parted = {
        disk['device']: Parted(
            label='gpt',
            name='/dev/{0}'.format(disk['device']),
            partitions=partitions[device].values()
        )

    }
    return parted, partitions


def make_pv(disk):
    return {
        '{}1'.format(disk['device']): PhysicalVolume(
            name='/dev/{0}1'.format(disk['device']),
            metadatacopies=2,
            metadatasize=28,
        )
    }


def random_mac():
    mac = [
        0x00, 0x24, 0x81,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff)
    ]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def get_nodes_and_disks():

    # dummy way to check if this is a disk
    # it should be added as a info to the ohai data
    # during the discovery
    def is_disk(block_device):
        return block_device.get('vendor') in ['ATA', ]

    def get_nodes_discovery_data():
        discovery_url = 'http://{ip}:{port}/'.format(
            ip=CONF.discovery_host_ip,
            port=CONF.discovery_port,
        )
        resp = requests.get(discovery_url)
        return resp.json()

    def filter_disks(block_devices):
        disks = []
        for dev, info in block_devices.items():
            if is_disk(info):
                info['device'] = dev
                disks.append(info)
        return disks

    nodes = {}
    disks = {}
    for node in get_nodes_discovery_data():
        disks[node['mac']] = filter_disks(node.get('discovery', {}).get('block_device', {}))
        nodes[node['mac']] = {
            'disks': disks[node['mac']],
            # NOTE(prmtl): it really doesn't matter if it's mac
            # or anything as long as it is consistent between
            # services in PoC
            'id': node['mac'],
        }
    return nodes, disks


def generate_spaces(nodes, disks):
    fss = {}
    partitions = {}
    parteds = {}
    pvs = {}
    vgs = {}
    lvs = {}

    for mac in nodes.keys():
        if not DISKS[mac]:
            continue

        disk = DISKS[mac][0]

        parteds[mac], partitions[mac] = make_parted_and_partitions(disk)
        fss[mac] = deepcopy(FS)
        pvs[mac] = make_pv(disk)
        vgs[mac] = make_vg(pvs[mac].values())
        vg = vgs[mac].values()[0]
        lvs[mac] = make_lv(vg)

    return fss, partitions, parteds, pvs, vgs, lvs


NODES = {}
DISKS = {}

FSS = {}
PARTITIONS = {}
PARTEDS = {}
PVS = {}
VGS = {}
LVS = {}
NODES, DISKS = get_nodes_and_disks()

FSS, PARTITIONS, PARTEDS, PVS, VGS, LVS = generate_spaces(NODES, DISKS)
