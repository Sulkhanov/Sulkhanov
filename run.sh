#!/usr/bin/env bash
echo "================================================"
echo "  Bank Customer Service System"
echo "  TSI Software Engineering Course Project"
echo "  Farrukh Sulkhanov - ST79251 - Group 4302BDA"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found."
    echo "Ubuntu/Debian:  sudo apt install python3 python3-tk"
    echo "macOS:          brew install python-tk"
    exit 1
fi

# Check tkinter
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: tkinter not available."
    echo "Ubuntu/Debian:  sudo apt install python3-tk"
    echo "macOS:          brew install python-tk"
    exit 1
fi

echo "Login: username = admin    password = admin123"
echo ""
cd "$(dirname "$0")"
python3 main.py
