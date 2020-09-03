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

import csv
import logging
import distutils
import distutils.util

import click

from skale import SkaleAllocator
from skale.utils.web3_utils import init_web3
from skale.wallets import Web3Wallet
from skale.contracts.allocator.allocator import TimeUnit

from utils.print_formatters import print_plans_table, print_beneficiates_table
from utils.constants import ABI_FILEPATH
from utils.helper import to_wei

logger = logging.getLogger(__name__)


def load_csv_dict(path_to_file):
    items = []
    with open(path_to_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            if row['name'] is not '' and bool(distutils.util.strtobool(row['added'])) is False:
                items.append(dict(row))
        return items


def add_beneficiates(csv_filepath, pk_file, dry_run, endpoint):
    beneficiates_data = load_csv_dict(csv_filepath)
    print('Following beneficiates will be added: \n')
    print_beneficiates_table(beneficiates_data)

    if dry_run:
        print('\n Remove option --dry-run to add beneficiates')
        return
    if not click.confirm('\nDo you want to continue?'):
        print('Operation canceled')
        return
    if not endpoint:
        print('Please provide an endpoint')
        return
    add_beneficiates_allocator(beneficiates_data, pk_file, endpoint)


def create_plans(csv_filepath, pk_file, dry_run, endpoint):
    plans_data = load_csv_dict(csv_filepath)
    print('Following plans will be created: \n')
    print_plans_table(plans_data)

    if dry_run:
        print('\n Remove option --dry-run to create plans')
        return
    if not click.confirm('\nDo you want to continue?'):
        print('Operation canceled')
        return
    if not endpoint:
        print('Please provide an endpoint')
        return
    create_plans_allocator(plans_data, pk_file, endpoint)


def create_plans_allocator(plans_data, pk_file, endpoint):
    skale_allocator = init_skale_allocator(endpoint, pk_file)
    for plan in plans_data:
        logger.info(f'Adding plan {plan["name"]}...')
        vesting_interval_time_unit = TimeUnit[plan['vesting_interval_time_unit']]
        skale_allocator.allocator.add_plan(
            vesting_cliff=int(plan['vesting_cliff']),
            total_vesting_duration=int(plan['total_vesting_duration']),
            vesting_interval_time_unit=vesting_interval_time_unit,
            vesting_interval=int(plan['vesting_interval']),
            can_delegate=bool(plan['can_delegate']),
            is_terminatable=bool(plan['is_terminatable']),
            wait_for=True
        )
    logger.info('Added all plans from the CSV file!')


def add_beneficiates_allocator(beneficiates_data, pk_file, endpoint):
    skale_allocator = init_skale_allocator(endpoint, pk_file)
    for beneficiary in beneficiates_data:
        logger.info(f'Adding plan {beneficiary["address"]} ({beneficiary["name"]})')

        full_amount_wei = to_wei(beneficiary["full_amount"])
        lockup_amount_wei = to_wei(beneficiary["lockup_amount"])

        skale_allocator.allocator.connect_beneficiary_to_plan(
            beneficiary_address=beneficiary["address"],
            plan_id=int(beneficiary["plan_id"]),
            start_month=int(beneficiary["start_month"]),
            full_amount=full_amount_wei,
            lockup_amount=lockup_amount_wei,
        )
    logger.info('Added all beneficiates from the CSV file!')


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
