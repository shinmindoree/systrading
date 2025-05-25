import os
from binance.um_futures import UMFutures
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

client = UMFutures(key=API_KEY, secret=API_SECRET)

def fetch_usdt_futures_24h_tickers():
    """
    바이낸스 USDT 선물 마켓의 모든 심볼 24시간 시세 정보를 가져온다.
    각 종목별로 symbol, quoteVolume(거래대금), volume(거래량), lastPrice(마지막 가격) 등을 포함한다.
    """
    tickers = client.ticker_24hr_price_change()
    return tickers 