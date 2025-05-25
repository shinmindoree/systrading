def get_top_n_by_quote_volume(tickers, n=5):
    """
    tickers 리스트에서 거래대금(quoteVolume) 기준 상위 n개 종목을 반환한다.
    내림차순 정렬.
    """
    sorted_tickers = sorted(tickers, key=lambda x: float(x['quoteVolume']), reverse=True)
    return sorted_tickers[:n] 