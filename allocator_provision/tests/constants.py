""" Constants for tests """

import os


HERE = os.path.dirname(os.path.realpath(__file__))
TEST_PK_FILE = os.path.join(HERE, 'test-pk.txt')

ENDPOINT = os.environ['ENDPOINT']
TEST_PK = os.environ['ETH_PRIVATE_KEY']

TEST_PLANS_CSV_FILEPATH = os.path.join(HERE, 'test-plans.csv')
TEST_BENEFICIATES_CSV_FILEPATH = os.path.join(HERE, 'test-beneficiates.csv')

N_OF_PLANS_CSV = 5
N_OF_BENEFICIATES_CSV = 9
