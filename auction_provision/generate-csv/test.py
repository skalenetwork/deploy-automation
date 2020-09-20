import pathlib

import pytest

from generate import generate_hashes, generate_csv

ADDRESSES = [
    '0x2E0834De824067c27BAa7Fc9bA157a204b74feC4',
    '0xd4aa478BFBa3c669dfE53E6e1D3a4007d72518F3',
    '0xD9bC51c150C5511CE32Fa4657Ed6FabFd251d077'
]
AMOUNTS = [53, 89, 22]


def test_generate_hashes():
    hashes = generate_hashes(ADDRESSES, AMOUNTS)
    print(hashes)
    assert hashes == [
        '0x1da5bce295f5072b4ec66717bbc3d59ca758ebedfc1c47704346336555ea9750',
        '0x9dd6d938d579d807d193eec001237edd72ad25c4291a58973433d35b73022d03',
        '0x13309f81505e31106440faf7247c6c7a3ee195fff0818907728999f76c80934f'
    ]


@pytest.fixture
def csv_filepath():
    filepath = 'test.csv'
    yield filepath
    pathlib.Path(filepath).unlink()


def test_generate_csv_file(csv_filepath):
    hashes = generate_hashes(ADDRESSES, AMOUNTS)
    generate_csv(ADDRESSES, AMOUNTS, hashes, csv_filepath)
    with open(csv_filepath) as csv_file:
        data = csv_file.read()
        assert data == 'address=0x2E0834De824067c27BAa7Fc9bA157a204b74feC4,amount=53,hash=0x1da5bce295f5072b4ec66717bbc3d59ca758ebedfc1c47704346336555ea9750\naddress=0xd4aa478BFBa3c669dfE53E6e1D3a4007d72518F3,amount=89,hash=0x9dd6d938d579d807d193eec001237edd72ad25c4291a58973433d35b73022d03\naddress=0xD9bC51c150C5511CE32Fa4657Ed6FabFd251d077,amount=22,hash=0x13309f81505e31106440faf7247c6c7a3ee195fff0818907728999f76c80934f\n'  # noqa
