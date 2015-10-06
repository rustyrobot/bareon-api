# -*- coding: utf-8 -*-

# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslotest import base
import pecan
import webtest

from bareon_api.api.controllers import root as root_ctrl


class TestCase(base.BaseTestCase):
    """Test case base class for all unit tests."""


class FunctionalTestCase(TestCase):

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        root = self.root
        config = {'app': {'root': root}}
        pecan.set_config(config, overwrite=True)
        self.app = webtest.TestApp(pecan.make_app(root))

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()
        pecan.set_config({}, overwrite=True)

    @property
    def root(self):
        return root_ctrl.V1Controller()
