# Copyright (C) 2016 Catalyst IT Ltd
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

from adjutantclient.common import base


class SignupManager(base.BaseManager):

    def post(self, username, email, project_name, setup_network):
        url = '/openstack/sign-up'
        fields = {
            'username': username,
            'email': email,
            'project_name': project_name,
            'setup_network': setup_network
        }
        return self.client.post(url, data=fields)
