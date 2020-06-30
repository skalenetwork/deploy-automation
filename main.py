""" SM deployment automation """

import os
import sys
import json
import logging
import datetime

import subprocess

import click
from skale import Skale
from skale.utils.account_tools import check_ether_balance
from skale.wallets.web3_wallet import Web3Wallet, generate_wallet
from skale.utils.web3_utils import init_web3

from utils.logger import init_logger, LOG_FILE_PATH
from utils.config import (ENDPOINT, ETH_PRIVATE_KEY, MANAGER_TAG, LONG_LINE, PROJECT_DIR, ADDRESS,
                          ABI_FILEPATH, GASPRICE, PRODUCTION, NETWORK)


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


@cli.command('update', help='Update SKALE Manager contracts')
def update():
    if not check_deploy_vars():
        logger.error('You should provide ENDPOINT, ETH_PRIVATE_KEY and MANAGER_TAG')
        exit(1)

    web3 = init_web3(ENDPOINT)
    wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)

    check_balance(wallet.address)
    logger.info(f'Starting SM update: \nTag: {MANAGER_TAG}\nEndpoint: {ENDPOINT}\nAddress: {wallet.address}\n')

    res = run_cmd([f'bash {PROJECT_DIR}/upgrade-manager.sh'], {
        'ENDPOINT': ENDPOINT,
        'ETH_PRIVATE_KEY': ETH_PRIVATE_KEY,
        'MANAGER_TAG': MANAGER_TAG,
        'GASPRICE': GASPRICE,
        'PRODUCTION': PRODUCTION,
        'NETWORK': NETWORK,
    }, shell=True)
    if res.returncode:
        logger.error('Update failed!')
        exit(res.returncode)
    logger.info(f'SM updated!\n{LONG_LINE}\n')
    check_balance(ADDRESS)

    time = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")
    update_info = {
        'address': wallet.address,
        'time': time,
        'manager_tag': MANAGER_TAG,
        'endpoint': ENDPOINT,
    }
    with open(f'{PROJECT_DIR}/artifacts/update_data.json', 'w', encoding='utf-8') as f:
        json.dump(update_info, f, ensure_ascii=False, indent=4)


@cli.command('deploy', help='Deploy SKALE Manager contracts')
def deploy():
    if not check_deploy_vars():
        logger.error('You should provide ENDPOINT, ETH_PRIVATE_KEY and MANAGER_TAG')
        exit(1)

    web3 = init_web3(ENDPOINT)
    wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)

    check_balance(wallet.address)
    logger.info(f'Starting SM deployment: \nTag: {MANAGER_TAG}\nEndpoint: {ENDPOINT}\nAddress: {wallet.address}\n')

    res = run_cmd([f'bash {PROJECT_DIR}/deploy-manager.sh'], {
        'ENDPOINT': ENDPOINT,
        'ETH_PRIVATE_KEY': ETH_PRIVATE_KEY,
        'MANAGER_TAG': MANAGER_TAG,
        'GASPRICE': GASPRICE,
        'PRODUCTION': PRODUCTION,
        'NETWORK': NETWORK,
    }, shell=True)
    if res.returncode:
        logger.error('Deployment failed!')
        exit(res.returncode)
    logger.info(f'SM deployed!\n{LONG_LINE}\n')
    check_balance(ADDRESS)

    time = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")
    deploy_info = {
        'address': wallet.address,
        'time': time,
        'manager_tag': MANAGER_TAG,
        'endpoint': ENDPOINT,
    }
    with open(f'{PROJECT_DIR}/artifacts/deploy_data.json', 'w', encoding='utf-8') as f:
        json.dump(deploy_info, f, ensure_ascii=False, indent=4)


@cli.command('balance', help='Check ETH balance of the address')
def balance():
    if not ADDRESS:
        logger.error('ADDRESS is not found in .env')
        return
    check_balance(ADDRESS)


def check_balance(address):
    web3 = init_web3(ENDPOINT)
    return check_ether_balance(web3, address)


@cli.command('set-roles', help='')
def set_roles():
    web3 = init_web3(ENDPOINT)
    owner_wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)
    skale = Skale(ENDPOINT, ABI_FILEPATH, owner_wallet)
    wallets = setup_wallets(web3)
    grant_admin_role(skale, wallets[0])
    grant_schain_creator_role(skale, wallets[1])


def setup_wallets(web3):
    wallets = generate_wallets(web3, 2)
    for wallet in wallets:
        logger.warning(f'Generated wallet: {wallet.address}, PK: {wallet._private_key}, save it somewhere!')
    role_keys = [
        {
            'address': wallets[0].address,
            'private_key': wallets[0]._private_key,
            'role': 'ADMIN_ROLE'
        },
        {
            'address': wallets[1].address,
            'private_key': wallets[1]._private_key,
            'role': 'SCHAIN_CREATOR_ROLE'
        }
    ]
    time = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H:%M:%S")
    with open(f'{PROJECT_DIR}/role_keys-{time}.json', 'w', encoding='utf-8') as f:
        json.dump(role_keys, f, ensure_ascii=False, indent=4)
    return wallets


def grant_admin_role(skale, admin_wallet):
    admin_role = skale.manager.admin_role()
    skale.manager.grant_role(
        admin_role,
        admin_wallet.address,
        wait_for=True
    )
    has_admin_role = skale.manager.has_role(admin_role, admin_wallet.address)
    if has_admin_role:
        logger.info(f'{admin_wallet.address} now have admin permissions!')
    else:
        logger.error(f'Permissions for {admin_wallet.address} was not granted!')


def grant_schain_creator_role(skale, schain_creator_wallet):
    schain_creator_role = skale.schains.schain_creator_role()
    skale.schains.grant_role(
        schain_creator_role,
        schain_creator_wallet.address,
        wait_for=True
    )
    logger.info(f'{schain_creator_wallet.address} now have sChain creation permissions!')


def generate_wallets(web3, n_wallets):
    return [generate_wallet(web3) for i in range(0, n_wallets)]



@cli.command('check-constants', help='')
def _check_constants():
    web3 = init_web3(ENDPOINT)
    skale = Skale(ENDPOINT, ABI_FILEPATH)
    check_constants(skale)
    

def check_constants(skale):
    reward_period = skale.constants_holder.get_reward_period()
    delta_period = skale.constants_holder.get_delta_period()
    check_time = skale.constants_holder.get_check_time()

    logger.info(f'reward_period: {reward_period}')
    logger.info(f'delta_period: {delta_period}')
    logger.info(f'check_time: {check_time}')

    if reward_period != 86400 or delta_period != 3600 or check_time != 300:
        logger.warning('SM with testnet constants!')
    else:
        logger.info('SM with mainnet constants!')


@cli.command('set-test-epoch', help='')
def set_epoch_and_delta():
    web3 = init_web3(ENDPOINT)
    owner_wallet = Web3Wallet(ETH_PRIVATE_KEY, web3)
    skale = Skale(ENDPOINT, ABI_FILEPATH, owner_wallet)
    new_epoch_in_sec = 30 * 60
    new_delta_in_sec = 10 * 60
    skale.constants_holder.set_periods(new_epoch_in_sec, new_delta_in_sec)
    print("new_reward_period", skale.constants_holder.get_reward_period())
    print("new_delta_period", skale.constants_holder.get_delta_period())


if __name__ == "__main__":
    args = sys.argv
    logger.debug(f'\n{LONG_LINE}\nRunning CMD: {" ".join(str(x) for x in args)}\n{LONG_LINE}')
    cli()
