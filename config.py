import os

# Konfigurasi Bot Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')

# Konfigurasi Bursa (Exchange)
# Jika Binance diblokir (Error 451), ganti ke 'bybit', 'kucoin', atau 'gateio'
EXCHANGE_ID = os.getenv('EXCHANGE_ID', 'bybit') 

# Konfigurasi Kripto
SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 
    'XLM/USDT', 'DOGE/USDT', 'GRASS/USDT', 'LIT/USDT', 'XPL/USDT',
    'FF/USDT', 'ZAMA/USDT', 'AZTEC/USDT', 'STABLE/USDT', 'MEGA/USDT',
    'NIGHT/USDT', 'JTO/USDT', 'EDGE/USDT', 'BILL/USDT', 'MON/USDT',
    
]
THRESHOLD_PERCENT = float(os.getenv('THRESHOLD_PERCENT', 0.1))
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))
