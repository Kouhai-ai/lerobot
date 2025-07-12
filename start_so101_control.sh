#!/bin/bash
# SO101 Robot Arm Control Startup Script
# This script activates the virtual environment and starts the keyboard control

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if port is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <serial_port>"
    echo "Example: $0 /dev/tty.usbmodem58FA0962001"
    exit 1
fi

echo "Starting SO101 Robot Arm Control..."
echo "Port: $1"
echo "Press Ctrl+C to stop"
echo ""

# Run the control script
python3 so101_keyboard_control.py --port "$1"