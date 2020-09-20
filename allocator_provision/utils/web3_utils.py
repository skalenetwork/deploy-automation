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

from skale import SkaleAllocator, SkaleManager
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet

from utils.constants import ABI_FILEPATH, MANAGER_ABI_FILEPATH


def init_skale_manager(endpoint):
    return SkaleManager(
        endpoint=endpoint,
        abi_filepath=MANAGER_ABI_FILEPATH
    )


def init_skale_manager_with_wallet(endpoint, pk_file):
    web3 = init_web3(endpoint)
    with open(pk_file, 'r') as f:
        pk = str(f.read()).strip()
    wallet = Web3Wallet(pk, web3)
    return SkaleManager(
        endpoint=endpoint,
        abi_filepath=MANAGER_ABI_FILEPATH,
        wallet=wallet
    )


def init_skale_allocator(endpoint, pk_file):
    web3 = init_web3(endpoint)
    with open(pk_file, 'r') as f:
        pk = str(f.read()).strip()
    wallet = Web3Wallet(pk, web3)
    return SkaleAllocator(
        endpoint=endpoint,
        abi_filepath=ABI_FILEPATH,
        wallet=wallet
    )
