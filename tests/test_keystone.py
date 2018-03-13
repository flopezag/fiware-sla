#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

__author__ = 'fla'

import re
from unittest import TestCase
from core.keystone import Keystone


class TestAjustHours(TestCase):
    pass

    def test_get_token(self):
        """Check the response of the token in order to be sure that it is a valid token"""
        keystone = Keystone()

        returned_value = keystone.get_token()

        matchObj = re.match(r'[a-z0-9]*', returned_value, re.M | re.I)

        if matchObj:
            expected_value_len = 32

            self.assertEqual(expected_value_len, len(returned_value))
        else:
            self.assertFalse(False)
