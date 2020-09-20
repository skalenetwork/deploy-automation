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

import os
import texttable


def get_tty_width():
    tty_size = os.popen('stty size 2> /dev/null', 'r').read().split()
    if len(tty_size) != 2:
        return 0
    _, width = tty_size
    return int(width)


class Formatter(object):
    def table(self, headers, rows):
        table = texttable.Texttable(max_width=get_tty_width())
        table.set_cols_dtype(['t' for h in headers])
        table.add_rows([headers] + rows)
        table.set_deco(table.HEADER)
        table.set_chars(['-', '|', '+', '-'])

        return table.draw()


def print_plans_table(plans_data):
    headers = [
        'Name',
        'ID',
        'Vesting cliff',
        'Total vesting duration',
        'Vesting interval time unit',
        'Vesting interval',
        'Can delegate',
        'Is terminatable'
    ]
    rows = []
    for plan in plans_data:
        rows.append([
            plan['name'],
            plan['id'],
            plan['vesting_cliff'],
            plan['total_vesting_duration'],
            plan['vesting_interval_time_unit'],
            plan['vesting_interval'],
            plan['can_delegate'],
            plan['is_terminatable']
        ])
    print(Formatter().table(headers, rows))


def print_beneficiates_table(plans_data):
    headers = [
        'Name',
        'Address',
        'Plan ID',
        'Start month',
        'Full amount',
        'Lockup amount'
    ]
    rows = []
    for plan in plans_data:
        rows.append([
            plan['name'],
            plan['address'],
            plan['plan_id'],
            plan['start_month'],
            plan['full_amount'],
            plan['lockup_amount']
        ])
    print(Formatter().table(headers, rows))


def print_auction_chunk_table(addresses, amounts, amounts_skl):
    headers = [
        'Address',
        'Amount (SKL)',
         'Amount (wei)'
    ]
    rows = []
    for i, address in enumerate(addresses):
        rows.append([
            address,
            amounts_skl[i],
            amounts[i]
        ])
    print(Formatter().table(headers, rows))
