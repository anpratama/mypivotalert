#!/bin/bash

# Skrip Otomatisasi Setup Bot Crypto Pivot di VPS Ubuntu
# Dibuat oleh Manus AI

echo "------------------------------------------------"
echo "🚀 Memulai Setup Otomatis Bot Crypto Pivot..."
echo "------------------------------------------------"

# 1. Update Sistem
echo "📦 Mengupdate paket sistem..."
sudo apt update && sudo apt upgrade -y

# 2. Instal Python dan Pip
echo "🐍 Menginstal Python3 dan Pip..."
sudo apt install python3 python3-pip -y

# 3. Instal Library Python
echo "📚 Menginstal library yang dibutuhkan..."
pip3 install python-telegram-bot[job-queue] ccxt pandas apscheduler

# 4. Mendapatkan Lokasi Folder Saat Ini
APP_DIR=$(pwd)
USER_NAME=$(whoami)

echo "📂 Lokasi aplikasi: $APP_DIR"
echo "👤 User: $USER_NAME"

# 5. Membuat Systemd Service
echo "⚙️ Membuat layanan latar belakang (Systemd)..."
SERVICE_FILE="/etc/systemd/system/cryptobot.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Crypto Pivot Telegram Bot
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 6. Menjalankan Service
echo "🔄 Merestart Systemd dan menjalankan bot..."
sudo systemctl daemon-reload
sudo systemctl enable cryptobot
sudo systemctl start cryptobot

echo "------------------------------------------------"
echo "✅ SETUP SELESAI!"
echo "------------------------------------------------"
echo "Bot Anda sekarang berjalan di latar belakang."
echo "Untuk cek status: sudo systemctl status cryptobot"
echo "Untuk cek log: journalctl -u cryptobot -f"
echo "------------------------------------------------"
echo "PENTING: Pastikan Anda sudah mengisi TELEGRAM_TOKEN di config.py!"
