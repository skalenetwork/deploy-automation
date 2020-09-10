""" SKALE config test """

import pytest
from click.testing import CliRunner

from core import init_skale_allocator
from tests.constants import TEST_PK_FILE, ENDPOINT


# @pytest.fixture
# def beneficiary_escrow_address(skale_allocator_beneficiary):
#     return skale_allocator_beneficiary.allocator.get_escrow_address(
#         beneficiary_address=skale_allocator_beneficiary.wallet.address
#    )


@pytest.fixture
def skale_allocator():
    '''Returns SKALE Allocator with provider'''
    return init_skale_allocator(
        endpoint=ENDPOINT,
        pk_file=TEST_PK_FILE
    )


@pytest.fixture
def runner():
    return CliRunner()


def str_contains(string, values):
    return all(x in string for x in values)
