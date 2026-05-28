import logging
import asyncio
import ccxt
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pivot_logic import get_current_pivots, check_proximity
import config

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

active_chats = set()
last_alerts = {}
exchange = ccxt.binance()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Bot Crypto Pivot Alert Aktif!\nMemantau {len(config.SYMBOLS)} koin.\n"
             "Gunakan /status untuk melihat level pivot saat ini."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = "📊 *Status Pivot Saat Ini (Top 5)*\n\n"
    
    # Hanya tampilkan top 5 agar tidak kepanjangan di Telegram
    display_symbols = config.SYMBOLS[:5]
    
    try:
        tickers = exchange.fetch_tickers(display_symbols)
        for symbol in display_symbols:
            pivots = get_current_pivots(exchange, symbol)
            if not pivots or symbol not in tickers: continue
            
            price = tickers[symbol]['last']
            message += f"*{symbol}*\n"
            message += f"Harga: `{price}`\n"
            message += f"Pivot (P): `{pivots['P']:.2f}`\n"
            message += f"R1: `{pivots['R1']:.2f}` | S1: `{pivots['S1']:.2f}`\n\n"
            
        if len(config.SYMBOLS) > 5:
            message += f"_...dan {len(config.SYMBOLS)-5} koin lainnya dipantau di background._"
            
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Gagal mengambil data: {e}")

async def price_monitor_job(context: ContextTypes.DEFAULT_TYPE):
    global last_alerts
    try:
        # Ambil semua harga sekaligus (Batch Fetching)
        tickers = exchange.fetch_tickers(config.SYMBOLS)
        
        for symbol in config.SYMBOLS:
            if symbol not in tickers: continue
            
            pivots = get_current_pivots(exchange, symbol)
            if not pivots: continue
            
            price = tickers[symbol]['last']
            alerts = check_proximity(price, pivots, config.THRESHOLD_PERCENT)
            
            for alert in alerts:
                alert_key = f"{symbol}_{alert['level']}"
                current_time = asyncio.get_event_loop().time()
                
                # Cooldown alert 1 jam agar tidak spam
                if alert_key not in last_alerts or current_time - last_alerts[alert_key] > 3600:
                    msg = (f"🚨 *ALERT PIVOT: {symbol}*\n\n"
                           f"Harga `{price}` mendekati level *{alert['level']}* (`{alert['value']:.2f}`)\n"
                           f"Selisih: `{alert['diff_percent']:.3f}%`")
                    
                    for chat_id in active_chats:
                        try:
                            await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
                        except Exception as e:
                            logging.error(f"Gagal kirim ke {chat_id}: {e}")
                    
                    last_alerts[alert_key] = current_time
                    
    except Exception as e:
        logging.error(f"Error in monitor job: {e}")

if __name__ == '__main__':
    if config.TELEGRAM_TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN':
        print("Mohon masukkan TELEGRAM_TOKEN di config.py")
    else:
        application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('status', status))
        
        job_queue = application.job_queue
        job_queue.run_repeating(price_monitor_job, interval=config.CHECK_INTERVAL, first=10)
        
        print(f"Bot berjalan memantau {len(config.SYMBOLS)} koin...")
        application.run_polling()
