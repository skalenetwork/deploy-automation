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

import logging

import click

from skale.contracts.allocator.allocator import TimeUnit

from utils.print_formatters import (print_plans_table, print_beneficiates_table,
                                    print_auction_chunk_table)
from utils.helper import to_wei, str_to_bool
from utils.web3_utils import init_skale_allocator, init_skale_manager_with_wallet
from utils.csv_utils import load_csv_lines, load_csv_dict

from auction import split_data, transform_data

logger = logging.getLogger(__name__)


def approve_transfers(csv_filepath, pk_file, chunk_length, dry_run, endpoint):
    data = load_csv_lines(csv_filepath)
    splitted_data = split_data(data, chunk_length)
    n_of_chunks = len(splitted_data)

    print(f'\nNumber of rows: {len(data)}')
    print(f'Chunk length: {chunk_length}')
    print(f'Number of chunks: {n_of_chunks}\n')

    if not click.confirm('\nDo you want to continue?'):
        print('Operation canceled')
        return

    for i, chunk in enumerate(splitted_data):
        print('==========================================================')
        print(f'Processing chunk {i+1}/{n_of_chunks}...')
        print(f'Items in this chunk: {len(chunk)}\n')

        addresses, amounts, _amounts_skl = transform_data(chunk)
        print_auction_chunk_table(addresses, amounts, _amounts_skl)

        if not click.confirm('\nApprove transfers for this chunk?'):
            print('Skipping this chunk\n')
            continue
        approve_transfers_manager(addresses, amounts, pk_file, endpoint)
        print('Transfers in this chunk were approved!')
    print('All transfers from the csv file were approved!')


def start_vesting(csv_filepath, pk_file, dry_run, endpoint):
    data = load_csv_dict(csv_filepath)
    print('Vesting will be started for the following beneficiates: \n')
    print_beneficiates_table(data)

    if dry_run:
        print('\n Remove option --dry-run to start vesting')
        return
    if not click.confirm('\nDo you want to continue?'):
        print('Operation canceled')
        return
    if not endpoint:
        print('Please provide an endpoint')
        return
    start_vesting_allocator(data, pk_file, endpoint)


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

    print(plans_data)
    print(csv_filepath)
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
    print('\nAll plans are successfully created!')


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
            can_delegate=str_to_bool(plan['can_delegate']),
            is_terminatable=str_to_bool(plan['is_terminatable']),
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


def start_vesting_allocator(beneficiates_data, pk_file, endpoint):
    skale_allocator = init_skale_allocator(endpoint, pk_file)
    for beneficiary in beneficiates_data:
        logger.info(f'Starting vesting for {beneficiary["address"]} ({beneficiary["name"]})')

        skale_allocator.allocator.start_vesting(
            beneficiary_address=beneficiary["address"]
        )
    logger.info('Started vesting for all beneficiates from the CSV file!')


def approve_transfers_manager(addresses, amounts, pk_file, endpoint):
    skale = init_skale_manager_with_wallet(endpoint, pk_file)
    skale.token_launch_manager.approve_batch_of_transfers(addresses, amounts)
