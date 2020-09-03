#   -*- coding: utf-8 -*-
#
#   This file is part of deploy-automation
#
#   Copyright (C) 2020 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys


def _get_env():
    try:
        sys._MEIPASS
    except AttributeError:
        return 'dev'
    return 'prod'


ENV = _get_env()
CURRENT_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))

if ENV == 'dev':
    ROOT_DIR = os.path.join(CURRENT_FILE_LOCATION, os.pardir)
else:
    ROOT_DIR = os.path.join(sys._MEIPASS, 'data')

TEXT_FILE = os.path.join(ROOT_DIR, 'text.yml')

LONG_LINE = '-' * 50
SPIN_COLOR = 'yellow'
DISABLE_SPIN = os.getenv('DISABLE_SPIN')

PERMILLE_MULTIPLIER = 10

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOG_FILE_SIZE_MB = 50
LOG_FILE_SIZE_BYTES = LOG_FILE_SIZE_MB * 1000000

LOG_BACKUP_COUNT = 2
LOG_DATA_PATH = os.path.join(ROOT_DIR, 'log')
LOG_FILEPATH = os.path.join(LOG_DATA_PATH, 'allocator-provision.log')
DEBUG_LOG_FILEPATH = os.path.join(LOG_DATA_PATH, 'debug-allocator-provision.log')


ABI_FILEPATH = os.path.join(ROOT_DIR, 'allocator.json')
