""" SM deployment automation """

import os
import sys
import logging

import subprocess
from subprocess import PIPE


import click
from skale import Skale
from skale.utils.account_tools import check_ether_balance
from skale.utils.web3_utils import init_web3
from web3 import Web3

from utils.logger import init_logger, LOG_FILE_PATH
from utils.config import ENDPOINT, ETH_PRIVATE_KEY, MANAGER_TAG, LONG_LINE, PROJECT_DIR, ADDRESS


init_logger(LOG_FILE_PATH, enable_stream_handler=True)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


def check_deploy_vars():
    return ENDPOINT and ETH_PRIVATE_KEY and MANAGER_TAG


def run_cmd(cmd, env={}, shell=False):
    logger.info(f'Running: {cmd}')
    res = subprocess.run(cmd, shell=shell, env={**env, **os.environ})
    if res.returncode:
        logger.error('Error during shell execution:')
        raise subprocess.CalledProcessError(res.returncode, cmd)
    return res


@cli.command('deploy', help='Deploy SKALE Manager contracts')
def deploy():
    if not check_deploy_vars():
        logger.error('You should provide ENDPOINT, ETH_PRIVATE_KEY and MANAGER_TAG')
        exit(1)

    check_balance(ADDRESS)
    logger.info(f'Starting SM deployment: \nTag: {MANAGER_TAG}\nEndpoint: {ENDPOINT}\n')

    run_cmd([f'bash {PROJECT_DIR}/deploy-manager.sh'], {
        'ENDPOINT': ENDPOINT,
        'ETH_PRIVATE_KEY': ETH_PRIVATE_KEY,
        'MANAGER_TAG': MANAGER_TAG,
    }, shell=True)

    logger.info(f'SM deployed!\n{LONG_LINE}\n')
    check_balance(ADDRESS)


@cli.command('balance', help='Check ETH balance of the address')
def balance():
    if not ADDRESS:
        logger.error('ADDRESS is not found in .env')
        return
    check_balance(ADDRESS)


def check_balance(address):
    web3 = init_web3(ENDPOINT)
    return check_ether_balance(web3, address)


if __name__ == "__main__":
    args = sys.argv
    logger.debug(f'\n{LONG_LINE}\nRunning CMD: {" ".join(str(x) for x in args)}\n{LONG_LINE}')
    cli()
