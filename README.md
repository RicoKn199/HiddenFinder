# 🔍 Hiddenfinder

**Hiddenfinder** adalah *command-line tool* berbasis Python yang dirancang untuk melakukan analisis statis pada file JavaScript. Alat ini menggunakan pola *Regular Expression* (Regex) secara komprehensif untuk mengekstrak URL *endpoint*, Google API Keys, dan potensi kebocoran kredensial (secrets/passwords) yang tersembunyi di dalam kode sumber.

Alat ini sangat berguna untuk keperluan *security testing*, *reverse engineering*, dan analisis keamanan API pada aplikasi web maupun *mobile*.

## ✨ Fitur Utama
* **Ekstraksi Endpoint Cepat**: Menemukan berbagai format URL dan *endpoint* API yang tersembunyi di dalam file `.js`.
* **Deteksi API Key**: Mengidentifikasi potensi kebocoran Google API Key.
* **Deteksi Generic Secrets**: Memindai kata kunci yang sering dikaitkan dengan token autentikasi, *access token*, dan *passwords*.
* **Output Detail**: Menampilkan seluruh hasil temuan secara lengkap tanpa batasan baris untuk analisis yang lebih mendalam.

## 🚀 Prasyarat
Pastikan Anda telah menginstal Python 3.x. 
*(Opsional: Jika ada library tambahan seperti colorama atau requests, cantumkan di sini)*

## 🛠️ Instalasi
1. Clone repositori ini ke dalam mesin lokal Anda:
   ```bash
   git clone [https://github.com/username-kamu/Hiddenfinder.git](https://github.com/username-kamu/Hiddenfinder.git)
2. Masuk ke direktori proyek
   ```bash
   cd Hiddenfinder

💻 Cara Penggunaan
Jalankan skrip dengan memanggil file utamanya dan berikan target file JavaScript yang ingin dianalisis.
Perintah
```bash
python hiddenfinder.py target_file.js
```

⚠️ Disclaimer
Alat ini dibuat murni untuk tujuan edukasi dan pengujian keamanan (security testing) pada sistem yang Anda miliki atau memiliki izin untuk diuji. Pengembang tidak bertanggung jawab atas penyalahgunaan alat ini.
