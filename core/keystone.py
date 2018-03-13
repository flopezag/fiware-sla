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

import requests
import json
import sys
from config.settings import OS_PROJECT_ID, OS_USERNAME, OS_PASSWORD, OS_AUTH_URL, OS_MONASCA_URL
from config.log import logger


__author__ = 'fla'


class Keystone:
    def __init__(self):
        self.url = OS_AUTH_URL + '/v3/auth/tokens'

        self.payload = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": OS_USERNAME,
                            "password": OS_PASSWORD,
                            "domain": {
                                "name": "default"
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "id": OS_PROJECT_ID
                    }
                }
            }
        }

        self.headers = {'Content-Type': 'application/json'}

    def get_token(self):
        logger.info('Requesting token to Keytone...')

        try:
            r = requests.post(self.url, json=self.payload,
                              headers=self.headers)

            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logger.error("Http Error: {}".format(errh))
            sys.exit(1)
        except requests.exceptions.ConnectionError as errc:
            logger.error("Error Connecting: {}".format(errc))
            sys.exit(1)
        except requests.exceptions.Timeout as errt:
            logger.error("Timeout Error: {}".format(errt))
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            logger.error("OOps: Something Else: {}".format(err))
            sys.exit(1)

        token = r.headers['X-Subject-Token']

        logger.info('Token obtained, status code: {}'.format(r.status_code))

        return token


if __name__ == "__main__":
    keystone = Keystone()

    token = keystone.get_token()

    print(token)
