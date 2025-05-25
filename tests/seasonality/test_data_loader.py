import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def test_fetch_15m_klines():
    import importlib.util
    data_loader_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../microservice/seasonality/data_loader.py'))
    spec = importlib.util.spec_from_file_location("data_loader", data_loader_path)
    data_loader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(data_loader)

    # BTCUSDT 15분 봉 최근 10개 데이터 수집
    klines = data_loader.fetch_15m_klines(symbol="BTCUSDT", limit=10)
    assert isinstance(klines, list)
    assert len(klines) == 10
    for k in klines:
        assert "open_time" in k
        assert "open" in k
        assert "close" in k 