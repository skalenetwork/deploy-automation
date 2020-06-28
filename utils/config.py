import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get('ENDPOINT')
ETH_PRIVATE_KEY = os.environ.get('ETH_PRIVATE_KEY')
MANAGER_TAG = os.environ.get('MANAGER_TAG')
ADDRESS = os.environ.get('ADDRESS')
GASPRICE = os.environ.get('GASPRICE')
GASPRICE = os.environ.get('GASPRICE')
PRODUCTION = os.environ.get('PRODUCTION')
NETWORK = os.environ.get('NETWORK')

LONG_LINE = '=' * 60

CURRENT_FILE_LOCATION = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.join(CURRENT_FILE_LOCATION, os.pardir)

ABI_FILEPATH = os.path.join(PROJECT_DIR, 'artifacts', 'abi.json')
