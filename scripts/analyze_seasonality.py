import os
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('font', family='AppleGothic')  # macOS
plt.rcParams['axes.unicode_minus'] = False   # 마이너스(-) 깨짐 방지

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_klines(symbol, limit=1000):
    response = supabase.table("klines") \
        .select("open_time, open, close") \
        .eq("symbol", symbol) \
        .order("open_time") \
        .limit(limit) \
        .execute()
    return response.data

def analyze_seasonality(symbol, limit=1000):
    klines = fetch_klines(symbol, limit)
    if not klines:
        print("데이터가 없습니다.")
        return
    df = pd.DataFrame(klines)
    df['datetime'] = pd.to_datetime(df['open_time'], unit='ms')
    df['hour'] = df['datetime'].dt.hour
    df['return'] = (df['close'] - df['open']) / df['open'] * 100
    df['is_bull'] = (df['close'] > df['open']).astype(int)

    # 시간대별 통계
    hourly_stats = df.groupby('hour').agg(
        avg_return = ('return', 'mean'),
        volatility = ('return', 'std'),
        bull_ratio = ('is_bull', 'mean')
    ).reset_index()
    hourly_stats['bull_ratio'] *= 100

    print(hourly_stats)

    # 시각화
    fig, ax1 = plt.subplots(figsize=(10,6))
    ax1.bar(hourly_stats['hour'], hourly_stats['avg_return'], color='skyblue', label='평균 수익률(%)')
    ax2 = ax1.twinx()
    ax2.plot(hourly_stats['hour'], hourly_stats['volatility'], color='orange', marker='o', label='변동성(표준편차)')
    ax1.set_xlabel('시간(시)')
    ax1.set_ylabel('평균 수익률(%)')
    ax2.set_ylabel('변동성(표준편차)')
    ax1.set_title(f'{symbol} 시간대별 Seasonality 분석')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    symbol = "BTCUSDT"
    analyze_seasonality(symbol, limit=1000) 