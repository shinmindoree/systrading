import importlib.util
import sys
import os

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../microservice/data_collector/binance_collector.py'))
spec = importlib.util.spec_from_file_location("binance_collector", module_path)
binance_collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(binance_collector)

def test_fetch_usdt_futures_24h_tickers():
    tickers = binance_collector.fetch_usdt_futures_24h_tickers()
    assert isinstance(tickers, list)
    assert len(tickers) > 0
    assert 'symbol' in tickers[0]
    assert 'quoteVolume' in tickers[0] 