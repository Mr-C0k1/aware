#!/usr/bin/env python3
"""
 - All-in-One Website Ransomware Scanner & Attacker Tracer
Versi terbaru dengan integrasi C++, Golang, dan Python untuk deteksi enkripsi tersembunyi.
"""

import argparse
import os
import subprocess
from datetime import datetime
import hashlib
import re
import requests
from urllib.parse import urlparse

AWARE_REPORT_DIR = "aware_reports"
os.makedirs(AWARE_REPORT_DIR, exist_ok=True)


def log(message):
    print(f"[AWARE] {message}")

def generate_hash_report(filepath):
    if not os.path.isfile(filepath):
        return "[!] Path tidak valid atau bukan file."

    try:
        with open(filepath, 'rb') as f:
            file_bytes = f.read()
            sha256 = hashlib.sha256(file_bytes).hexdigest()
            md5 = hashlib.md5(file_bytes).hexdigest()
        return f"SHA256: {sha256}\nMD5: {md5}"
    except Exception as e:
        return f"[!] Gagal menghitung hash: {e}"

def detect_hidden_encryption(content):
    patterns = [
        r'base64_decode\(',
        r'crypt\(',
        r'openssl_encrypt\(',
        r'aes-\d{3}-cbc',
        r'rsa_public_key',
        r'new Cipher\(',
        r'CryptoJS\.AES',
        r'atob\(',
    ]
    for p in patterns:
        if re.search(p, content, re.IGNORECASE):
            return True
    return False

def scan_website(url):
    result_file = os.path.join(AWARE_REPORT_DIR, f"scan_web_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(result_file, 'w') as f:
        f.write(f"Memindai URL: {url}\n")
        try:
            response = requests.get(url, timeout=10)
            content = response.text
            if detect_hidden_encryption(content):
                f.write("[!!] Deteksi enkripsi tersembunyi pada halaman website!\n")
            else:
                f.write("[OK] Tidak ditemukan enkripsi mencurigakan.\n")

            parsed = urlparse(url)
            f.write(f"[Info] Hostname: {parsed.hostname}\n")
            f.write(f"[Info] Port: {parsed.port if parsed.port else 'default'}\n")
            f.write(f"[Info] Path: {parsed.path}\n")

            log(f"Scan web selesai. Hasil disimpan di {result_file}")

        except Exception as e:
            f.write(f"[!] Gagal mengakses URL: {e}\n")
            log(f"[!] Gagal scan web: {e}")

def scan_target(target):
    log(f"Memulai pemindaian: {target}")

    if target.startswith("http://") or target.startswith("https://"):
        scan_website(target)
        return

    result_file = os.path.join(AWARE_REPORT_DIR, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(result_file, 'w') as f:
        f.write(f"Memindai target: {target}\n")

        # Python level detection
        if os.path.isfile(target):
            try:
                with open(target, 'r', errors='ignore') as file:
                    content = file.read()
                    if detect_hidden_encryption(content):
                        f.write("[!!] Deteksi enkripsi tersembunyi pada file!\n")
                    else:
                        f.write("[OK] Tidak ditemukan enkripsi mencurigakan.\n")
                f.write(generate_hash_report(target) + "\n")
            except Exception as e:
                f.write(f"[!] Gagal membaca file: {e}\n")

        # Jalankan scanner C++ jika tersedia
        if os.path.exists("cpp_scanner"):
            log("Menjalankan scanner C++...")
            try:
                output = subprocess.check_output(["./cpp_scanner", target], stderr=subprocess.STDOUT)
                f.write(output.decode() + "\n")
            except Exception as e:
                f.write(f"[Error] C++ scanner: {e}\n")

        # Jalankan scanner Go jika tersedia
        if os.path.exists("go_scanner"):
            log("Menjalankan scanner Golang...")
            try:
                output = subprocess.check_output(["./go_scanner", target], stderr=subprocess.STDOUT)
                f.write(output.decode() + "\n")
            except Exception as e:
                f.write(f"[Error] Go scanner: {e}\n")

        f.write("\n[Scan selesai]\n")
        log(f"Hasil disimpan di {result_file}")

def main():
    parser = argparse.ArgumentParser(description="AWARE - Website Ransomware Scanner")
    parser.add_argument("--scan", help="Target URL atau direktori lokal/file untuk dipindai")
    args = parser.parse_args()

    if args.scan:
        scan_target(args.scan)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
