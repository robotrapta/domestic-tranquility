#!/bin/bash

set -ex

/usr/bin/tmux new-session -d -s glapp '/home/leodirac/ptdev/domestic-tranquility/launch.sh' >> /tmp/tmux_cron.log 2>&1


