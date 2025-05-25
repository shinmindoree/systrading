import importlib.util
import os

# binance_collector 모듈 직접 import
collector_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../microservice/data_collector/binance_collector.py'))
spec1 = importlib.util.spec_from_file_location("binance_collector", collector_path)
binance_collector = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(binance_collector)

# screener 모듈 직접 import
screener_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../microservice/screener/screener.py'))
spec2 = importlib.util.spec_from_file_location("screener", screener_path)
screener = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(screener)

# storage 모듈 직접 import
storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../microservice/screener/storage.py'))
spec3 = importlib.util.spec_from_file_location("storage", storage_path)
storage = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(storage)

if __name__ == "__main__":
    # 1. 바이낸스 USDT 선물 24시간 시세 데이터 수집
    tickers = binance_collector.fetch_usdt_futures_24h_tickers()

    # 2. 거래대금 상위 5개 종목 스크리닝
    top5 = screener.get_top_n_by_quote_volume(tickers, n=5)

    # 3. Supabase에 저장
    storage.save_screened_symbols(top5)
    print("상위 5개 종목이 Supabase에 저장되었습니다.") 