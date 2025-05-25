import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def save_screened_symbols(symbols: list[dict]) -> None:
    """
    상위 N개 종목(symbols: [{symbol, quoteVolume, ...}, ...])을 Supabase에 저장
    symbol, quote_volume 컬럼만 저장
    """
    for item in symbols:
        row = {
            "symbol": item["symbol"],
            "quote_volume": float(item["quoteVolume"])
        }
        supabase.table("screened_symbols").insert(row).execute()

def load_recent_screened_symbols(limit: int = 5) -> list[dict]:
    """
    Supabase에서 최근 저장된 종목을 거래대금 내림차순으로 최대 limit개 불러오기
    """
    result = supabase.table("screened_symbols")\
        .select("*")\
        .order("quote_volume", desc=True)\
        .limit(limit)\
        .execute()
    return result.data if result.data else [] 