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
