import os
import pytest
from dotenv import load_dotenv
from supabase import create_client, Client

# .env 파일 로드
load_dotenv()

# Supabase 클라이언트 초기화
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def test_save_and_load_screened_symbols():
    # 테스트 데이터
    test_data = [
        {"symbol": "BTCUSDT", "quote_volume": 1000000.0},
        {"symbol": "ETHUSDT", "quote_volume": 500000.0},
        {"symbol": "BNBUSDT", "quote_volume": 300000.0}
    ]
    
    # 데이터 저장
    for item in test_data:
        result = supabase.table("screened_symbols").insert(item).execute()
        assert result.data is not None
    
    # 데이터 조회
    result = supabase.table("screened_symbols")\
        .select("*")\
        .order("quote_volume", desc=True)\
        .limit(3)\
        .execute()
    
    # 검증
    assert len(result.data) == 3
    assert result.data[0]["symbol"] == "BTCUSDT"
    assert result.data[1]["symbol"] == "ETHUSDT"
    assert result.data[2]["symbol"] == "BNBUSDT"
    
    # 테스트 데이터 정리
    for item in test_data:
        supabase.table("screened_symbols")\
            .delete()\
            .eq("symbol", item["symbol"])\
            .execute() 