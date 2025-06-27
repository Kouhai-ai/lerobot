#!/usr/bin/env python3

import time
import traceback
from lerobot.common.robots.so101_follower import SO101Follower, SO101FollowerConfig
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset
from lerobot.common.datasets.utils import hw_to_dataset_features, build_dataset_frame

def manual_control():
    # Create robot config
    config = SO101FollowerConfig(
        port="/dev/tty.usbmodem58FA0962001",
        id="blue"
    )
    
    robot = None
    dataset = None
    
    try:
        # Create robot instance
        robot = SO101Follower(config)
        
        # Connect to robot with retry logic
        print("Connecting to robot...")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                robot.connect(calibrate=False)
                print("Robot connected!")
                break
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
        
        # Get current position
        current_obs = robot.get_observation()
        motor_positions = [f"{key}: {value:.2f}" for key, value in current_obs.items()]
        print(f"Current positions: {motor_positions}")
        
        # Create dataset for recording with simpler approach
        print("Creating dataset...")
        
        print("\nManual Control Started!")
        print("Controls:")
        print("- Press ENTER to record current position")
        print("- Type 'q' and press ENTER to quit")
        print("- Move the robot manually (if it's safe to do so)")
        
        frame_count = 0
        
        while True:
            try:
                user_input = input(f"Frame {frame_count + 1} - Press ENTER to record (or 'q' to quit): ")
                
                if user_input.lower() == 'q':
                    break
                
                # Try to get observation with retry
                for retry in range(3):
                    try:
                        observation = robot.get_observation()
                        break
                    except Exception as e:
                        print(f"Read attempt {retry + 1} failed: {e}")
                        if retry == 2:
                            print("Failed to read from robot after 3 attempts. Stopping.")
                            return
                        time.sleep(1)
                
                frame_count += 1
                motor_positions = [f"{key}: {value:.2f}" for key, value in observation.items()]
                print(f"Frame {frame_count} recorded - positions: {motor_positions}")
                
                # Add small delay to avoid overwhelming the connection
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\nStopping due to keyboard interrupt...")
                break
            except Exception as e:
                print(f"Error during recording: {e}")
                traceback.print_exc()
                break
        
        print(f"\nRecording completed! Total frames: {frame_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
    
    finally:
        # Safely disconnect
        if robot is not None:
            try:
                print("Disconnecting robot...")
                robot.disconnect()
                print("Robot disconnected safely.")
            except Exception as e:
                print(f"Warning: Error during disconnect: {e}")

if __name__ == "__main__":
    manual_control() 