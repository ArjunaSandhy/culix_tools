# CULIX-TOOLS

CULIX-TOOLS adalah aplikasi CLI (Command Line Interface) untuk manajemen grup Telegram yang memungkinkan Anda untuk mengumpulkan member dari grup publik dan menambahkan mereka ke grup Anda.

## 🚀 Fitur

- 📥 **Scraper Member**: Mengumpulkan member dari grup Telegram publik
- 📤 **Adder Member**: Menambahkan member ke grup Anda secara otomatis
- 📊 **Sistem Log**: Pencatatan aktivitas lengkap
- 🔄 **Delay System**: Sistem delay pintar untuk menghindari batasan Telegram
- 💻 **CLI Interface**: Antarmuka command line yang mudah digunakan

## 📋 Persyaratan

- Python 3.9 atau lebih tinggi
- Telethon
- Rich
- Pandas
- InquirerPy

## 🛠️ Instalasi

### Menggunakan Python

1. Clone repository:
```bash
git clone https://github.com/username/culix-tools.git
cd culix-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
python main.py
```

### Menggunakan Docker

1. Build image:
```bash
docker build -t culix-tools .
```

2. Jalankan container:
```bash
docker run -d \
  --name culix-tools \
  --restart unless-stopped \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/config:/app/config \
  culix-tools
```

## 📝 Konfigurasi

1. Buat file `config/config.json`:
```json
{
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH",
    "phone": "YOUR_PHONE_NUMBER"
}
```

2. Dapatkan `api_id` dan `api_hash` dari:
   - Kunjungi https://my.telegram.org
   - Login dan buat aplikasi baru
   - Salin API ID dan API Hash

## 💡 Penggunaan

### Menu Utama
1. **[SCRAPER]** - Mengumpulkan member dari grup
   - Masukkan username grup (tanpa @)
   - Hasil akan disimpan dalam format CSV di folder `output`

2. **[ADDER]** - Menambahkan member ke grup
   - Pilih file CSV hasil scraping
   - Masukkan username grup tujuan
   - Sistem akan menambahkan member dengan delay otomatis

3. **[LOGS]** - Melihat 100 aktivitas terakhir
   - Menampilkan log detail dari setiap operasi

4. **[SHUTDOWN]** - Menghentikan aplikasi

## ⚠️ Batasan dan Keamanan

- Gunakan delay yang wajar untuk menghindari pemblokiran
- Pastikan grup sumber adalah grup publik
- Jangan menggunakan untuk spam atau aktivitas yang melanggar ToS Telegram
- Backup data secara berkala

## 📁 Struktur Folder

```
culix-tools/
├── config/         # File konfigurasi
├── logs/          # File log
├── output/        # Hasil scraping (CSV)
├── telegram/      # Modul Telegram
├── utils/         # Utilitas
├── main.py        # File utama
├── Dockerfile     # Konfigurasi Docker
└── requirements.txt
```

## 🔧 Maintenance

### Backup Data
Lakukan backup regular untuk folder:
- `output/`: Hasil scraping
- `logs/`: File log
- `config/`: File konfigurasi

### Update Aplikasi
```bash
git pull origin main
pip install -r requirements.txt
```

Jika menggunakan Docker:
```bash
docker build -t culix-tools .
docker stop culix-tools
docker rm culix-tools
# Jalankan ulang container
```

## 🐛 Troubleshooting

1. **FloodWaitError**
   - Ini normal, aplikasi akan menunggu sesuai waktu yang ditentukan
   - Pertimbangkan untuk menambah delay

2. **Connection Error**
   - Periksa koneksi internet
   - Pastikan API ID dan Hash valid

3. **Privacy Error**
   - Beberapa user memiliki pengaturan privasi yang membatasi
   - Aplikasi akan melewati user tersebut secara otomatis