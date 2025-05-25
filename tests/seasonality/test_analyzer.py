import pytest
from datetime import datetime, timedelta
import numpy as np

# 예시 15분 봉 데이터 (open_time, open, close)
sample_klines = [
    # 00:00, 00:15, 00:30, ...
    {"open_time": 0, "open": 100, "close": 101},
    {"open_time": 15*60*1000, "open": 101, "close": 102},
    {"open_time": 30*60*1000, "open": 102, "close": 101},
    {"open_time": 45*60*1000, "open": 101, "close": 100},
    # 01:00, 01:15, ...
    {"open_time": 60*60*1000, "open": 100, "close": 99},
    {"open_time": 75*60*1000, "open": 99, "close": 100},
]

def test_calc_15min_seasonality():
    # analyzer 모듈의 calc_15min_seasonality 함수 import
    import importlib.util, os
    analyzer_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../microservice/seasonality/analyzer.py'))
    spec = importlib.util.spec_from_file_location("analyzer", analyzer_path)
    analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analyzer)

    result = analyzer.calc_15min_seasonality(sample_klines)
    # 15분 구간별 평균 수익률이 계산되어야 함
    assert isinstance(result, dict)
    assert len(result) == 4  # 1시간에 4구간, 2시간이면 8구간이지만 샘플은 6개만 있음
    # 각 구간별로 평균 수익률(float) 값이 있어야 함
    for k, v in result.items():
        assert isinstance(v, float) 