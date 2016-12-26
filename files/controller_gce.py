# !/usr/bin/env python3
# Copyright (C) 2016  Qrama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406
import os
from subprocess import check_output, check_call
import yaml


class Token(object):
    def __init__(self, url, username, password):
        self.type = 'gce'
        self.supportlxd = True
        self.url = url


def create_controller(name, region, credentials):
    check_call(['juju', 'add-credential', 'google', '-f', create_credentials_file(credentials)])
    output = check_output(['juju', 'bootstrap', 'gce/{}'.format(region), name])
    return output


def get_supported_series():
    return ['precise', 'trusty', 'xenial', 'yakkety']


def create_credentials_file(filepath):
    path = '/tmp/credentials.yaml'
    data = {'credentials': {'google': {os.environ.get('JUJU_ADMIN_USER'): {'auth-type': 'jsonfile',
                                                                           'file': filepath}}}}
    with open(path, 'w') as dest:
        yaml.dump(data, dest, default_flow_style=True)
    return path
