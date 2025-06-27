#!/bin/bash
python -m lerobot.record \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem58FA0962001 \
    --robot.id=blue \
    --teleop.type=keyboard \
    --teleop.id=my_keyboard \
    --dataset.repo_id=test_user/simple_test \
    --dataset.root=./local_datasets \
    --dataset.push_to_hub=false \
    --dataset.num_episodes=1 \
    --dataset.episode_time_s=10 \
    --dataset.single_task="Simple test" 