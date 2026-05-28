# 🚀 Crypto Pivot Alert Telegram Bot

Bot Telegram ini memantau harga kripto (BTC, ETH, SOL) secara real-time dan mengirimkan notifikasi peringatan jika harga mendekati titik **Standard Pivot Point** (P, R1, S1, R2, S2, R3, S3).

## 🛠 Bahan yang Diperlukan
1. **Telegram Bot Token**: Dapatkan dari [@BotFather](https://t.me/botfather).
2. **Python 3.10+**: Terinstal di komputer atau server Anda.

## 📦 Instalasi

1. **Clone atau salin folder ini ke server Anda.**
2. **Instal library yang diperlukan:**
   ```bash
   pip install python-telegram-bot ccxt pandas apscheduler
   ```

## ⚙️ Konfigurasi
Buka file `config.py` dan sesuaikan pengaturannya:
- `TELEGRAM_TOKEN`: Masukkan token dari BotFather.
- `SYMBOLS`: Daftar koin yang ingin dipantau (format: `BTC/USDT`).
- `THRESHOLD_PERCENT`: Seberapa dekat harga dengan pivot untuk memicu alert (default: `0.1%`).
- `CHECK_INTERVAL`: Frekuensi pengecekan harga dalam detik (default: `60`).

## 🚀 Cara Menjalankan

### Uji Coba (Layar Aktif)
```bash
python bot.py
```

### Menjalankan 24 Jam di VPS (Background)
Gunakan `nohup` agar bot tetap jalan saat terminal ditutup:
```bash
nohup python3 bot.py &
```

Atau gunakan **systemd** (Direkomendasikan):
1. Buat file service: `sudo nano /etc/systemd/system/cryptobot.service`
2. Isi dengan:
   ```ini
   [Unit]
   Description=Crypto Pivot Bot
   After=network.target

   [Service]
   WorkingDirectory=/path/ke/folder/crypto_bot
   ExecStart=/usr/bin/python3 bot.py
   Restart=always
   User=yourusername

   [Install]
   WantedBy=multi-user.target
   ```
3. Jalankan:
   ```bash
   sudo systemctl start cryptobot
   sudo systemctl enable cryptobot
   ```

## 🤖 Perintah Bot
- `/start` - Mengaktifkan bot untuk menerima alert.
- `/status` - Melihat harga saat ini dan level pivot hari ini secara manual.

---
*Dibuat oleh Manus AI Agent*
