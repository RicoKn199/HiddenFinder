import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import re

# Regex Konfigurasi
# ------------------ FIND RELATIVE PATH DAN URL
ENDPOINT_REGEX = r"https?://[^\s\"']+|(?<=[\"'])/[a-zA-Z0-9_?&=/.-]+(?=[\"'])"
# ------------------ FIND SENSITIVE KEY
SECRET_REGEXES = {
    # Layanan Cloud & Infrastruktur
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "AWS Access Key ID": r"AKIA[0-9A-Z]{16}",
    "DigitalOcean PAT": r"dop_v1_[a-f0-9]{64}",
    
    # Layanan Pembayaran
    "Stripe Secret Key": r"[sr]k_(?:test|live)_[0-9a-zA-Z]{24}",
    "Square Access Token": r"sq0atp-[0-9A-Za-z\-_]{22}",
    "PayPal Braintree Token": r"access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}",
    
    # Layanan Komunikasi & Kolaborasi
    "Slack Token": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
    "Discord Bot Token": r"[MN][A-Za-z0-9_-]{23,25}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{27}",
    "Telegram Bot Token": r"[0-9]{9,10}:[a-zA-Z0-9_-]{35}",
    
    # Repositori & Version Control
    "GitHub Token (Baru)": r"(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}",
    
    # Standar Web & Database
    "JSON Web Token (JWT)": r"eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*",
    "Firebase URL": r"[a-z0-9.-]+\.firebaseio\.com",
    
    # Generic Catch-all (Untuk token custom yang tidak punya pola khusus)
    # Menggunakan grup penangkap (...) agar hanya mengambil nilai tokennya saja
    "Generic Secret / Password": r"(?i)(?:api_key|apikey|secret_key|token|bearer|password)[\s=:\"']+([A-Za-z0-9_\-\.]{15,})"
}

def create_directory(url):
    """Membuat folder berdasarkan nama domain target"""
    domain = urllib.parse.urlparse(url).netloc
    dir_name = f"js_miner_{domain}"
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name

def analyze_js(content, source_name):
    """Memindai isi file JS menggunakan Dictionary Regex"""
    print(f"\n[🔍] Analisis Regex untuk: {source_name}")
    
    # 1. Mencari Endpoint (Sama seperti sebelumnya)
    endpoints = re.findall(ENDPOINT_REGEX, content)
    unique_endpoints = set(endpoints) 
    
    if unique_endpoints:
        print(f"  --> Ditemukan {len(unique_endpoints)} Endpoint/URL.")
        for ep in list(unique_endpoints)[:1000]:
            print(f"      - {ep}")
        if len(unique_endpoints) > 1000:
            print("      - ... (cek file untuk melihat semua)")

    # 2. MENCARI DATA SENSITIF (BARU)
    # Melakukan perulangan untuk mengecek setiap pola regex yang ada di kamus
    for secret_name, regex_pattern in SECRET_REGEXES.items():
        matches = re.findall(regex_pattern, content)
        
        # Menghapus duplikat
        unique_matches = set(matches)
        
        if unique_matches:
            print(f"  --> [!] POTENSI {secret_name.upper()} DITEMUKAN:")
            for match in list(unique_matches)[:3]: # Menampilkan maks 3 agar rapi
                # Jika regex menangkap string kosong/spasi, kita abaikan
                if match and str(match).strip():
                    print(f"      - {match}")

def mine_js(url):
    print(f"[*] Memulai mining dari: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        
        # Buat folder khusus target ini
        dir_name = create_directory(url)
        print(f"[*] Folder penyimpanan disiapkan: {dir_name}/")
        
        inline_counter = 1
        
        for script in scripts:
            src = script.get('src')
            
            # --- 1. PROSES JS EKSTERNAL ---
            if src:
                full_url = urllib.parse.urljoin(url, src)
                # Mengambil nama file dari URL (misal: app.min.js)
                filename = os.path.basename(urllib.parse.urlparse(full_url).path)
                if not filename or not filename.endswith('.js'):
                    filename = f"external_script_{inline_counter}.js" 
                
                print(f"\n[-] Mengunduh: {full_url}")
                try:
                    js_response = requests.get(full_url, headers=headers, timeout=10)
                    js_content = js_response.text
                    
                    # Simpan ke komputer
                    filepath = os.path.join(dir_name, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(js_content)
                    
                    # Analisis dengan Regex
                    analyze_js(js_content, filename)
                except requests.exceptions.RequestException as e:
                    print(f"  [x] Gagal mengunduh: {e}")
                    
            # --- 2. PROSES JS INLINE ---
            elif script.string:
                js_content = script.string.strip()
                filename = f"inline_script_{inline_counter}.js"
                
                # Simpan ke komputer
                filepath = os.path.join(dir_name, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(js_content)
                
                # Analisis dengan Regex
                analyze_js(js_content, filename)
                inline_counter += 1

    except requests.exceptions.RequestException as e:
        print(f"[!] Gagal memproses {url}: {e}")

# ==========================================
# EKSEKUSI PROGRAM
# ==========================================
if __name__ == "__main__":
    print("-" * 40)
    print("🕸️  JS MINER & ANALYZER v2 🕸️")
    print("-" * 40)
    target = input("Masukkan URL target (contoh: https://example.com): ")
    mine_js(target)
    print(f"\n[*] Selesai! Semua file JS telah disimpan di folder target.")