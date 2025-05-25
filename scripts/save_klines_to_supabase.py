import importlib.util
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# data_loader 모듈 직접 import
loader_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../microservice/seasonality/data_loader.py'))
spec = importlib.util.spec_from_file_location("data_loader", loader_path)
data_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data_loader)

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    supabase.table("klines").upsert(data).execute()

if __name__ == "__main__":
    symbol = "BTCUSDT"
    klines = data_loader.fetch_15m_klines(symbol, limit=1000)  # 최근 24시간 데이터
    save_klines_to_supabase(symbol, klines)
    print("Supabase에 15분봉 데이터 저장 완료!") 