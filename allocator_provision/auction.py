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

from web3 import Web3
from decimal import Decimal
from itertools import groupby
from operator import itemgetter

import click

from utils.web3_utils import init_skale_manager, init_skale_manager_with_wallet
from utils.helper import to_wei
from utils.csv_utils import load_csv_lines


ADDRESS_LINE_PREFIX = 'address='
AMOUNT_LINE_PREFIX = 'amount='


def list_to_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def split_data(data, chunk_length):
    return list(list_to_chunks(data, int(chunk_length)))


def transform_data(chunk_data):
    addresses = []
    amounts = []
    _amounts_skl = []
    for line in chunk_data:
        if ADDRESS_LINE_PREFIX in line[0] and AMOUNT_LINE_PREFIX in line[1]:
            address = Web3.toChecksumAddress(get_address(line[0]))
            amount = get_amount(line[1])
            amount_wei = to_wei(amount)

            if int(amount_wei) == 0 or Decimal(amount) == 0:
                print(f'WARNING: Found an address with zero amount: {address} - {amount}, \
it will be skipped.')
                continue

            addresses.append(address)
            amounts.append(amount_wei)
            _amounts_skl.append(amount)
        else:
            raise ValueError('Malformed csv file!')
    return addresses, amounts, _amounts_skl


def get_address(string):
    return string.replace(ADDRESS_LINE_PREFIX, '')


def get_amount(string):
    return string.replace(AMOUNT_LINE_PREFIX, '')


def verify_transfers(csv_file, endpoint):
    data = load_csv_lines(csv_file)
    skale = init_skale_manager(endpoint)

    n_of_rows = len(data)

    for i, line in enumerate(data):
        amount = get_amount(line[1])
        amount_wei = to_wei(amount)
        line.append(int(amount_wei))

    res = [(key, sum(map(itemgetter(3), ele)))
       for key, ele in groupby(sorted(data, key = itemgetter(0)),
                                                key = itemgetter(0))]

    n_of_unique_rows = len(res)

    print('n_of_rows', n_of_rows)
    print('n_of_unique_rows', n_of_unique_rows)

    for i, line in enumerate(res):
        print(f'Verifying {i+1}/{n_of_unique_rows}')
        address = get_address(line[0])
        aggregated_amount = line[1]
        value = skale.token_launch_manager.approved(address)
        info_str = f'Address: {address}, amount: {aggregated_amount}, contract value: {value}'
        print(info_str)
        if aggregated_amount != value:
            raise Exception(info_str)
        print('Values matches!')


def calculate_total(csv_file):
    data = load_csv_lines(csv_file)
    total_amount = 0
    total_amount_wei = 0
    for line in data:
        amount = get_amount(line[1])
        amount_wei = to_wei(amount)
        total_amount += Decimal(amount)
        total_amount_wei += int(amount_wei)
    print('DON\'T USE THESE VALUES IN PRODUCTION!\n')
    print('Total amount: ', total_amount)
    print('Total amount wei: ', total_amount_wei)


def mint_to_tlm(amount, pk_filepath, endpoint):
    amount = int(amount)
    skale = init_skale_manager_with_wallet(endpoint, pk_filepath)
    address = skale.token_launch_manager.address

    balance_before = skale.token.get_balance(address)
    print(f'\nTokenLaunchManager ({address}) balance: {balance_before} SKL (wei)')
    print(f'Tokens to be minted: {amount} SKL (wei)')

    if not click.confirm('\nDo you want to continue?'):
        print('Operation canceled')
        return

    skale.token.mint(address, amount)

    balance_after = skale.token.get_balance(address)
    print(f'\nTokenLaunchManager ({address}) balance: {balance_after} SKL (wei)')


def complete_token_launch(pk_filepath, endpoint):
    skale = init_skale_manager_with_wallet(endpoint, pk_filepath)
    print('THIS ACTION IS IRREVERSIBLE!!!!')
    if not click.confirm('\nDo you want to continue?'):
        print('Operation canceled')
        return
    skale.token_launch_manager.complete_token_launch()
    print('Token launch completed!')
