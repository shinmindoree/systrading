import numpy as np

def calc_15min_seasonality(klines):
    """
    klines: [{"open_time": ms, "open": float, "close": float}, ...]
    15분 단위별로 평균 수익률을 계산하여 dict로 반환
    key: 0~3 (00:00~00:15, 00:15~00:30, ...)
    value: 해당 구간의 평균 수익률(float)
    """
    buckets = {i: [] for i in range(4)}
    for k in klines:
        # 15분 구간 인덱스 (0~3)
        idx = int((k["open_time"] // (15*60*1000)) % 4)
        # 수익률 계산 (close/open - 1)
        ret = (k["close"] / k["open"]) - 1
        buckets[idx].append(ret)
    # 각 구간별 평균 수익률 계산
    result = {i: float(np.mean(buckets[i])) if buckets[i] else 0.0 for i in buckets}
    return result 