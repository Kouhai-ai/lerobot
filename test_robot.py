#!/usr/bin/env python3

from lerobot.common.robots.so101_follower import SO101Follower, SO101FollowerConfig

def test_robot():
    # Create robot config
    config = SO101FollowerConfig(
        port="/dev/tty.usbmodem58FA0962001",
        id="blue"
    )
    
    # Create robot instance
    robot = SO101Follower(config)
    
    try:
        # Connect to robot
        print("Connecting to robot...")
        robot.connect(calibrate=False)  # Don't calibrate since we already did
        print("Robot connected!")
        
        # Check if calibrated
        print(f"Robot calibrated: {robot.is_calibrated}")
        
        # Try to read observation
        print("Reading observation...")
        obs = robot.get_observation()
        print(f"Observation keys: {list(obs.keys())}")
        print(f"Motor positions: {[f'{k}: {v:.2f}' for k, v in obs.items() if k.endswith('.pos')]}")
        
        # Try to send a simple action (stay in current position)
        print("Sending action...")
        current_pos = {k: v for k, v in obs.items() if k.endswith('.pos')}
        sent_action = robot.send_action(current_pos)
        print(f"Action sent successfully: {sent_action}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if robot.is_connected:
            robot.disconnect()
            print("Robot disconnected")

if __name__ == "__main__":
    test_robot() 