#AWARE - Advanced Web Attack & Ransomware Examiner
AWARE adalah tool pendeteksi ransomware dan serangan siber berbasis web yang mendukung integrasi Python, C++, dan Golang dalam satu perintah. Dirancang seperti utilitas Kali Linux (nmap, sqlmap, dll), AWARE sangat cocok untuk analisa forensik dan mitigasi serangan web.

🔧 Fitur Utama
Deteksi ransomware tipe:
Encrypting Ransomware
Locker Ransomware
MBR Ransomware
Mobile Ransomware
Scareware
#Analisis:
Hash signature malware
Enkripsi tersembunyi (AES, RSA, ChaCha)
Script obfuscation (eval(base64_decode))
Penyisipan file mencurigakan (akira_readme.txt, shell.php, crypto-miner.js)
Integrasi runtime:
cpp_scanner (jika tersedia)
go_scanner (jika tersedia)

🚀 Cara Menjalankan
✅ Jalankan Pemindaian:
python3 aware.py --scan /var/www/html
✅ Jalankan Pemindaian URL:
python3 aware.py --scan https://example.com/var/www/html
📁 Hasil laporan akan tersimpan otomatis di folder aware_reports/.

#CARA INSTALASI 
git clone https://github.com/Mr-C0k1/aware.git
cd aware
chmod +x antiware.py
# Scan direktori target
python3 antiware.py --scan /path/to/folder --type encrypting
# Scan MBR ransomware
sudo python3 antiware.py --scan / --type mbr
# Scan semua jenis ransomware
python3 antiware.py --scan /home/user/documents --type all
# Aktifkan mode tracing IP dari log
python3 antiware.py --log apache.log --trace

#dorware scan 
python3 dorware.py --scan https://example.com 





✨ Fitur Utama
🔍 Deteksi Multi-Ransomware:
Encrypting Ransomware: Deteksi ekstensi file terenkripsi umum seperti .akira, .lockbit, .deadbolt, dll.
Locker Ransomware: Mendeteksi file dan proses yang digunakan untuk mengunci layar korban.
MBR Ransomware: Mendeteksi modifikasi sektor boot (MBR) yang digunakan untuk mengunci sistem sejak awal booting.
Scareware & Mobile (Planned): Dukungan analisis scareware dan ransomware mobile di update berikutnya.

🧠 Pelacakan Penyerang (Attacker Tracing):
Mengekstrak IP pelaku dari ransom note, log, atau koneksi aktif.
Menentukan IP dengan tingkat aktivitas tinggi sebagai tersangka utama.

📁 Forensik File dan Log:
Otomatis mencari ransom note populer (misal: akira_readme.txt).
Menelusuri log untuk mendeteksi aktivitas IP mencurigakan.

🧾 Laporan JSON Otomatis:
Semua hasil pemindaian dan pelacakan disimpan dalam format .json di direktori antiware_logs.


💡 Kebutuhan Tambahan
Untuk hasil maksimal, Anda dapat menyediakan binary scanner tambahan:
cpp_scanner : scanner berbasis C++.
go_scanner : scanner berbasis Golang.
Letakkan binary-nya di folder yang sama dengan aware.py.

✅ Kesimpulan
Satu tool untuk semua kebutuhan pendeteksian ransomware berbasis web.
Bisa dijalankan di Kali Linux, Termux, dan server forensik.
Dukungan penuh multi-bahasa (Python + C++ + Go).
Output tersimpan rapi dalam format .log dan .json.
🧠 AWARE bukan sekadar scanner, tapi juga awal dari proses mitigasi dan pemulihan sistem akibat ransomware.


⚠️ Disclaimer
Proyek ini hanya untuk penelitian keamanan dan edukasi. Jangan gunakan untuk aktivitas ilegal. Penulis tidak bertanggung jawab atas penyalahgunaan tools ini.
