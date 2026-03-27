# Copyright 2026 Thibault Poignonec
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pkgutil

from rocker.extensions import RockerExtension
from rocker.em import empy_expand

SUPPORTED_ETHERLAB_VERSIONS = [
    'stable-1.5',
    'none'
]
DEFAULT_ETHERLAB_VERSION = SUPPORTED_ETHERLAB_VERSIONS[0]
DEFAULT_ETHERCAT_MASTER_IDX = 0

def has_etherlab():
    """
    Detect if EtherLab is available on the host system.

    We check these device files rather than searching for libraries or
    executables:
    - /etc/init.d/ethercat is the init script for EtherLab
    - /etc/sysconfig/ethercat is the configuration file for EtherLab

    Returns:
        bool: True if EtherLab is detected, False otherwise.
    """
    return os.path.exists('/etc/init.d/ethercat') and \
        os.path.exists('/etc/sysconfig/ethercat2')


class EtherLab(RockerExtension):

    @staticmethod
    def get_name():
        return 'etherlab'

    def validate_environment(self, cliargs, parser):
        if cliargs.get('etherlab'):
            if not has_etherlab():
                parser.error(
                    "--etherlab was specified, but no EtherLab installation "
                    "was detected on the host.\n"
                    "The container may not have access to EtherCAT hardware.")

    def get_snippet(self, cliargs):
        if cliargs.get('etherlab_version') == 'none':
            return ''
        snippet = pkgutil.get_data(
            'etherlab_rocker',
            'templates/%s_snippet.Dockerfile.em' % self.get_name()
        ).decode('utf-8')
        return empy_expand(snippet, {})

    def get_docker_args(self, cli_args):
        args = ''
        # Mount the EtherLab configuration file into the container
        args += ' -v /etc/sysconfig/ethercat:/etc/sysconfig/ethercat:ro'
        # Forward the EtherCAT master device into the container (if specified)
        master_idx = cli_args.get('ethercat_master_idx', 0)
        if master_idx >= 0:
            device = '/dev/EtherCAT{}'.format(master_idx)
            args += ' --device {dev}:{dev}'.format(dev=device)
        return args

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(
            '--etherlab',
            action='store_true',
            default=defaults.get('etherlab', False),
            help='Enable EtherCAT Master IgH (EtherLab) support '
                 'in the container.')
        parser.add_argument(
            '--etherlab-version',
            type=str,
            default=defaults.get('etherlab_version', DEFAULT_ETHERLAB_VERSION),
            choices=SUPPORTED_ETHERLAB_VERSIONS,
            help='Version of EtherCAT Master IgH (EtherLab) to install.'
        )
        parser.add_argument(
            '--ethercat-master-idx',
            type=int,
            default=defaults.get(
                'ethercat_master_idx', DEFAULT_ETHERCAT_MASTER_IDX),
            help='Index of the EtherCAT master device "/dev/EtherCAT<idx>"'
                 'to forward into the container. Set to -1 to disable '
                 'forwarding.'
                )
