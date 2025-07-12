#!/usr/bin/env python3
"""
Minimal SO101 Robot Arm Control with Keyboard Input
==================================================

This script provides a simple interface to control a SO101 robot arm using keyboard commands.
It extracts only the essential functionality needed for basic robot control.

Controls:
- Arrow keys: Move shoulder_pan and shoulder_lift
- WASD: Move elbow_flex and wrist_flex
- QE: Move wrist_roll
- ZX: Control gripper (open/close)
- ESC: Exit program
- SPACE: Emergency stop

Requirements:
- SO101 robot arm connected via USB
- Python packages: scservo_sdk, pynput

Usage:
    python so101_keyboard_control.py --port /dev/ttyUSB0
"""

import argparse
import logging
import sys
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional
from queue import Queue
import threading

# Try to import required packages
try:
    import scservo_sdk as scs
except ImportError:
    print("ERROR: scservo_sdk not installed. Install with: pip install feetech-servo-sdk")
    sys.exit(1)

try:
    from pynput import keyboard
except ImportError:
    print("ERROR: pynput not installed. Install with: pip install pynput")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OperatingMode(Enum):
    POSITION = 0
    VELOCITY = 1
    PWM = 2
    STEP = 3


@dataclass
class Motor:
    id: int
    model: str
    position: float = 0.0
    min_pos: float = -180.0
    max_pos: float = 180.0


class SO101Controller:
    """Minimal SO101 robot arm controller"""

    # Motor configuration for SO101
    MOTORS = {
        "shoulder_pan": Motor(1, "sts3215"),
        "shoulder_lift": Motor(2, "sts3215"),
        "elbow_flex": Motor(3, "sts3215"),
        "wrist_flex": Motor(4, "sts3215"),
        "wrist_roll": Motor(5, "sts3215"),
        "gripper": Motor(6, "sts3215", min_pos=0.0, max_pos=100.0),
    }

    # Control table addresses for STS3215
    ADDR_TORQUE_ENABLE = 40
    ADDR_GOAL_POSITION = 42
    ADDR_PRESENT_POSITION = 56
    ADDR_OPERATING_MODE = 33

    def __init__(self, port: str, baudrate: int = 1000000):
        self.port = port
        self.baudrate = baudrate
        self.port_handler = None
        self.packet_handler = None
        self.connected = False

    def connect(self):
        """Connect to the robot arm"""
        try:
            logger.info(f"Attempting to connect to {self.port} at {self.baudrate} baud")
            self.port_handler = scs.PortHandler(self.port)
            self.packet_handler = scs.PacketHandler(0)  # Protocol version 0

            logger.debug("Opening port...")
            if not self.port_handler.openPort():
                raise Exception(f"Failed to open port {self.port}")

            logger.debug("Setting baudrate...")
            if not self.port_handler.setBaudRate(self.baudrate):
                raise Exception(f"Failed to set baudrate to {self.baudrate}")

            logger.debug("Testing connection by pinging motors...")
            # Test connection by pinging motors
            self._ping_motors()

            logger.debug("Configuring motors...")
            # Configure motors
            self._configure_motors()

            self.connected = True
            logger.info(f"Successfully connected to SO101 robot on {self.port}")

        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self.disconnect()
            raise

    def disconnect(self):
        """Disconnect from the robot arm"""
        if self.port_handler and self.connected:
            try:
                self.disable_torque()
            except Exception as e:
                logger.warning(f"Error disabling torque during disconnect: {e}")

            try:
                self.port_handler.closePort()
            except Exception as e:
                logger.warning(f"Error closing port during disconnect: {e}")

            self.connected = False
            logger.info("Disconnected from SO101 robot")

    def _ping_motors(self):
        """Ping all motors to check connection"""
        for name, motor in self.MOTORS.items():
            model_number, result, error = self.packet_handler.ping(self.port_handler, motor.id)
            if result != scs.COMM_SUCCESS:
                raise Exception(f"Failed to ping motor {name} (ID: {motor.id}): {self.packet_handler.getTxRxResult(result)}")
            logger.debug(f"Motor {name} (ID: {motor.id}) found, model: {model_number}")

    def _configure_motors(self):
        """Configure motors for position control"""
        for name, motor in self.MOTORS.items():
            # Set operating mode to position control
            self._write_byte(motor.id, self.ADDR_OPERATING_MODE, OperatingMode.POSITION.value)

            # Enable torque
            self._write_byte(motor.id, self.ADDR_TORQUE_ENABLE, 1)

            # Read current position
            motor.position = self._read_position(motor.id)

        logger.info("Motors configured for position control")

    def enable_torque(self):
        """Enable torque for all motors"""
        for motor in self.MOTORS.values():
            self._write_byte(motor.id, self.ADDR_TORQUE_ENABLE, 1)

    def disable_torque(self):
        """Disable torque for all motors"""
        if not self.connected:
            return

        for name, motor in self.MOTORS.items():
            try:
                self._write_byte(motor.id, self.ADDR_TORQUE_ENABLE, 0)
                logger.debug(f"Disabled torque for {name}")
            except Exception as e:
                logger.warning(f"Failed to disable torque for {name}: {e}")

    def _write_byte(self, motor_id: int, address: int, value: int):
        """Write a byte to motor register"""
        try:
            result, error = self.packet_handler.write1ByteTxRx(
                self.port_handler, motor_id, address, value
            )
            if result != scs.COMM_SUCCESS:
                logger.warning(f"Write byte failed for motor {motor_id}: {self.packet_handler.getTxRxResult(result)}")
        except Exception as e:
            logger.warning(f"Exception writing byte to motor {motor_id}: {e}")

    def _write_word(self, motor_id: int, address: int, value: int):
        """Write a word (2 bytes) to motor register"""
        try:
            result, error = self.packet_handler.write2ByteTxRx(
                self.port_handler, motor_id, address, value
            )
            if result != scs.COMM_SUCCESS:
                logger.warning(f"Write word failed for motor {motor_id}: {self.packet_handler.getTxRxResult(result)}")
        except Exception as e:
            logger.warning(f"Exception writing word to motor {motor_id}: {e}")

    def _read_position(self, motor_id: int) -> float:
        """Read current position from motor"""
        position_value, result, error = self.packet_handler.read2ByteTxRx(
            self.port_handler, motor_id, self.ADDR_PRESENT_POSITION
        )
        if result != scs.COMM_SUCCESS:
            logger.warning(f"Read failed for motor {motor_id}: {self.packet_handler.getTxRxResult(result)}")
            return 0.0

        # Convert from motor units to degrees
        return self._motor_units_to_degrees(position_value)

    def _degrees_to_motor_units(self, degrees: float) -> int:
        """Convert degrees to motor units (0-4095)"""
        # Map -180 to 180 degrees to 0-4095 motor units
        motor_units = int((degrees + 180.0) * 4095.0 / 360.0)
        return max(0, min(4095, motor_units))

    def _motor_units_to_degrees(self, motor_units: int) -> float:
        """Convert motor units to degrees"""
        # Map 0-4095 motor units to -180 to 180 degrees
        return (motor_units * 360.0 / 4095.0) - 180.0

    def move_motor(self, motor_name: str, position: float):
        """Move a specific motor to a position"""
        if not self.connected:
            logger.warning("Robot not connected")
            return

        if motor_name not in self.MOTORS:
            logger.warning(f"Unknown motor: {motor_name}")
            return

        motor = self.MOTORS[motor_name]

        # Clamp position to motor limits
        position = max(motor.min_pos, min(motor.max_pos, position))

        # Convert to motor units
        if motor_name == "gripper":
            # Gripper uses 0-100 range mapped to 0-4095
            motor_units = int(position * 4095.0 / 100.0)
        else:
            motor_units = self._degrees_to_motor_units(position)

        # Send command
        self._write_word(motor.id, self.ADDR_GOAL_POSITION, motor_units)
        motor.position = position

        logger.debug(f"Moved {motor_name} to {position:.1f}")

    def get_positions(self) -> Dict[str, float]:
        """Get current positions of all motors"""
        positions = {}
        for name, motor in self.MOTORS.items():
            positions[name] = self._read_position(motor.id)
        return positions

    def emergency_stop(self):
        """Emergency stop - disable all torque"""
        logger.warning("EMERGENCY STOP!")
        self.disable_torque()


class KeyboardController:
    """Handles keyboard input for robot control"""

    def __init__(self, robot: SO101Controller):
        self.robot = robot
        self.key_queue = Queue()
        self.running = False
        self.listener = None

        # Movement step size (degrees)
        self.step_size = 5.0
        self.gripper_step = 10.0

        # Key mappings
        self.key_actions = {
            # Arrow keys for shoulder movement
            keyboard.Key.up: ("shoulder_lift", self.step_size),
            keyboard.Key.down: ("shoulder_lift", -self.step_size),
            keyboard.Key.left: ("shoulder_pan", -self.step_size),
            keyboard.Key.right: ("shoulder_pan", self.step_size),

            # WASD for elbow and wrist
            'w': ("elbow_flex", self.step_size),
            's': ("elbow_flex", -self.step_size),
            'a': ("wrist_flex", -self.step_size),
            'd': ("wrist_flex", self.step_size),

            # QE for wrist roll
            'q': ("wrist_roll", -self.step_size),
            'e': ("wrist_roll", self.step_size),

            # ZX for gripper
            'z': ("gripper", -self.gripper_step),
            'x': ("gripper", self.gripper_step),
        }

    def start(self):
        """Start keyboard listener"""
        self.running = True
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        logger.info("Keyboard controller started")
        self._print_help()

    def stop(self):
        """Stop keyboard listener"""
        self.running = False
        if self.listener:
            self.listener.stop()
        logger.info("Keyboard controller stopped")

    def _on_press(self, key):
        """Handle key press events"""
        if not self.running:
            return

        # Handle special keys
        if key == keyboard.Key.esc:
            logger.info("ESC pressed - exiting")
            self.running = False
            return False
        elif key == keyboard.Key.space:
            logger.info("SPACE pressed - emergency stop")
            self.robot.emergency_stop()
            return

        # Handle movement keys
        action = None
        if hasattr(key, 'char') and key.char:
            action = self.key_actions.get(key.char.lower())
        else:
            action = self.key_actions.get(key)

        if action:
            motor_name, delta = action
            current_pos = self.robot.MOTORS[motor_name].position
            new_pos = current_pos + delta
            self.robot.move_motor(motor_name, new_pos)

    def _on_release(self, key):
        """Handle key release events"""
        pass

    def _print_help(self):
        """Print control help"""
        print("\n" + "="*50)
        print("SO101 Robot Arm Keyboard Control")
        print("="*50)
        print("Controls:")
        print("  Arrow Keys    - Shoulder Pan/Lift")
        print("  W/S          - Elbow Flex")
        print("  A/D          - Wrist Flex")
        print("  Q/E          - Wrist Roll")
        print("  Z/X          - Gripper Close/Open")
        print("  SPACE        - Emergency Stop")
        print("  ESC          - Exit Program")
        print("="*50)
        print("Move the robot carefully!")
        print("="*50 + "\n")


def main():
    """Main program"""
    parser = argparse.ArgumentParser(description="SO101 Robot Arm Keyboard Control")
    parser.add_argument("--port", required=True, help="Serial port (e.g., /dev/ttyUSB0)")
    parser.add_argument("--baudrate", type=int, default=1000000, help="Baudrate (default: 1000000)")
    args = parser.parse_args()

    robot = None
    keyboard_controller = None

    try:
        # Connect to robot
        print(f"Connecting to SO101 robot on {args.port}...")
        robot = SO101Controller(args.port, args.baudrate)
        robot.connect()

        # Start keyboard controller
        keyboard_controller = KeyboardController(robot)
        keyboard_controller.start()

        # Main loop
        while keyboard_controller.running:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Cleanup
        if keyboard_controller:
            keyboard_controller.stop()
        if robot:
            robot.disconnect()
        print("Program ended")


if __name__ == "__main__":
    main()