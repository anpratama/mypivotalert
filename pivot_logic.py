import pandas as pd
import ccxt
from datetime import datetime

# Cache untuk menyimpan pivot harian agar tidak ambil data terus menerus
pivot_cache = {}

def get_ohlcv(exchange, symbol='BTC/USDT', timeframe='1d', limit=2):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def calculate_standard_pivots(high, low, close):
    p = (high + low + close) / 3
    r1 = (p * 2) - low
    s1 = (p * 2) - high
    r2 = p + (high - low)
    s2 = p - (high - low)
    r3 = high + 2 * (p - Low) if 'Low' in locals() else high + 2 * (p - low)
    s3 = low - 2 * (high - p)
    
    return {
        'P': p, 'R1': r1, 'S1': s1, 'R2': r2, 'S2': s2, 'R3': r3, 'S3': s3
    }

def get_current_pivots(exchange, symbol='BTC/USDT'):
    global pivot_cache
    
    today_date = datetime.now().strftime('%Y-%m-%d')
    cache_key = f"{symbol}_{today_date}"
    
    # Jika sudah ada di cache untuk hari ini, kembalikan langsung
    if cache_key in pivot_cache:
        return pivot_cache[cache_key]
    
    try:
        df = get_ohlcv(exchange, symbol, timeframe='1d', limit=2)
        if len(df) < 2:
            return None
        
        # Ambil data hari kemarin (index 0)
        yesterday = df.iloc[0]
        pivots = calculate_standard_pivots(yesterday['high'], yesterday['low'], yesterday['close'])
        
        # Simpan ke cache
        pivot_cache[cache_key] = pivots
        
        # Bersihkan cache lama (opsional, untuk hemat memori)
        if len(pivot_cache) > 500: # Batas cache 500 koin
            pivot_cache.clear()
            pivot_cache[cache_key] = pivots
            
        return pivots
    except Exception as e:
        print(f"Error fetching pivots for {symbol}: {e}")
        return None

def check_proximity(current_price, pivots, threshold_percent=0.1):
    if not pivots: return []
    alerts = []
    for level, value in pivots.items():
        diff = abs(current_price - value) / value * 100
        if diff <= threshold_percent:
            alerts.append({
                'level': level,
                'value': value,
                'diff_percent': diff
            })
    return alerts
