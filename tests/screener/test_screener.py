import importlib.util
import os

# screener 모듈 직접 import
screener_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../microservice/screener/screener.py'))
spec = importlib.util.spec_from_file_location("screener", screener_path)
screener = importlib.util.module_from_spec(spec)
spec.loader.exec_module(screener)

# binance_collector 모듈 직접 import
collector_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../microservice/data_collector/binance_collector.py'))
spec2 = importlib.util.spec_from_file_location("binance_collector", collector_path)
binance_collector = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(binance_collector)

def test_get_top_n_by_quote_volume():
    tickers = binance_collector.fetch_usdt_futures_24h_tickers()
    top5 = screener.get_top_n_by_quote_volume(tickers, n=5)
    assert isinstance(top5, list)
    assert len(top5) == 5
    # 거래대금이 내림차순으로 정렬되어 있는지 확인
    quote_volumes = [float(t['quoteVolume']) for t in top5]
    assert quote_volumes == sorted(quote_volumes, reverse=True)
    # 각 항목에 symbol, quoteVolume이 있는지 확인
    for t in top5:
        assert 'symbol' in t
        assert 'quoteVolume' in t 