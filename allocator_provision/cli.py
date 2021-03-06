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

#   -*- coding: utf-8 -*-
#
#   This file is part of allcator-cli
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

import sys
import logging
import traceback

import click

from utils.logs import init_logger, init_log_dir
# from utils.constants import (SKALE_ALLOCATOR_CONFIG_FOLDER, SKALE_ALLOCATOR_CONFIG_FILE,
#                              SKALE_ALLOCATOR_ABI_FILE, LONG_LINE, WALLET_TYPES)

from core import create_plans, add_beneficiates, start_vesting, approve_transfers
from auction import verify_transfers, calculate_total, mint_to_tlm, complete_token_launch

__version__ = '0.0.1'
logger = logging.getLogger(__name__)

PK_FILE_HELP = 'Path to file with private key'


@click.group()
def cli():
    pass


@cli.command('test', help='test cmd')
def test():
    print('test')


@click.argument('csv_filepath')
@click.argument('pk_filepath')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint"
)
@click.option(
    '--dry-run',
    is_flag=True,
    help="Load and show data without actual transactions"
)
@cli.command('create-plans', help='Create plans from CSV file')
def _create_plans(csv_filepath, pk_filepath, dry_run, endpoint):
    create_plans(csv_filepath, pk_filepath, dry_run, endpoint)


@click.argument('csv_filepath')
@click.argument('pk_filepath')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint"
)
@click.option(
    '--dry-run',
    is_flag=True,
    help="Load and show data without actual transactions"
)
@cli.command('add-beneficiates', help='Add beneficiates to plans')
def _add_beneficiates(csv_filepath, pk_filepath, dry_run, endpoint):
    add_beneficiates(csv_filepath, pk_filepath, dry_run, endpoint)


@click.argument('csv_filepath')
@click.argument('pk_filepath')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint"
)
@click.option(
    '--dry-run',
    is_flag=True,
    help="Load and show data without actual transactions"
)
@cli.command('start-vesting', help='Start vesting for beneficiates from csv file')
def _start_vesting(csv_filepath, pk_filepath, dry_run, endpoint):
    start_vesting(csv_filepath, pk_filepath, dry_run, endpoint)


@click.argument('csv_filepath')
@click.argument('pk_filepath')
@click.argument('chunk_length')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint",
    prompt='Ethereum network endpoint'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help="Load and show data without actual transactions"
)
@cli.command('approve-transfers', help='Approve batch of transfers')
def _approve_transfers(csv_filepath, pk_filepath, chunk_length, dry_run, endpoint):
    approve_transfers(csv_filepath, pk_filepath, chunk_length, dry_run, endpoint)


@click.argument('csv_filepath')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint",
    prompt='Ethereum network endpoint'
)
@cli.command('verify-transfers', help='Verify complete transfers')
def _verify_transfers(csv_filepath, endpoint):
    verify_transfers(csv_filepath, endpoint)


@click.argument('csv_filepath')
@cli.command('calculate-total', help='Calculate total amount in csv file')
def _calculate_total(csv_filepath):
    calculate_total(csv_filepath)


@click.argument('amount')
@click.argument('pk_filepath')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint",
    prompt='Ethereum network endpoint'
)
@cli.command('mint-to-tlm', help='Mint tokens to the TokenLaunchManager contract')
def _mint_to_tlm(amount, pk_filepath, endpoint):
    mint_to_tlm(amount, pk_filepath, endpoint)


@click.argument('pk_filepath')
@click.option(
    '--endpoint',
    help="Ethereum network endpoint",
    prompt='Ethereum network endpoint'
)
@cli.command('complete-token-launch', help='Complete token launch')
def _complete_token_launch(pk_filepath, endpoint):
    complete_token_launch(pk_filepath, endpoint)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception",
                 exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

if __name__ == '__main__':
    init_log_dir()
    init_logger(enable_stream_handler=True)
    logger.info(f'cmd: {" ".join(str(x) for x in sys.argv)}, v.{__version__}')
    cmd_collection = click.CommandCollection(sources=[cli])
    try:
        cmd_collection()
    except Exception as err:
        print(f'Command execution failed with {err}. Recheck your inputs')
        traceback.print_exc()
        logger.error(err)
