#!/usr/bin/env python3
"""
AWARE - All-in-One Website Ransomware Scanner & Attacker Tracer
Versi terbaru dengan integrasi C++, Golang, dan Python untuk deteksi enkripsi tersembunyi.
"""

import argparse
import os
import subprocess
from datetime import datetime

AWARE_REPORT_DIR = "aware_reports"
os.makedirs(AWARE_REPORT_DIR, exist_ok=True)


def log(message):
    print(f"[AWARE] {message}")


def scan_target(target):
    log(f"Memulai pemindaian: {target}")

    result_file = os.path.join(AWARE_REPORT_DIR, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(result_file, 'w') as f:
        # Python level analysis (dummy placeholder)
        f.write(f"Memindai target: {target}\n")

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
    parser.add_argument("--scan", help="Target URL atau direktori lokal untuk dipindai")
    args = parser.parse_args()

    if args.scan:
        scan_target(args.scan)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
