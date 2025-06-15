# CULIX TOOLS

Telegram member scraper dan adder tool dengan fitur otomatis.

## Menjalankan dengan Docker

### Prasyarat
- Docker dan Docker Compose terinstall di VPS
- Git (opsional)

### Langkah-langkah Instalasi

1. Clone atau upload kode ke VPS:
```bash
git clone <repository-url>
cd culix
```

2. Siapkan file konfigurasi:
```bash
mkdir -p config logs output session
# Pastikan untuk menempatkan file config.json di folder config/
```

3. Build dan jalankan container:
```bash
docker-compose up -d --build
```

### Monitoring dan Maintenance

- Melihat logs aplikasi:
```bash
docker logs -f culix-tools
```

- Menghentikan aplikasi:
```bash
docker-compose down
```

- Restart aplikasi:
```bash
docker-compose restart
```

### Fitur Docker

- Auto-restart jika aplikasi crash
- Persistent storage untuk config, logs, output, dan session
- Timezone disetel ke Asia/Jakarta
- Resource isolation
- Mudah di-update

### Tips Penggunaan di VPS

1. Gunakan screen atau tmux jika perlu mengakses console:
```bash
screen -S culix
docker-compose up
# Ctrl+A+D untuk detach
```

2. Cek status container:
```bash
docker ps
```

3. Backup data penting:
```bash
tar -czf backup.tar.gz config/ logs/ output/ session/
``` 