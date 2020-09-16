""" Preparation scripts for tests """

from skale.utils.helper import init_default_logger

from core import init_skale_allocator
from tests.constants import TEST_PK_FILE, ENDPOINT


def main():
    init_default_logger()
    skale_allocator = init_skale_allocator(
        endpoint=ENDPOINT,
        pk_file=TEST_PK_FILE
    )
    vesting_manager_role = skale_allocator.allocator.vesting_manager_role()
    skale_allocator.allocator.grant_role(vesting_manager_role, skale_allocator.wallet.address)
    # transfer_tokens_to_allocator()


if __name__ == '__main__':
    main()
