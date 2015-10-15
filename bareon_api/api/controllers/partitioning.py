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

import pecan
from pecan import rest

from bareon_api.common import utils
from bareon_api import models


LOG = utils.getLogger(__name__)


def get_or_404(model, obj_id):
    try:
        return model[obj_id]
    except (IndexError, KeyError):
        pecan.abort(404)


class SimpleRestController(rest.RestController):

    model = None
    collection = None

    @pecan.expose(template='json')
    def get_one(self, node_id, name):
        node_id = int(node_id)
        objs = get_or_404(self.collection, node_id)
        return get_or_404(objs, name)

    @pecan.expose(template='json')
    def get_all(self, node_id):
        node_id = int(node_id)
        return get_or_404(self.collection, node_id)

    @pecan.expose(template='json')
    def put(self, node_id, name):
        node_id = int(node_id)
        objs = get_or_404(self.collection, node_id)
        objs[name] = self.model(**pecan.request.json)
        return objs[name]

    @pecan.expose(template='json')
    def delete(self, node_id, name):
        node_id = int(node_id)
        objs = get_or_404(self.collection, node_id)
        get_or_404(objs, name)
        del objs[name]
        pecan.abort(204)


class FSController(SimpleRestController):
    model = models.FileSystem
    collection = models.FSS


class LVController(SimpleRestController):
    model = models.LogicalVolume
    collection = models.LVS


class PVController(SimpleRestController):
    model = models.PhysicalVolume
    collection = models.PVS


class VGController(SimpleRestController):
    model = models.VolumeGroup
    collection = models.LVS


class PartitioningCotroller(rest.RestController):

    @pecan.expose(template='json')
    def get(self, node_id):
        node_id = int(node_id)

        if node_id not in models.NODES:
            pecan.abort(404)

        fss = models.FSS[node_id].values()
        lvs = models.LVS[node_id].values()
        pvs = models.PVS[node_id].values()
        vgs = models.VGS[node_id].values()

        data = {
            'fss': fss,
            "lvs": lvs,
            'parteds': [
                {
                    'label': 'gpt',
                    'name': '/dev/vdc',
                    'partitions': [
                        {
                            'begin': 1,
                            'configdrive': False,
                            'count': 1,
                            'device': '/dev/vdc',
                            'end': 20000,
                            'flags': ['bios_grub'],
                            'guid': None,
                            'name': '/dev/vdc1',
                            'partition_type': 'primary',
                        },
                    ],
                },
            ],
            'pvs': pvs,
            'vgs': vgs,
        }
        return data


class DisksController(rest.RestController):

    @pecan.expose(template='json')
    def get_one(self, node_id, disk_id):
        node_id = int(node_id)
        # NOTE(prmtl): since this is just a list, lets not
        # force to use ids starting with 0
        disk_id = int(disk_id) - 1
        node_disks = get_or_404(models.DISKS, node_id)
        return get_or_404(node_disks, disk_id)

    @pecan.expose(template='json')
    def get_all(self, node_id):
        node_id = int(node_id)
        return get_or_404(models.DISKS, node_id)


class NodesController(rest.RestController):

    disks = DisksController()
    fss = FSController()
    lvs = LVController()
    pvs = PVController()
    vgs = VGController()
    partitioning = PartitioningCotroller()

    @pecan.expose(template='json')
    def get_one(self, node_id):
        node_id = int(node_id)
        return get_or_404(models.NODES, node_id)

    @pecan.expose(template='json')
    def put(self, node_id):
        node_id = int(node_id)
        models.NODES[node_id] = pecan.request.json
        return models.NODES[node_id]

    @pecan.expose(template='json')
    def get_all(self):
        return models.NODES.values()
