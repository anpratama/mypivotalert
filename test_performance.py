import asyncio
import ccxt
import time
from pivot_logic import get_current_pivots
import config

async def test_batch_performance():
    exchange = ccxt.binance()
    print(f"Menguji performa untuk {len(config.SYMBOLS)} koin...")
    
    start_time = time.time()
    
    # 1. Uji Batch Fetching Harga
    print("Mengambil semua harga sekaligus (Batch Fetching)...")
    tickers = exchange.fetch_tickers(config.SYMBOLS)
    print(f"Berhasil mengambil {len(tickers)} harga dalam {time.time() - start_time:.2f} detik.")
    
    # 2. Uji Caching Pivot
    print("\nMenghitung Pivot (Pertama kali - Ambil dari API)...")
    p_start = time.time()
    for s in config.SYMBOLS:
        get_current_pivots(exchange, s)
    print(f"Selesai dalam {time.time() - p_start:.2f} detik.")
    
    print("\nMenghitung Pivot (Kedua kali - Dari Cache)...")
    c_start = time.time()
    for s in config.SYMBOLS:
        get_current_pivots(exchange, s)
    print(f"Selesai dalam {time.time() - c_start:.2f} detik (Harusnya hampir 0 detik).")

if __name__ == "__main__":
    asyncio.run(test_batch_performance())
