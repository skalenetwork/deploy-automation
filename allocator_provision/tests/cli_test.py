""" Tests for cli/escrow.py module """

import mock

from cli import (
    test, _add_beneficiates, _create_plans
)
from tests.constants import (TEST_PK_FILE, ENDPOINT, TEST_PLANS_CSV_FILEPATH,
                             TEST_BENEFICIATES_CSV_FILEPATH, N_OF_PLANS_CSV)


def test_test(runner, skale_allocator):
    result = runner.invoke(
        test
    )
    result.output == 'test'


def test_create_plans(runner, skale_allocator):
    plans_before = skale_allocator.allocator.get_all_plans()
    with mock.patch('click.confirm', return_value=True):
        runner.invoke(
            _create_plans,
            [
                TEST_PK_FILE,
                TEST_PLANS_CSV_FILEPATH,
                '--endpoint', ENDPOINT
            ]
        )
    plans_after = skale_allocator.allocator.get_all_plans()
    n_of_plans_after = len(plans_after)

    assert n_of_plans_after == len(plans_before) + N_OF_PLANS_CSV

    assert plans_after[-3] == {
        'totalVestingDuration': 12,
        'vestingCliff': 6,
        'vestingIntervalTimeUnit': 1,
        'vestingInterval': 2,
        'isDelegationAllowed': True,
        'isTerminatable': False,
        'planId': n_of_plans_after - 2
    }

    assert plans_after[-2] == {
        'totalVestingDuration': 36,
        'vestingCliff': 12,
        'vestingIntervalTimeUnit': 1,
        'vestingInterval': 12,
        'isDelegationAllowed': False,
        'isTerminatable': True,
        'planId': n_of_plans_after - 1
    }

    assert plans_after[-1] == {
        'totalVestingDuration': 48,
        'vestingCliff': 12,
        'vestingIntervalTimeUnit': 1,
        'vestingInterval': 12,
        'isDelegationAllowed': True,
        'isTerminatable': True,
        'planId': n_of_plans_after
    }


def ttest_add_beneficiates(runner, skale_allocator):
    # todo: show all plans
    with mock.patch('click.confirm', return_value=True):
        result = runner.invoke(
            _add_beneficiates,
            [
                TEST_PK_FILE,
                TEST_BENEFICIATES_CSV_FILEPATH,
                '--endpoint', ENDPOINT
            ]
        )
    print(result.output)
    assert False
    # todo: _add_beneficiates
    pass
