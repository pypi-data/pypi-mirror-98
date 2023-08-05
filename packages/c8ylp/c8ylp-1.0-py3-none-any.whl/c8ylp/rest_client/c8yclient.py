#  Copyright (c) 2021 Software AG, Darmstadt, Germany and/or its licensors
#
#  SPDX-License-Identifier: Apache-2.0
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import logging
import sys
from base64 import b64encode

import requests


class CumulocityClient:

    def __init__(self, hostname: str, tenant: str, user: str, password: str, tfacode: str):
        self.hostname = hostname
        self.tenant = tenant
        self.user = user
        self.password = password
        self.tfacode = tfacode
        self.session = requests.Session()
        self.url = f'https://{hostname}'
        self.logger = logging.getLogger(__name__)

    def retrieve_token(self):
        oauth_url = self.url + f'/tenant/oauth?tenant_id={self.tenant}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'PASSWORD',
            'username': self.user,
            'password': self.password,
            'tfa_code': self.tfacode
        }
        self.logger.debug(f'Sending requests to {oauth_url}')
        response = self.session.post(oauth_url,headers=headers,data=body)
        if response.status_code == 200:
            self.logger.debug(f'Authenticateion successful. Tokens have been updated {self.session.cookies.get_dict()}!')
        elif response.status_code == 401:
            self.logger.error(f'User {self.user} is not authorized to access Tenant {self.tenant} or TFA-Code is invalid.')
            sys.exit(1)
        return self.session

    def read_ext_Id(self, device, extype):
        identiy_url = self.url + f'/identity/externalIds/{extype}/{device}'
        #auth_string = f'{self.tenant}/{self.user}:{self.password}'
        #encoded_auth_string = b64encode(
        #    bytes(auth_string, 'utf-8')).decode('ascii')
        headers = {'Content-Type': 'application/json',
                    'X-XSRF-TOKEN': self.session.cookies.get_dict()['XSRF-TOKEN']
                   #'Authorization': 'Basic ' + encoded_auth_string
                  }
        self.logger.debug(f'Sending requests to {identiy_url}')
        response = self.session.get(identiy_url, headers=headers)
        self.logger.debug(f'Response received: {response}')
        ext_id = None
        if response.status_code == 200:
            ext_id = json.loads(response.content.decode('utf-8'))
        elif response.status_code == 401:
            self.logger.error(f'User {self.user} is not authorized to read Device Data of Device {device}')
            sys.exit(1)
        elif response.status_code == 404:
            self.logger.error(f'Device {device} not found!')
            # print(f'Device {device} not found!')
            sys.exit(1)
        else:
            self.logger.error(f'Error on retrieving device. Status Code {response.status_code}')
            # print(f'Error on retrieving device. Status Code {response.status_code}')
            sys.exit(1)
        return ext_id

    def read_mo(self, device, extype):
        ext_id = self.read_ext_Id(device, extype)
        mor_id = None
        mor = None
        if ext_id['managedObject']['id']:
            mor_id = ext_id['managedObject']['id']
        if mor_id:
            managed_object_url = self.url + f'/inventory/managedObjects/{mor_id}'
            #auth_string = f'{self.tenant}/{self.user}:{self.password}'
            #encoded_auth_string = b64encode(
            #    bytes(auth_string, 'utf-8')).decode('ascii')
            headers = {'Content-Type': 'application/json',
                       'X-XSRF-TOKEN': self.session.cookies.get_dict()['XSRF-TOKEN']
                       #'Authorization': 'Basic ' + encoded_auth_string
                      }
            self.logger.debug(f'Sending requests to {managed_object_url}')
            response = self.session.get(managed_object_url, headers=headers)
            self.logger.debug(f'Response received: {response}')
            if response.status_code == 200:
                mor = json.loads(response.content.decode('utf-8'))
                return mor
            elif response.status_code == 401:
                self.logger.error(f'User {self.user} is not authorized to read Device Data of Device {device}')
                sys.exit(1)
            elif response.status_code == 404:
                self.logger.error(f'Device {device} not found!')
                sys.exit(1)
            else:
                self.logger.error(f'Error on retrieving device. Status Code {response.status_code}')
                sys.exit(1)
            return mor

    def get_config_id(self, mor, config):
        access_list = mor['c8y_RemoteAccessList']
        device = mor['name']
        config_id = None
        for remote_access in access_list:
            if not remote_access['protocol'] == 'PASSTHROUGH':
                continue
            if config and remote_access['name'] == config:
                config_id = remote_access['id']
                break
            if not config:
                config_id = remote_access['id']
                break
        if not config_id:
            if config:
                self.logger.error(
                    f'Provided config name "{config}" for "{device}" was not found or not of type "PASSTHROUGH"')
                sys.exit(1)
            else:
                self.logger.error(f'No config of Type "PASSTHROUGH" has been found for device "{device}"')
                sys.exit(1)
        return config_id

    def get_device_id(self, mor):
        return mor['id']
