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

import logging
from rsync_backup_cluster.config import load_config
from rsync_backup_cluster.log import setup_log
from rsync_backup_cluster.worker.app import load_app
from rsync_backup_cluster.utils import get_parser, which
import sys


LOG = logging.getLogger(__name__)


def main():
    parser = get_parser()
    args = parser.parse_args()

    setup_log(args.debug, args.logfile)

    LOG.info('starting rsync-backup-worker')

    rsync_path = which('rsync')

    if rsync_path is None:
        LOG.error('rsync command not found on worker')
        sys.exit(1)

    LOG.debug('loading configuration file %s' % (args.config))
    config = load_config(args.config, component='worker')

    worker = load_app(config)
    worker.work()
