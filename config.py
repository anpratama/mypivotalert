import os

# Konfigurasi Bot Telegram
# Di Railway, Anda bisa mengisi ini di menu "Variables" dengan nama TELEGRAM_TOKEN
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')

# Konfigurasi Kripto
SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 
    'ADA/USDT', 'DOGE/USDT', 'DOT/USDT', 'MATIC/USDT', 'LINK/USDT'
]
THRESHOLD_PERCENT = float(os.getenv('THRESHOLD_PERCENT', 0.1))
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))
