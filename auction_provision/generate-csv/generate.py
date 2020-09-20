import csv
import sys
import random

from web3.auto import w3

MAX_AMOUNT = 100


def to_checksum_address(address: str) -> str:
    return w3.toChecksumAddress(address)


def generate_accounts(n: int) -> list:
    return [w3.eth.account.create() for i in range(n)]


def accounts_to_addresses(accounts: list):
    return list(map(lambda a: to_checksum_address(a.address), accounts))


def generate_amounts(n: int) -> list:
    return [random.uniform(1, MAX_AMOUNT) for i in range(n)]


def generate_hashes(addresses, amounts):
    return [w3.keccak(text=addr + str(amount)).hex()
            for addr, amount in zip(addresses, amounts)]


def generate_csv(addresses, amounts, hashes, csv_filepath='info.csv'):
    with open(csv_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for addr, amount, hash_ in zip(addresses, amounts, hashes):
            writer.writerow([
                f'address={addr}',
                f'amount={amount}',
                f'hash={hash_}'
            ])


def main():
    number = int(sys.argv[1])
    csv_filename = sys.argv[2]
    accounts = generate_accounts(number)
    addresses = accounts_to_addresses(accounts)
    amounts = generate_amounts(number)
    hashes = generate_hashes(addresses, amounts)
    generate_csv(addresses, amounts, hashes, csv_filepath=csv_filename)


if __name__ == '__main__':
    main()
