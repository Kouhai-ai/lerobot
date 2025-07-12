#!/usr/bin/env python3
"""
Example Usage of SO101 Controller
=================================

This script demonstrates how to use the SO101Controller class programmatically
without keyboard input. Useful for automated sequences or custom control logic.
"""

import time
from so101_keyboard_control import SO101Controller

def demo_sequence(robot):
    """Demonstrate a simple movement sequence"""
    print("Starting demo sequence...")

    # Get initial positions
    initial_positions = robot.get_positions()
    print(f"Initial positions: {initial_positions}")

    # Move shoulder pan left and right
    print("Moving shoulder pan...")
    robot.move_motor("shoulder_pan", -30)
    time.sleep(2)
    robot.move_motor("shoulder_pan", 30)
    time.sleep(2)
    robot.move_motor("shoulder_pan", 0)
    time.sleep(1)

    # Move shoulder lift up and down
    print("Moving shoulder lift...")
    robot.move_motor("shoulder_lift", 20)
    time.sleep(2)
    robot.move_motor("shoulder_lift", -20)
    time.sleep(2)
    robot.move_motor("shoulder_lift", 0)
    time.sleep(1)

    # Move elbow
    print("Moving elbow...")
    robot.move_motor("elbow_flex", 45)
    time.sleep(2)
    robot.move_motor("elbow_flex", -45)
    time.sleep(2)
    robot.move_motor("elbow_flex", 0)
    time.sleep(1)

    # Move wrist
    print("Moving wrist...")
    robot.move_motor("wrist_flex", 30)
    time.sleep(1)
    robot.move_motor("wrist_roll", 45)
    time.sleep(1)
    robot.move_motor("wrist_roll", -45)
    time.sleep(1)
    robot.move_motor("wrist_roll", 0)
    robot.move_motor("wrist_flex", 0)
    time.sleep(1)

    # Move gripper
    print("Moving gripper...")
    robot.move_motor("gripper", 50)  # Half open
    time.sleep(1)
    robot.move_motor("gripper", 100)  # Fully open
    time.sleep(1)
    robot.move_motor("gripper", 0)  # Closed
    time.sleep(1)

    print("Demo sequence completed!")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="SO101 Robot Demo Sequence")
    parser.add_argument("--port", required=True, help="Serial port (e.g., /dev/ttyUSB0)")
    parser.add_argument("--baudrate", type=int, default=1000000, help="Baudrate (default: 1000000)")
    args = parser.parse_args()

    robot = None

    try:
        # Connect to robot
        print(f"Connecting to SO101 robot on {args.port}...")
        robot = SO101Controller(args.port, args.baudrate)
        robot.connect()

        # Run demo sequence
        demo_sequence(robot)

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        if robot:
            robot.disconnect()
        print("Program ended")

if __name__ == "__main__":
    main()