#!/usr/bin/env python3

import time
import traceback
from lerobot.common.robots.so101_follower import SO101Follower, SO101FollowerConfig

def replay_manual_recording():
    # The positions we recorded manually (from the previous session)
    recorded_positions = [
        {'shoulder_pan.pos': 3.30, 'shoulder_lift.pos': 97.83, 'elbow_flex.pos': -16.91, 'wrist_flex.pos': 17.91, 'wrist_roll.pos': 99.32, 'gripper.pos': 0.41},
        {'shoulder_pan.pos': 17.91, 'shoulder_lift.pos': 21.96, 'elbow_flex.pos': -100.00, 'wrist_flex.pos': 17.44, 'wrist_roll.pos': 99.75, 'gripper.pos': 0.48},
        {'shoulder_pan.pos': 18.12, 'shoulder_lift.pos': 100.00, 'elbow_flex.pos': -100.00, 'wrist_flex.pos': 18.01, 'wrist_roll.pos': 99.75, 'gripper.pos': 0.41},
        {'shoulder_pan.pos': 18.12, 'shoulder_lift.pos': 100.00, 'elbow_flex.pos': -100.00, 'wrist_flex.pos': -77.06, 'wrist_roll.pos': 99.32, 'gripper.pos': 0.41},
        {'shoulder_pan.pos': -42.54, 'shoulder_lift.pos': 100.00, 'elbow_flex.pos': -100.00, 'wrist_flex.pos': -77.34, 'wrist_roll.pos': 99.32, 'gripper.pos': 0.41},
        {'shoulder_pan.pos': 15.99, 'shoulder_lift.pos': 100.00, 'elbow_flex.pos': -16.18, 'wrist_flex.pos': -76.96, 'wrist_roll.pos': 99.32, 'gripper.pos': 1.10},
        {'shoulder_pan.pos': 70.58, 'shoulder_lift.pos': 100.00, 'elbow_flex.pos': -16.27, 'wrist_flex.pos': -76.77, 'wrist_roll.pos': 99.66, 'gripper.pos': 1.03},
        {'shoulder_pan.pos': -38.38, 'shoulder_lift.pos': 100.00, 'elbow_flex.pos': -16.27, 'wrist_flex.pos': -3.34, 'wrist_roll.pos': 99.32, 'gripper.pos': 1.03},
        {'shoulder_pan.pos': -37.53, 'shoulder_lift.pos': 36.16, 'elbow_flex.pos': -15.72, 'wrist_flex.pos': -3.24, 'wrist_roll.pos': 99.49, 'gripper.pos': 1.03},
        {'shoulder_pan.pos': 10.55, 'shoulder_lift.pos': 36.34, 'elbow_flex.pos': -15.53, 'wrist_flex.pos': -3.24, 'wrist_roll.pos': 99.58, 'gripper.pos': 1.03},
        {'shoulder_pan.pos': -34.65, 'shoulder_lift.pos': -8.88, 'elbow_flex.pos': -15.44, 'wrist_flex.pos': -3.24, 'wrist_roll.pos': 99.58, 'gripper.pos': 1.03},
        {'shoulder_pan.pos': -55.22, 'shoulder_lift.pos': 37.55, 'elbow_flex.pos': -1.38, 'wrist_flex.pos': -3.24, 'wrist_roll.pos': 99.58, 'gripper.pos': 1.03}
    ]
    
    # Create robot config
    config = SO101FollowerConfig(
        port="/dev/tty.usbmodem58FA0962001",
        id="blue"
    )
    
    robot = None
    
    try:
        # Create robot instance
        robot = SO101Follower(config)
        
        # Connect to robot
        print("Connecting to robot...")
        robot.connect(calibrate=False)
        print("Robot connected!")
        
        # Get current position
        current_obs = robot.get_observation()
        motor_positions = [f"{key}: {value:.2f}" for key, value in current_obs.items()]
        print(f"Starting positions: {motor_positions}")
        
        print(f"\nReplaying {len(recorded_positions)} recorded positions...")
        print("Press Ctrl+C to stop at any time")
        
        # Play back each recorded position
        for i, target_position in enumerate(recorded_positions):
            print(f"\nMoving to position {i+1}/{len(recorded_positions)}...")
            
            # Send the recorded position as an action
            try:
                sent_action = robot.send_action(target_position)
                print(f"Target: {[f'{k}: {v:.2f}' for k, v in target_position.items()]}")
                
                # Wait a bit for the robot to move
                time.sleep(2.0)
                
                # Check current position
                current_obs = robot.get_observation()
                current_positions = [f"{key}: {value:.2f}" for key, value in current_obs.items()]
                print(f"Current: {current_positions}")
                
            except Exception as e:
                print(f"Error sending action {i+1}: {e}")
                break
        
        print("\nReplay completed!")
        print("Press ENTER to continue...")
        input()
        
    except KeyboardInterrupt:
        print("\nReplay stopped by user.")
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
    replay_manual_recording() 