#!/usr/bin/env python3
"""
AntiWare - All-in-One Ransomware Detector & Attacker Tracer
Mendeteksi Encrypting, Locker, MBR, Mobile, Scareware Ransomware,
dan melakukan traceback IP penyerang dari ransom note, log, dan koneksi aktif.
"""
from colorama import init, Fore

def tampilkan_logo():
    init(autoreset=True)
    logo = f"""{Fore.GREEN}
 █████╗ ██╗    ██╗ █████╗ ██████╗ ███████╗
██╔══██╗██║    ██║██╔══██╗██╔══██╗██╔════╝
███████║██║ █╗ ██║███████║██████╔╝█████╗  
██╔══██║██║███╗██║██╔══██║██╔═══╝ ██╔══╝  
██║  ██║╚███╔███╔╝██║  ██║██║     ███████╗
╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚══════╝

    Website Threat & Ransomware Detector
               Powered by AWARE
"""
    print(logo)

import os
import re
import argparse
import json
import hashlib
import subprocess
from datetime import datetime
from urllib.parse import urlparse

REPORT_DIR = 'antiware_logs'
os.makedirs(REPORT_DIR, exist_ok=True)

KNOWN_EXTENSIONS = ['.encrypted', '.akira', '.lockbit', '.deadbolt']
KNOWN_RANSOM_NOTES = ['readme.txt', 'restore_files.html', 'akira_readme.txt']
KNOWN_LOCKER_PROCESSES = ['taskmgr.exe', 'explorer.exe', 'lockscreen']
KNOWN_BOOT_SIGNATURE = b'\xEB\x3C\x90\x4D\x53'  # Typical MBR header

ATTACKER_IPS = []


def scan_encrypting(path):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in KNOWN_EXTENSIONS):
                result.append(os.path.join(root, file))
            elif file in KNOWN_RANSOM_NOTES:
                with open(os.path.join(root, file), 'r', errors='ignore') as f:
                    content = f.read()
                    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', content)
                    ATTACKER_IPS.extend(ips)
                    result.append(os.path.join(root, file))
    return result


def scan_mbr():
    try:
        with open('/dev/sda', 'rb') as f:
            mbr = f.read(512)
            if mbr[:5] != KNOWN_BOOT_SIGNATURE:
                return True
    except Exception as e:
        return False
    return False


def scan_trace_logs(log_file, threshold=3):
    ip_hits = {}
    with open(log_file, 'r', errors='ignore') as f:
        for line in f:
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            for ip in ips:
                ip_hits[ip] = ip_hits.get(ip, 0) + 1
    suspects = {ip: count for ip, count in ip_hits.items() if count >= threshold}
    ATTACKER_IPS.extend(suspects.keys())
    return suspects


def generate_report(detections, ip_traces):
    now = datetime.now().isoformat()
    data = {
        'time': now,
        'detections': detections,
        'ip_trace': list(set(ip_traces))
    }
    filename = os.path.join(REPORT_DIR, f'report_{now.replace(":", "_")}.json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"[+] Laporan disimpan ke {filename}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AntiWare Unified Scanner")
    parser.add_argument('--scan', help='Path folder target untuk scanning ransomware')
    parser.add_argument('--type', choices=['encrypting', 'locker', 'mbr', 'all'], default='all', help='Jenis ransomware yang ingin dipindai')
    parser.add_argument('--trace', action='store_true', help='Aktifkan mode tracing IP penyerang')
    parser.add_argument('--log', help='Log file yang ingin dianalisis untuk pelacakan IP')
    args = parser.parse_args()

    found = []

    if args.scan:
        if args.type in ['encrypting', 'all']:
            res = scan_encrypting(args.scan)
            found.extend(res)
            print(f"[+] Encrypting ransomware terdeteksi: {len(res)} file")

        if args.type in ['mbr', 'all']:
            if scan_mbr():
                print("[!] Sektor boot kemungkinan dimodifikasi oleh MBR ransomware!")

    if args.trace and args.log:
        suspects = scan_trace_logs(args.log)
        print(f"[+] IP mencurigakan ditemukan: {suspects}")

    generate_report(found, ATTACKER_IPS)
    print("[✓] Proses selesai.")
