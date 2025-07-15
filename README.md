#AWARE - Advanced Web Attack & Ransomware Examiner
AWARE adalah tool pendeteksi ransomware dan serangan siber berbasis web yang mendukung integrasi Python, C++, dan Golang dalam satu perintah. Dirancang seperti utilitas Kali Linux (nmap, sqlmap, dll), AWARE sangat cocok untuk analisa forensik dan mitigasi serangan web.

#INSTALASI 
git clone https://github.com/Mr-C0k1/aware.git
cd aware
python3 aware.py 

🔐 Suware.py — Website & System Ransomware Detector + Attacker Tracer
🎯 Deskripsi Umum
suware.py adalah sebuah Python-based security tool yang dirancang untuk:
Mendeteksi ransomware (Encrypting, Locker, MBR, Mobile, Scareware) secara lokal pada sistem atau direktori website.
Melacak IP penyerang dari ransom note, file log (web server), atau koneksi aktif.
Memberikan laporan terstruktur dalam format JSON untuk keperluan forensik dan dokumentasi.

⚙️ Fungsi Utama
Fitur	Penjelasan
🔍 Pemindaian File/Folder	Mendeteksi file yang dienkripsi oleh ransomware (misal .akira, .lockbit, .deadbolt, dll).
📄 Pendeteksian Ransom Note	Mengidentifikasi file seperti readme.txt, akira_readme.txt dan mengekstrak IP jika ditemukan.
💾 MBR Scanner	Membaca sektor boot awal (MBR) untuk indikasi ransomware bootloader.
🧠 IP Tracing	Menganalisis file log (misalnya access.log) dan menghitung kemunculan IP untuk melacak asal serangan.
📑 Laporan Otomatis	Output laporan hasil dalam format .json dengan waktu scan.

💻 Contoh Penggunaan
# 1. Deteksi ransomware encrypting saja:
python3 suware.py --scan /var/www/html --type encrypting
# 2. Deteksi semua tipe ransomware & lacak IP dari log:
python3 suware.py --scan /home/web --type all --trace --log /var/log/apache2/access.log

# 3. Deteksi manipulasi bootloader (MBR ransomware):
sudo python3 suware.py --scan / --type mbr
🧪 Ransomware yang Didukung
Tipe Ransomware	Metode Deteksi
Encrypting Ransomware	File extension dan ransom note
Locker Ransomware	(Akan dikembangkan via process watcher)
MBR Ransomware	Signature sektor boot pada /dev/sda
Scareware	Deteksi keyword dan proses (rencana pengembangan)
Mobile Ransomware	(Untuk Android: butuh modul terpisah - tidak dibahas dalam suware.py)

📁 Output Laporan
Disimpan dalam folder antiware_logs/

Format file:
pgsql
report_2025-07-15_08_30_15.json
Isi laporan:
json
{
  "time": "2025-07-15T08:30:15",
  "detections": ["/var/www/html/akira_readme.txt", "..."],
  "ip_trace": ["192.123.1.10", "123.111.24.7"] ( alamat palsu )
}
🛡️ Kelebihan suware.py
✅ Mudah digunakan hanya lewat 1 baris perintah
✅ Dapat dijalankan di Linux Server, Termux, Kali Linux, dan VPS
✅ Cocok untuk sysadmin, peneliti keamanan, dan bug hunter
✅ Tidak membutuhkan instalasi library berat
✅ Dapat diintegrasikan dengan skrip forensik, SIEM, atau dashboard keamanan

📌 Tujuan Script aware.py
Skrip ini adalah tool utama dari proyek AWARE untuk memindai situs web atau direktori lokal dari indikasi ransomware.
🎯 Fitur utama:
🔎 Memindai target (URL atau direktori).
🤖 Menjalankan scanner berbasis Python, C++, dan Golang jika tersedia.
📁 Menyimpan hasil ke dalam file log (aware_reports/scan_*.log).
📦 Siap dipaketkan sebagai executable tool seperti di Kali Linux.
🔍 Penjelasan Per Baris:
Baris 1–6:
python
#!/usr/bin/env python3
"""
AWARE - All-in-One Website Ransomware Scanner & Attacker Tracer
Versi terbaru dengan integrasi C++, Golang, dan Python untuk deteksi enkripsi tersembunyi.
"""
Shebang: Agar file dapat dieksekusi langsung (chmod +x aware.py && ./aware.py).
Docstring: Penjelasan singkat alat.
Baris 8–11:
python
import argparse
import os
import subprocess
from datetime import datetime
Mengimpor modul Python standar yang digunakan untuk:
parsing argumen CLI
menjalankan proses eksternal (subprocess)
membuat timestamp
membuat folder, dll.
Baris 13–14:
python
AWARE_REPORT_DIR = "aware_reports"
os.makedirs(AWARE_REPORT_DIR, exist_ok=True)
Membuat folder aware_reports untuk menyimpan log hasil scan.
Jika folder sudah ada, tidak error (exist_ok=True).
def log(message):
    print(f"[AWARE] {message}")
Fungsi helper untuk mencetak pesan dengan prefix [AWARE].
Fungsi scan_target():
Ini fungsi utama untuk pemindaian.
def scan_target(target):
    ...
Menerima parameter target, bisa URL atau path lokal.
Di dalamnya:
Membuat log awal pemindaian.
Membuat file log hasil scan.
Menulis placeholder pemindaian Python.
Jika ada file cpp_scanner, jalankan (gunakan subprocess).
Jika ada file go_scanner, jalankan juga.
Semua output dimasukkan ke file log.
Fungsi main():
def main():
    parser = argparse.ArgumentParser(description="AWARE - Website Ransomware Scanner")
    parser.add_argument("--scan", help="Target URL atau direktori lokal untuk dipindai")
    args = parser.parse_args()
Parsing argumen CLI.

Saat dijalankan:
python3 aware.py --scan https://target.com
Jika tidak ada --scan, maka akan menampilkan bantuan.

🧪 Output Contoh
Misalnya:
$ python3 aware.py --scan https://example.com

[AWARE] Memulai pemindaian: https://example.com
[AWARE] Menjalankan scanner C++...
[AWARE] Menjalankan scanner Golang...
[AWARE] Hasil disimpan di aware_reports/scan_20250715_123456.log
🔐 Kenapa Ini Powerfull?
Mendukung 3 bahasa: Python, C++, Go.

Fleksibel: Bisa deteksi ransomware real-time jika dipadukan dengan modul hash dan forensik.

Future-proof: Mudah dikembangkan, misalnya menambahkan:
--extract-key
--trace-attacker
--decrypt
atau dashboard monitoring.

🚧 Catatan Penting
Pastikan python3 sudah terinstal.
Jalankan dengan sudo untuk mendeteksi sektor boot (/dev/sda).
Untuk output maksimal, gunakan opsi --trace jika memiliki file log web server.
🧠 AWARE bukan sekadar scanner, tapi juga awal dari proses mitigasi dan pemulihan sistem akibat ransomware.


⚠️ Disclaimer
Proyek ini hanya untuk penelitian keamanan dan edukasi. Jangan gunakan untuk aktivitas ilegal. Penulis tidak bertanggung jawab atas penyalahgunaan tools ini.
