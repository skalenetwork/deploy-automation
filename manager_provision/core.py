#   -*- coding: utf-8 -*-
#
#   This file is part of deploy-automation
#
#   Copyright (C) 2019 SKALE Labs
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
from skale import SkaleManager

from utils.constants import ABI_FILEPATH


def list_validators(endpoint):
    skale_manager = init_skale_manager(endpoint)
    skale_manager.constants_holder.msr()


def init_skale_manager(endpoint):
    return SkaleManager(
        endpoint=endpoint,
        abi_filepath=ABI_FILEPATH
    )
