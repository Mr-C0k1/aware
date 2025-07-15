#!/usr/bin/env python3
"""
AntiWare - Website Threat & Malware Scanner (CLI & API)
Versi CLI lengkap dan bisa dieksekusi seperti tool di Kali Linux
"""

import re
import requests
import argparse
import os
import json
import hashlib
import time
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from urllib.parse import urlparse
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv, set_key
from PIL import Image
import sys
import base64
import paramiko

# Load dan buat konfigurasi
ENV_FILE = '.env'
load_dotenv(ENV_FILE)

if not os.path.exists(ENV_FILE):
    with open(ENV_FILE, 'w') as f:
        f.write('API_TOKEN=changeme\nVT_API_KEY=your_virustotal_key\nREPORT_DASHBOARD=https://dashboard.example.com/api/report\n')

# Setup logging
logging.basicConfig(
    filename='antiware_scanner.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

REPORT_DIR = 'antiware_reports'
os.makedirs(REPORT_DIR, exist_ok=True)

KNOWN_MALWARE_HASHES = {
    "e99a18c428cb38d5f260853678922e03": "Akira ransomware variant",
    "44d88612fea8a8f36de82e1278abb02f": "EICAR test file"
}

def tampilkan_logo():
    try:
        from io import BytesIO
        logo_path = os.path.join(os.path.dirname(__file__), 'antiware_logo.png')
        if not os.path.exists(logo_path):
            print("[!] Gambar logo tidak ditemukan: antiware_logo.png")
            return
        img = Image.open(logo_path)
        img = img.convert('L').resize((60, 30))
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                brightness = pixels[x, y]
                char = ' ' if brightness > 128 else '#'
                print(char, end='')
            print()
        print("\nANTIWARE - Website Threat Scanner\n")
    except Exception as e:
        print(f"[!] Gagal menampilkan logo: {e}")

class AntiWareScanner:
    def __init__(self):
        self.threat_patterns = [
            {
                'type': 'Ransomware Behavior',
                'pattern': r'encrypt\\.(php|asp|js)',
                'cve': 'CVE-2022-26134',
                'description': 'Script mencurigakan yang mencoba mengenkripsi file secara massal.',
                'solution': 'Isolasi server dan periksa backup. Blokir script dan ganti kredensial.'
            },
            {
                'type': 'Malware Injection',
                'pattern': r'<script[^>]+src=["\']?https?://[^>]*obfuscated',
                'cve': 'CVE-2023-28546',
                'description': 'Indikasi injeksi script malware obfuscated dari domain tidak dikenal.',
                'solution': 'Hapus script mencurigakan, update CMS/plugin, dan scan file server.'
            },
            {
                'type': 'Ransomware Akira',
                'pattern': r'akira_readme\\.txt|\\.akira$|akira_enc\\.php|Set-MpPreference.*DisableRealtimeMonitoring',
                'cve': 'RANSOM-AKIRA-2023',
                'description': 'Tanda-tanda ransomware Akira ditemukan (catatan, file terenkripsi, atau script anti-antivirus).',
                'solution': 'Putuskan koneksi jaringan, isolasi sistem, dan lakukan forensik file.'
            }
        ]

    def extract_key_from_php_js(self, content):
        found_keys = re.findall(r'[A-Za-z0-9+/=]{16,}', content)
        return found_keys[:3] if found_keys else []

    def scan_url(self, url, extract_key=False):
        url = self.normalize_url(url)
        logging.info(f"[Scan] {url}")
        result = {
            'url': url,
            'scan_time': datetime.now(timezone.utc).isoformat(),
            'vulnerabilities': [],
            'possible_keys': []
        }
        try:
            response = requests.get(url, timeout=10)
            html_content = response.text
            for rule in self.threat_patterns:
                if re.search(rule['pattern'], html_content, re.IGNORECASE):
                    result['vulnerabilities'].append({
                        'type': rule['type'],
                        'cve': rule['cve'],
                        'description': rule['description'],
                        'solution': rule['solution'],
                        'detected_on': url
                    })
            if extract_key:
                result['possible_keys'] = self.extract_key_from_php_js(html_content)
        except Exception as e:
            result['error'] = str(e)
        return result

    def scan_remote_ssh(self, host, key_path, remote_path):
        result = {
            'host': host,
            'remote_path': remote_path,
            'files_scanned': [],
            'possible_keys': []
        }
        try:
            k = paramiko.RSAKey.from_private_key_file(key_path)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host, username='root', pkey=k)
            sftp = ssh.open_sftp()
            files = sftp.listdir(remote_path)
            for fname in files:
                try:
                    remote_file = sftp.open(os.path.join(remote_path, fname))
                    content = remote_file.read().decode('utf-8', errors='ignore')
                    keys = self.extract_key_from_php_js(content)
                    if keys:
                        result['possible_keys'].extend(keys)
                    result['files_scanned'].append(fname)
                except:
                    continue
        except Exception as e:
            result['error'] = str(e)
        return result

    def normalize_url(self, url):
        if not url.startswith('http'):
            return 'http://' + url
        return url

def main():
    tampilkan_logo()
    parser = argparse.ArgumentParser(description='AntiWare Website Threat Detector')
    parser.add_argument('url', nargs='?', help='Target URL to scan')
    parser.add_argument('--extract-key', action='store_true', help='Extract encryption key from target URL')
    parser.add_argument('--ssh', help='SSH host to connect (e.g. root@ip)')
    parser.add_argument('--key', help='Path to private SSH key')
    parser.add_argument('--remote-path', help='Remote path to scan via SSH')
    args = parser.parse_args()

    scanner = AntiWareScanner()

    if args.url:
        result = scanner.scan_url(args.url, extract_key=args.extract_key)
        print(json.dumps(result, indent=2))
    elif args.ssh and args.key and args.remote_path:
        host = args.ssh.split('@')[1]
        result = scanner.scan_remote_ssh(host, args.key, args.remote_path)
        print(json.dumps(result, indent=2))
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
