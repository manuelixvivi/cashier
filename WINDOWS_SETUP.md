# POS AI Backend - Windows Setup Guide

## Prerequisites
- Windows 10/11 (64-bit)
- Python 3.11+ (https://www.python.org/downloads/)
- Git (optional, for cloning)

---

## Step 1: Install MongoDB

### Option A: MongoDB Installer (Recommended)
1. Download MongoDB Community Server: https://www.mongodb.com/try/download/community
2. Pilih versi **7.0**, Platform **Windows**, Package **msi**
3. Jalankan installer, pilih **Complete** setup
4. Centang **"Install MongoDB as a Service"**
5. Klik **Install**

### Option B: ZIP File (Manual)
1. Download ZIP dari link di atas
2. Extract ke `C:\mongodb`
3. Buat folder data:
   ```
   mkdir C:\data\db
   ```
4. Jalankan MongoDB:
   ```
   C:\mongodb\bin\mongod.exe --dbpath C:\data\db
   ```

### Verifikasi MongoDB
Buka CMD baru, jalankan:
```
mongosh
```
Kalo muncul `>`, MongoDB sudah jalan. Ketik `exit` untuk keluar.

---

## Step 2: Install Redis (Windows)

### Download Redis for Windows
1. Buka: https://github.com/microsoftarchive/redis/releases
2. Download `Redis-x64-5.0.14.1.msi` (atau versi terbaru)
3. Install dengan default settings

### Atau pakai WSL (Windows Subsystem for Linux)
Jika sudah install WSL:
```bash
wsl
sudo apt update
sudo apt install redis-server
redis-server --daemonize yes
```

### Verifikasi Redis
```
redis-cli ping
```
Kalo muncul `PONG`, Redis sudah jalan.

---

## Step 3: Setup Project

### 1. Extract ZIP Project
Extract `pos-ai-backend.zip` ke folder, misal:
```
C:\pos-ai-backend
```

### 2. Buka CMD/Terminal
```cmd
cd C:\pos-ai-backend
```

### 3. Buat Virtual Environment
```cmd
python -m venv venv
```

### 4. Aktifkan Virtual Environment
```cmd
venv\Scripts\activate.bat
```

### 5. Install Dependencies
```cmd
pip install -r requirements.txt
```

> **Catatan:** Kalau ada error saat install, coba install satu per satu:
> ```cmd
> pip install Flask==3.0.3 pymongo==4.7.2 flask-jwt-extended==4.6.0
> ```

### 6. Buat File .env
Buat file baru bernama `.env` di folder project, isi dengan:
```
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
MONGO_URI=mongodb://localhost:27017/pos_ai_db
MONGO_DB_NAME=pos_ai_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
AI_MODE=offline
STORE_NAME=Toko Saya
CURRENCY=IDR
```

---

## Step 4: Jalankan Aplikasi

### Terminal 1 - Jalankan Flask API
```cmd
venv\Scripts\activate.bat
python app.py
```

Aplikasi akan jalan di: **http://localhost:5000**

### Terminal 2 - Jalankan Celery Worker (Opsional)
Buka CMD baru:
```cmd
cd C:\pos-ai-backend
venv\Scripts\activate.bat
celery -A app.tasks.celery_worker worker --loglevel=info
```

### Terminal 3 - Jalankan Celery Beat (Opsional)
Buka CMD baru:
```cmd
cd C:\pos-ai-backend
venv\Scripts\activate.bat
celery -A app.tasks.celery_worker beat --loglevel=info
```

---

## Step 5: Verifikasi

### Test Health Check
Buka browser atau Postman:
```
GET http://localhost:5000/health
```

Response:
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "status": "healthy",
    "version": "1.0.0"
  }
}
```

### Test Register User
```
POST http://localhost:5000/api/v1/auth/register
Content-Type: application/json

{
  "username": "admin",
  "email": "admin@toko.com",
  "password": "password123",
  "full_name": "Admin Toko",
  "role": "admin"
}
```

### Test Login
```
POST http://localhost:5000/api/v1/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

---

## Troubleshooting Windows

### Error: "python" tidak dikenali
```cmd
# Cek apakah Python sudah di PATH
python --version

# Kalau tidak, pakai full path
C:\Users\<nama>\AppData\Local\Programs\Python\Python311\python.exe -m venv venv
```

### Error: "pip" tidak dikenali
```cmd
python -m pip install -r requirements.txt
```

### Error: MongoDB tidak connect
1. Pastikan MongoDB service jalan:
   ```
   net start MongoDB
   ```
2. Atau jalankan manual:
   ```
   "C:\Program Files\MongoDB\Server\7.0\bin\mongod.exe" --dbpath="C:\data\db"
   ```

### Error: Redis tidak connect
1. Pastikan Redis service jalan:
   ```
   net start Redis
   ```
2. Atau jalankan manual:
   ```
   "C:\Program Files\Redis\redis-server.exe"
   ```

### Error: Port 5000 sudah dipakai
```cmd
# Cek port
netstat -ano | findstr :5000

# Kill process (ganti <PID> dengan nomor yang muncul)
taskkill /PID <PID> /F
```

### Error: Module not found
```cmd
# Pastikan venv aktif
venv\Scripts\activate.bat

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Error: bcrypt/gunicorn compile failed
```cmd
# Install Visual C++ Build Tools
# Download dari: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Pilih "Desktop development with C++"

# Atau install precompiled wheels
pip install bcrypt --only-binary :all:
```

---

## Jalankan sebagai Windows Service (Production)

### Install NSSM (Non-Sucking Service Manager)
1. Download: https://nssm.cc/download
2. Extract `nssm.exe` ke `C:\Windows\System32`

### Buat Service untuk Flask API
```cmd
nssm install POS-AI-Backend
```
Isi form:
- **Path**: `C:\pos-ai-backend\venv\Scripts\python.exe`
- **Startup directory**: `C:\pos-ai-backend`
- **Arguments**: `app.py`

Klik **Install service**, lalu:
```cmd
net start POS-AI-Backend
```

---

## Quick Start Checklist

- [ ] Python 3.11+ terinstall
- [ ] MongoDB terinstall & jalan
- [ ] Redis terinstall & jalan
- [ ] Project di-extract
- [ ] Virtual environment dibuat
- [ ] Dependencies terinstall
- [ ] File `.env` dibuat
- [ ] Flask API jalan di port 5000
- [ ] Health check berhasil
- [ ] Register user berhasil
- [ ] Login berhasil

---

## API Testing dengan cURL (Windows)

```cmd
# Health Check
curl http://localhost:5000/health

# Register
curl -X POST http://localhost:5000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"email\":\"admin@toko.com\",\"password\":\"password123\",\"full_name\":\"Admin\",\"role\":\"admin\"}"

# Login
curl -X POST http://localhost:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"password123\"}"

# Create Product (ganti <TOKEN> dengan token dari login)
curl -X POST http://localhost:5000/api/v1/products ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <TOKEN>" ^
  -d "{\"name\":\"Rokok Surya\",\"sku\":\"ROK001\",\"category\":\"Rokok\",\"base_unit\":\"bungkus\",\"cost_price\":25000,\"stock\":100}"

# Chatbot Test
curl -X POST http://localhost:5000/api/v1/chatbot/chat ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <TOKEN>" ^
  -d "{\"message\":\"jual rokok 2 bungkus 50000\"}"
```

---

## Selamat! 🎉

POS AI Backend sudah berjalan di Windows Anda. Selanjutnya bisa:
1. Import data produk via API
2. Setup frontend/kasir
3. Coba fitur chatbot AI
4. Lihat laporan & analytics
