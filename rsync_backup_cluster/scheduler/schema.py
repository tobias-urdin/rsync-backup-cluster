# -*- coding: utf-8 -*-

# Copyright (C) 2019 Tobias Urdin
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

from voluptuous import Schema, Invalid, Optional
import os


def validate_steps(value):
    if not isinstance(value, int):
        raise Invalid('steps must be a integer')

    if value < 0:
        raise Invalid('steps must be zero or above')

    return value


def validate_path(value):
    if not isinstance(value, dict):
        raise Invalid('must be a dict')

    if 'path' not in value:
        raise Invalid('dict must contain path')

    path = value.get('path')

    if not os.path.isdir(path):
        raise Invalid('%s must be a existing directory' % path)

    if not os.path.isabs(path):
        raise Invalid('%s must be a absolute path' % path)

    if 'mount' in value:
        mount = value.get('mount')

        if not isinstance(mount, bool):
            raise Invalid('mount must be a boolean')

        if mount and not os.path.ismount(path):
            raise Invalid('%s must be a mount' % path)

    return value


def validate_exclusions(value):
    if not isinstance(value, list):
        raise Invalid('exclusions must be a list')

    for val in value:
        if not isinstance(val, str):
            raise Invalid('all exclusions must be strings')

    return value


def validate_options(value):
    if not isinstance(value, list):
        raise Invalid('options must be a list')

    for val in value:
        if not isinstance(val, str):
            raise Invalid('all options must be strings')

        if not val.startswith('-'):
            raise Invalid('option %s must start with a dash' % val)

    return value


def validate_allowed_returncodes(value):
    if not isinstance(value, list):
        raise Invalid('allowed_returncodes must be a list')

    for val in value:
        if not isinstance(val, int):
            raise Invalid('all allowed_returncodes must be integers')

    return value


job_schema = Schema({
    'source': validate_path,
    'destination': validate_path,
    Optional('exclusions'): validate_exclusions,
    Optional('options'): validate_options,
    Optional('steps'): validate_steps,
    Optional('allowed_returncodes'): validate_allowed_returncodes,
    Optional('queue'): str
})
