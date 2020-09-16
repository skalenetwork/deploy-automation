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
from utils.print_formatters import print_validators_list


def list_validators(endpoint, all=False, wei=False):
    skale_manager = init_skale_manager(endpoint)
    msr = skale_manager.constants_holder.msr()
    print(f'Minimum Staking Requirement: {msr}\n')
    if all:
        validators_data = skale_manager.validator_service.ls(trusted_only=False)
    else:
        validators_data = skale_manager.validator_service.ls(trusted_only=True)
    for validator in validators_data:
        balance = skale_manager.token.get_balance(validator['validator_address'])
        diff = balance - msr
        if not wei:
            balance = skale_manager.web3.fromWei(balance, 'ether')
            diff = skale_manager.web3.fromWei(diff, 'ether')
        validator['balance'] = balance
        validator['msr_diff'] = f'+{diff}' if diff > 0 else str(diff)
        validator['satisfy_msr'] = diff >= 0
    print_validators_list(validators_data, wei)


def init_skale_manager(endpoint):
    return SkaleManager(
        endpoint=endpoint,
        abi_filepath=ABI_FILEPATH
    )
