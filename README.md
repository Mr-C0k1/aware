#AWARE - Advanced Web Attack & Ransomware Examiner
AWARE adalah tool pendeteksi ransomware dan serangan siber berbasis web yang mendukung integrasi Python, C++, dan Golang dalam satu perintah. Dirancang seperti utilitas Kali Linux (nmap, sqlmap, dll), AWARE sangat cocok untuk analisa forensik dan mitigasi serangan web.

#INSTALASI 
git clone https://github.com/Mr-C0k1/aware.git
cd aware
pip install -r requirements.txt --break-system-pakages (jika terjadi eror di kali linux atau debian basic lainya) 
python3 aware.py 

✅ Kegunaan dan Fungsi utama aware.py:
🔎 1. Website Threat Scanner (Scan URL)
Melakukan pemindaian halaman website terhadap indikasi ancaman malware atau ransomware (seperti Akira ransomware).
Deteksi berbasis pola (regex) terhadap skrip mencurigakan seperti:
Script encrypt.php (indikasi ransomware)
Obfuscated script injection
Akira ransomware note (akira_readme.txt)
Dapat mengekstrak kemungkinan kunci enkripsi dari source code (PHP/JS) pada halaman yang dipindai.

🛡️ 2. Remote Server Scanner (via SSH)
Melakukan scan file di server Linux melalui koneksi SSH menggunakan RSA key.
Mengecek isi file (PHP, JS) untuk menemukan:
Pola file mencurigakan
Kemungkinan kunci enkripsi disisipkan oleh malware

🧪 3. Integrasi VirusTotal dan Dashboard (potensial)
Dalam .env terdapat pengaturan VT_API_KEY dan REPORT_DASHBOARD yang bisa dikembangkan untuk:
Melaporkan hasil scan ke dashboard internal
Melakukan verifikasi hash ke VirusTotal (belum diaktifkan dalam versi ini)
🖼️ 4. ASCII Logo + Logging
Menampilkan logo dalam bentuk ASCII art dari gambar antiware_logo.png.
Menyimpan hasil scan dan error ke dalam file antiware_scanner.log.

⚙️ Cara Penggunaan:
🔸 Scan Website:
python3 aware.py https://example.com --extract-key
🔸 Scan Server Remote (SSH):
python3 aware.py --ssh root@192.168.1.10 --key ~/.ssh/id_rsa --remote-path /var/www/html
📁 Output:
Disimpan dalam folder antiware_reports/
Log aktivitas di antiware_scanner.log
Format hasil dalam JSON (mudah digunakan untuk integrasi lebih lanjut)

✅ Kegunaan dan Fungsi dorware.py
🎯 1. Deteksi Berbagai Jenis Ransomware
Tool ini mampu mendeteksi 5 jenis ransomware utama:

Jenis Ransomware	Cara Deteksi	Keterangan
🔐 Encrypting	Mendeteksi ekstensi file terenkripsi seperti .akira, .lockbit, dan ransom note seperti readme.txt	
🪟 Locker	(Belum diimplementasikan penuh, tapi dirancang untuk proses lockscreen dan sejenisnya)	
🧱 MBR (Master Boot Record)	Mengecek apakah sektor MBR (/dev/sda) dimodifikasi, khas dari MBR Ransomware seperti Petya	
📱 Mobile	Dapat ditambah nantinya, belum diimplementasikan	
😱 Scareware	Dideteksi dari ransom note atau pola teks manipulatif pada log	

🧠 2. Pelacakan IP Penyerang (Trace Mode)
Analisis log file (contohnya access.log, auth.log) untuk mendeteksi IP mencurigakan.
Jika ada IP yang muncul lebih dari threshold (default 3 kali), akan ditandai sebagai attacker suspect.

🔑 3. Ekstraksi Kunci Enkripsi
Mendeteksi kemungkinan kata kunci enkripsi (AES, RSA, Key) dari:
Website (--extract-key)
Remote server via SSH (--ssh, --key, --remote-path)
Berguna dalam tahap forensik untuk menyelidiki apakah ada kunci yang disisipkan oleh pelaku.

🐧 4. Analisis Remote via SSH
Terhubung ke server jarak jauh menggunakan kunci privat RSA.
Mengekstrak file .txt pada direktori target, lalu memindai kemungkinan kunci enkripsi.
Sangat berguna untuk sistem yang telah dikompromi tetapi masih bisa diakses via SSH.

📄 5. Laporan Otomatis (JSON Report)
Hasil scan dan IP attacker otomatis disimpan ke file antiware_logs/report_<timestamp>.json.
Format JSON ini memudahkan untuk digunakan dalam SIEM, dashboard, atau laporan keamanan.
⚙️ Contoh Penggunaan
🔸 Deteksi ransomware lokal:
python3 dorware.py --scan /home/user/documents --type encrypting
🔸 Cek MBR ransomware:
python3 dorware.py --scan / --type mbr
🔸 Ekstrak key dari URL:
python3 dorware.py --extract-key https://example.com/restore.php
🔸 Scan remote server via SSH:
python3 dorware.py --ssh root@192.168.0.10 --key ~/.ssh/id_rsa --remote-path /var/www/html
🔸 Analisis log untuk IP attacker:
python3 dorware.py --trace --log /var/log/apache2/access.log
🔒 Keamanan & Audit
Tool ini tidak melakukan penyerangan, hanya pasif melakukan deteksi dan pelacakan.
Cocok digunakan oleh:
Cybersecurity analyst
Incident response team
Sysadmin forensik
Bug hunter untuk menganalisis payload ransomware

✅ Kegunaan suware.py secara umum:
1. 🔐 Mendeteksi Infeksi Ransomware di Sistem Lokal
Tool ini akan memindai direktori lokal yang Anda tentukan dan mendeteksi ransomware berdasarkan:
Ekstensi file terenkripsi seperti .akira, .lockbit, .deadbolt
File ransom note seperti akira_readme.txt, restore_files.html
Sektor boot (MBR) yang dimodifikasi oleh ransomware seperti Petya/NotPetya

2. 🕵️ Melacak IP Penyerang dari File Log
Jika Anda mengaktifkan mode --trace, tool ini akan membaca file log (misalnya access.log atau ransom_note.txt) dan:
Mengidentifikasi alamat IP yang muncul berkali-kali
Membuat daftar tersangka (attacker suspects) berdasarkan intensitas IP muncul

3. 📄 Laporan Otomatis (JSON)
Setelah proses selesai, tool akan membuat file laporan JSON yang berisi:
Waktu scan
File yang terdeteksi terkait ransomware
Daftar IP penyerang
Disimpan ke dalam direktori antiware_logs/

🧠 Penjelasan Tiap Fungsi Penting:
Fungsi	Deskripsi
tampilkan_logo()	Menampilkan logo ASCII di terminal saat dijalankan, agar terlihat seperti tool profesional
scan_encrypting(path)	Memindai direktori yang diberikan untuk mencari file terenkripsi dan ransom note
scan_mbr()	Membaca sektor boot awal dari /dev/sda untuk mengecek apakah ada perubahan dari signature MBR standar
scan_trace_logs(log_file)	Menganalisis file log untuk mencari IP penyerang berdasarkan frekuensi kemunculan
generate_report(...)	Membuat file laporan hasil deteksi dalam format JSON untuk dokumentasi atau bukti forensik

⚙️ Contoh Penggunaan:
🔸 Scan ransomware di folder /home/user/data:
python3 suware.py --scan /home/user/data --type encrypting
🔸 Scan sektor MBR:
python3 suware.py --scan / --type mbr
🔸 Lacak IP penyerang dari file log:
python3 suware.py --trace --log /var/log/apache2/access.log
🔸 Jalankan semua fungsi deteksi:
python3 suware.py --scan /home/user --type all --trace --log /var/log/syslog

🎯 Target Pengguna:
SysAdmin yang ingin mengecek sistem dari serangan ransomware.
Tim forensik keamanan untuk investigasi pasca serangan.
Peneliti malware atau bug hunter yang menganalisis jejak infeksi.
User Linux lanjutan yang ingin mendeteksi anomali sistem.


✅ 1. Kompatibilitas Umum di Kali Linux
Semua script pada dasarnya kompatibel dengan Kali Linux karena:
Ditulis dalam Python 3 (#!/usr/bin/env python3)
Menggunakan modul umum seperti: os, re, argparse, json, subprocess, requests, colorama, dan paramiko
Kali Linux secara default sudah menyediakan banyak dependensi, namun tidak semuanya terinstal.

⚠️ 2. Potensi Error dan Solusinya
Modul/Fungsi	Risiko Error	Penyebab	Solusi
colorama	ModuleNotFoundError	Belum terinstall	pip install colorama
requests	ModuleNotFoundError	Belum terinstall	pip install requests
paramiko (di aware.py & dorware.py)	ModuleNotFoundError	Belum terinstall	pip install paramiko
PIL.Image (aware.py)	ImportError: No module named PIL	Pillow belum terpasang	pip install pillow
Akses /dev/sda (suware.py & dorware.py)	PermissionError: [Errno 13] Permission denied	Membuka sektor disk butuh hak root	Jalankan dengan sudo
ssh, cat, subprocess (dorware.py)	Error jika SSH atau file tidak tersedia	SSH key salah, direktori salah	Pastikan SSH key valid dan path benar
File ransom note tidak ditemukan	File tidak ada di folder target	Tidak dianggap error, hanya hasil kosong	Lewati atau siapkan sample
Jalur file antiware_logo.png (aware.py)	FileNotFoundError	Gambar tidak tersedia	Tambahkan gambar atau modifikasi kode
os.walk(path)	Error jika path salah	Jalur folder tidak ada	Pastikan folder target benar

📦 Saran: Install Semua Dependensi Sekali Jalan
Jalankan perintah berikut di Kali Linux:
sudo apt update
sudo apt install python3-pip
pip3 install colorama requests paramiko pillow
💻 Akses Root untuk Fungsi Tertentu
Beberapa bagian HARUS dijalankan sebagai root, seperti:
Akses /dev/sda untuk scan MBR (suware.py)
Mengakses direktori sistem (/var/log/, /etc, dll)
Menjalankan subprocess SSH (remote command)

🧠 AWARE bukan sekadar scanner, tapi juga awal dari proses mitigasi dan pemulihan sistem akibat ransomware.


⚠️ Disclaimer
Proyek ini hanya untuk penelitian keamanan dan edukasi. Jangan gunakan untuk aktivitas ilegal. Penulis tidak bertanggung jawab atas penyalahgunaan tools ini.
