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
        accepted_balance, proposed_balance = get_validator_balance(skale_manager, validator['id'])
        diff = accepted_balance - msr
        max_node_amount = accepted_balance // msr
        if not wei:
            if accepted_balance > 0:
                accepted_balance = skale_manager.web3.fromWei(accepted_balance, 'ether')
            if proposed_balance > 0:
                proposed_balance = skale_manager.web3.fromWei(proposed_balance, 'ether')
            if diff > 0:
                diff = skale_manager.web3.fromWei(diff, 'ether')
        validator['accepted_balance'] = accepted_balance
        validator['proposed_balance'] = proposed_balance
        validator['msr_diff'] = f'+{diff}' if diff > 0 else str(diff)
        validator['max_node_amount'] = max_node_amount
    print_validators_list(validators_data, wei)


def get_validator_balance(skale_manager, validator_id):
    delegations = skale_manager.delegation_controller.get_all_delegations_by_validator(validator_id)
    accepted_amount = 0
    proposed_amount = 0
    for delegation in delegations:
        if delegation['status'] == 'ACCEPTED':
            accepted_amount += delegation['amount']
        if delegation['status'] == 'PROPOSED':
            proposed_amount += delegation['amount']
    return accepted_amount, proposed_amount


def init_skale_manager(endpoint):
    return SkaleManager(
        endpoint=endpoint,
        abi_filepath=ABI_FILEPATH
    )
