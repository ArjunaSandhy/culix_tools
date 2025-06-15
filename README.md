# CULIX-TOOLS

CULIX-TOOLS adalah aplikasi CLI untuk manajemen anggota grup Telegram. Aplikasi ini memungkinkan Anda untuk mengumpulkan anggota dari grup publik, menambahkan anggota ke grup Anda, dan memfilter anggota yang belum bergabung dengan grup target.

## Fitur

1. **[SCRAPER]** - Mengumpulkan anggota dari grup publik
   - Menyimpan data anggota ke file CSV
   - Hanya mengumpulkan anggota valid (memiliki username, bukan bot)
   - Menampilkan statistik hasil pengumpulan

2. **[ADDER]** - Menambahkan anggota ke grup Anda
   - Memilih file CSV hasil scraping
   - Delay otomatis untuk menghindari flood
   - Menampilkan progress dan statistik
   - Mencatat semua aktivitas di log

3. **[FILTER]** - Memeriksa anggota yang belum masuk grup target
   - Memilih file CSV untuk difilter
   - Memeriksa setiap anggota di grup target
   - Delay 20 detik setiap 30 anggota
   - Menyimpan hasil filter ke file CSV baru

4. **[LOGS]** - Melihat 100 aktivitas terakhir

## Instalasi

1. Clone repository ini:
```bash
git clone https://github.com/yourusername/culix-tools.git
cd culix-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Buat file konfigurasi `config/config.json`:
```json
{
    "api_id": "YOUR_API_ID",
    "api_hash": "YOUR_API_HASH",
    "session_name": "session/culix_session"
}
```

## Penggunaan

1. Jalankan aplikasi:
```bash
python main.py
```

2. Pilih opsi yang diinginkan dari menu utama:
   - SCRAPER - untuk mengumpulkan anggota
   - ADDER - untuk menambahkan anggota
   - FILTER - untuk memfilter anggota
   - LOGS - untuk melihat aktivitas
   - SHUTDOWN - untuk keluar

## Struktur Folder

```
culix-tools/
├── config/
│   └── config.json
├── logs/
│   └── activity.log
├── output/
│   └── (file CSV hasil)
├── session/
│   └── culix_session
├── telegram/
│   ├── __init__.py
│   ├── client.py
│   ├── scraper.py
│   ├── adder.py
│   └── filter.py
├── utils/
│   ├── __init__.py
│   ├── display.py
│   ├── logger.py
│   └── delay.py
├── main.py
├── requirements.txt
└── README.md
```

## Catatan Penting

- Pastikan Anda memiliki API ID dan API Hash dari [my.telegram.org](https://my.telegram.org)
- Gunakan delay yang wajar untuk menghindari flood ban
- Backup file CSV hasil scraping yang penting
- Jangan share file session Anda dengan orang lain

## Author

ARXADEV 