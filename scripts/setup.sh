#!/bin/bash

set -e  # exit on error

echo "[INFO] Starting Orcstrate setup..."

# Detect distro
if ! command -v apt &> /dev/null
then
    echo "[ERROR] This script currently supports Debian/Ubuntu only."
    exit 1
fi

echo "[INFO] Updating package list..."
sudo apt update

echo "[INFO] Installing dependencies..."
sudo apt install -y \
    python3 \
    python3-gi \
    gir1.2-gtk-4.0 \
    xfce4-terminal

echo "[INFO] Setup complete! You can now run the project."