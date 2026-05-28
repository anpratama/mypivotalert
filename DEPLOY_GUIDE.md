# 🖥️ Panduan Deployment Bot ke VPS (24/7)

Ikuti langkah-langkah ini untuk menjalankan bot Telegram Anda di server VPS agar aktif terus-menerus meskipun komputer Anda dimatikan.

---

## Langkah 1: Persiapan VPS
1. **Beli/Sewa VPS**: Anda bisa menggunakan DigitalOcean, Linode, AWS, atau Vultr. Pilih OS **Ubuntu 22.04 LTS** (paling direkomendasikan).
2. **Login ke VPS**: Buka terminal (atau Putty di Windows) dan ketik:
   ```bash
   ssh root@ip_address_vps_anda
   ```

---

## Langkah 2: Update dan Instalasi Python
Setelah masuk ke VPS, jalankan perintah berikut untuk menyiapkan lingkungan:
```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Instal Python dan Pip
sudo apt install python3 python3-pip -y

# Cek versi (Pastikan 3.10 ke atas)
python3 --version
```

---

## Langkah 3: Upload Kode ke VPS
Ada dua cara mudah:
- **Cara A (Git)**: Jika Anda menggunakan GitHub, lakukan `git clone`.
- **Cara B (SCP/FileZilla)**: Upload folder `crypto_bot` langsung ke VPS.

Jika sudah di VPS, masuk ke folder tersebut:
```bash
cd crypto_bot
```

---

## Langkah 4: Instal Library Python
Instal semua bahan yang diperlukan agar bot bisa berjalan:
```bash
pip3 install python-telegram-bot[job-queue] ccxt pandas apscheduler
```

---

## Langkah 5: Konfigurasi Bot
Pastikan Anda sudah mengisi **Telegram Token** di file `config.py`.
```bash
nano config.py
# Ganti YOUR_TELEGRAM_BOT_TOKEN dengan token asli Anda.
# Tekan CTRL+O lalu Enter untuk simpan, CTRL+X untuk keluar.
```

---

## Langkah 6: Menjalankan Bot Agar Tidak Mati (Persistence)
Agar bot tetap jalan saat Anda menutup terminal, gunakan **Systemd**. Ini adalah cara paling profesional.

1. **Buat file service**:
   ```bash
   sudo nano /etc/systemd/system/cryptobot.service
   ```

2. **Salin dan tempel kode berikut** (Sesuaikan path-nya):
   ```ini
   [Unit]
   Description=Crypto Pivot Telegram Bot
   After=network.target

   [Service]
   # Sesuaikan 'ubuntu' dengan username VPS Anda (atau 'root')
   User=root
   # Sesuaikan path folder tempat Anda menaruh kode
   WorkingDirectory=/root/crypto_bot
   ExecStart=/usr/bin/python3 bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Aktifkan Service**:
   ```bash
   # Reload sistem agar membaca file baru
   sudo systemctl daemon-reload

   # Jalankan bot
   sudo systemctl start cryptobot

   # Atur agar bot otomatis nyala saat VPS restart
   sudo systemctl enable cryptobot
   ```

4. **Cek Status Bot**:
   ```bash
   sudo systemctl status cryptobot
   ```
   *Jika muncul tulisan hijau "active (running)", selamat! Bot Anda sudah online 24/7.*

---

## Tips Tambahan: Cara Cek Log/Error
Jika bot tidak mengirim pesan, Anda bisa mengecek apa yang terjadi dengan perintah:
```bash
journalctl -u cryptobot -f
```

---
*Panduan ini dibuat untuk membantu Anda menjalankan Bot Agent AI Kripto dengan stabil.*
