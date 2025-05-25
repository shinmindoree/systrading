import os
from dotenv import load_dotenv
from binance.um_futures import UMFutures
from supabase import create_client, Client

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

client = UMFutures(key=API_KEY, secret=API_SECRET)

def fetch_15m_klines(symbol: str, limit: int = 1000):
    """
    바이낸스 USDT 선물 마켓에서 15분 봉 데이터를 수집한다.
    반환: [{"open_time": int, "open": float, "close": float}, ...]
    """
    klines = client.klines(symbol=symbol, interval="15m", limit=limit)
    result = []
    for k in klines:
        result.append({
            "open_time": k[0],
            "open": float(k[1]),
            "close": float(k[4])
        })
    return result 

def save_klines_to_supabase(symbol, klines):
    data = [
        {
            "symbol": symbol,
            "open_time": k["open_time"],
            "open": k["open"],
            "close": k["close"]
        }
        for k in klines
    ]
    supabase.table("klines").insert(data).execute()

if __name__ == "__main__":
    symbol = "BTCUSDT"
    klines = fetch_15m_klines(symbol, limit=96)  # 최근 24시간 데이터
    save_klines_to_supabase(symbol, klines) 