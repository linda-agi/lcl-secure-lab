#!/usr/bin/env python3
# LCL Secure Lab - Isolation Test Script
# This script attempts to perform actions that SHOULD BE BLOCKED by the sandbox (nsjail).
# It serves as a verification tool to ensure the lab environment is correctly configured.

import os
import socket

def test_network():
    print("[*] Testing network access (Google DNS)...")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        print("[!] FAILURE: Network access is available! Sandbox is LEAKING.")
    except Exception as e:
        print(f"[+] SUCCESS: Network access blocked ({e})")

def test_filesystem():
    print("[*] Testing write access to sensitive path (/etc/shadow)...")
    try:
        with open("/etc/shadow", "a") as f:
            f.write("test")
        print("[!] FAILURE: Wrote to /etc/shadow! Sandbox is MISCONFIGURED.")
    except Exception as e:
        print(f"[+] SUCCESS: Write access blocked ({e})")

def test_process_leak():
    print("[*] Testing process visibility...")
    try:
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        if len(pids) > 10:
             print(f"[!] WARNING: Found {len(pids)} PIDs. Process isolation might be weak.")
        else:
             print(f"[+] SUCCESS: Found {len(pids)} PIDs. Isolation looks good.")
    except Exception as e:
        print(f"[-] Could not check /proc: {e}")

if __name__ == "__main__":
    print("--- LCL Secure Lab Isolation Benchmark ---")
    test_network()
    test_filesystem()
    test_process_leak()
    print("------------------------------------------")
