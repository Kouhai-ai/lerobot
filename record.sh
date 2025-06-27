python -m lerobot.record \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem58FA0962001 \
    --robot.cameras="{laptop: {type: opencv, camera_index: 0, width: 640, height: 480}}" \
    --robot.id=blue \
    --dataset.repo_id=aliberts/record-test \
    --dataset.num_episodes=2 \
    --dataset.single_task="Grab the cube" \