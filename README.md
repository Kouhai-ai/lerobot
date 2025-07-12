# SO101 Robot Arm - Minimal Keyboard Control

This is a minimal, standalone script for controlling a SO101 robot arm using keyboard commands. All unnecessary code has been removed, leaving only the essential functionality for basic robot control.

## Features

- **Simple keyboard control** - Use arrow keys, WASD, and other keys to move the robot
- **Emergency stop** - Press SPACE to immediately disable all motors
- **Minimal dependencies** - Only requires 2 Python packages
- **Standalone script** - No complex framework, just one Python file

## Requirements

- SO101 robot arm connected via USB
- Python 3.7 or higher
- Linux/macOS/Windows

## Installation

1. The startup script will automatically create a virtual environment and install dependencies:
```bash
./start_so101_control.sh /dev/tty.usbmodem58FA0962001
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Find your robot's USB port:
   - Linux: Usually `/dev/ttyUSB0` or `/dev/ttyACM0`
   - macOS: Usually `/dev/tty.usbmodem*`
   - Windows: Usually `COM3`, `COM4`, etc.
   - Your robot: `/dev/tty.usbmodem58FA0962001`

## Usage

### Option 1: Using the startup script (recommended)
```bash
./start_so101_control.sh /dev/tty.usbmodem58FA0962001
```

### Option 2: Manual activation
```bash
source venv/bin/activate
python so101_keyboard_control.py --port /dev/tty.usbmodem58FA0962001
```

Replace `/dev/tty.usbmodem58FA0962001` with your actual port if different.

### macOS Accessibility Permission

On macOS, you may see a warning about accessibility permissions. To fix this:

1. Go to **System Preferences** → **Security & Privacy** → **Privacy**
2. Select **Accessibility** from the left sidebar
3. Click the **lock** icon and enter your password
4. Click **+** and add your **Terminal** application
5. Restart the terminal and try again

Alternatively, you can run the script from an IDE like VS Code or PyCharm which may already have permissions.

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move shoulder pan/lift |
| W/S | Move elbow flex |
| A/D | Move wrist flex |
| Q/E | Move wrist roll |
| Z/X | Close/open gripper |
| SPACE | Emergency stop |
| ESC | Exit program |

## Safety

- **Always be ready to press SPACE** for emergency stop
- **Start with small movements** to test the robot
- **Keep the robot in a safe workspace** away from obstacles
- **Never leave the robot unattended** while running

## Troubleshooting

**Connection Issues:**
- Check USB cable connection
- Verify the correct port with `ls /dev/tty*` (Linux/macOS) or Device Manager (Windows)
- Make sure no other programs are using the port

**Permission Issues (Linux):**
```bash
sudo chmod 666 /dev/ttyUSB0
# or add your user to the dialout group:
sudo usermod -a -G dialout $USER
```

**Motor Issues:**
- Check that all motors are properly connected
- Verify motor IDs are set correctly (1-6)
- Ensure adequate power supply

## What Was Removed

This minimal version removes:
- All ML/AI training code
- Dataset recording functionality
- Camera support
- Complex configuration systems
- All other robot types
- Visualization tools
- Most of the original framework

Only the essential SO101 control and keyboard input remain.
