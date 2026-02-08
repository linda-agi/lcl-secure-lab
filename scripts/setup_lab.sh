#!/bin/bash
# LCL Secure Lab Setup Script
# Installs necessary dependencies for the sandbox environment.

echo "[*] Initializing LCL Secure Lab dependencies..."

# Detect OS
if [ -f /etc/debian_version ]; then
    echo "[+] Debian/Ubuntu detected."
    sudo apt-get update
    sudo apt-get install -y nsjail python3-pip
elif [ -f /etc/redhat-release ]; then
    echo "[+] RHEL/CentOS detected."
    sudo yum install -y nsjail python3-pip
else
    echo "[!] Unsupported OS. Please install 'nsjail' manually."
fi

# Install Python dependencies
echo "[+] Installing GGUF audit dependencies..."
pip3 install gguf

echo "[SUCCESS] Lab setup complete. Use scripts/run_isolated.sh to start testing."
