import os
import pytest
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

@pytest.mark.skipif(not API_KEY or not API_SECRET, reason="No API key/secret provided")
def test_binance_account_info():
    client = Client(API_KEY, API_SECRET)
    account = client.get_account()
    assert 'balances' in account 