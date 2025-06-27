python -m lerobot.teleoperate \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem58FA0962001 \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 1920, height: 1080, fps: 30}}" \
    --robot.id=blue \
    --teleop.type=so101_follower \
    --teleop.port=/dev/tty.usbmodem58FA0962001 \
    --teleop.id=blue \
    --display_data=true