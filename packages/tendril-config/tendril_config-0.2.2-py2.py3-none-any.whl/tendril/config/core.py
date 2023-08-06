# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of Tendril.
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
"""
Core Configuration Constants
============================
"""

import os
from tendril.utils.config import ConfigConstant
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = []


config_constants_basic = [
    ConfigConstant(
        'INSTANCE_ROOT',
        "os.path.join(os.path.expanduser('~'), '.tendril')",
        "Path to the tendril instance root. Can be redirected if necessary"
        "with a file named ``redirect`` in this folder."
    )
]


config_constants_redirected = [
    ConfigConstant(
        'INSTANCE_CONFIG_FILE',
        "os.path.join(INSTANCE_ROOT, 'instance_config.py')",
        'Path to the tendril instance configuration.'
    ),
    ConfigConstant(
        'LOCAL_CONFIG_FILE',
        "os.path.join(INSTANCE_ROOT, 'local_config_overrides.py')",
        'Path to local overrides to the instance configuration.'
    ),
]

config_constants_external = [
    ConfigConstant(
        'EXTERNAL_CONFIG_SOURCES',
        "os.path.join(INSTANCE_ROOT, 'external_configs.yaml')",
        "Path to a yaml definition file mapping to external config sources."
    )
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_constants_basic,
                          doc="Tendril Default Instance Root")

    if os.path.exists(os.path.join(manager.INSTANCE_ROOT, 'redirect')):
        logger.info("Found instance redirect")
        with open(os.path.join(manager.INSTANCE_ROOT, 'redirect'), 'r') as f:
            manager.INSTANCE_ROOT = f.read().strip()

    manager.load_elements(config_constants_redirected,
                          doc="Tendril Configuration Paths")

    manager.load_elements(config_constants_external,
                          doc="External Configuration Sources")

    manager.load_config_files()
