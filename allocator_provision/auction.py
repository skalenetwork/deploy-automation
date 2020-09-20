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

from utils.web3_utils import init_skale_manager
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
            address = get_address(line[0])
            amount = get_amount(line[1])
            amount_wei = to_wei(amount)
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
        print(f'Verifying {i+1}/{n_of_rows}')
        address = get_address(line[0])
        amount = get_amount(line[1])
        amount_wei = to_wei(amount)
        value = skale.token_launch_manager.approved(address)

        info_str = f'Address: {address}, amount: {amount}, amount_wei: {amount_wei}, contract value: {value}'
        print(info_str)
        if amount_wei != value:
            raise Exception(info_str)
        print('Values matches!')
