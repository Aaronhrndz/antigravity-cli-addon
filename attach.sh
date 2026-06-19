#!/bin/bash
export TERM=xterm-256color
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US:en

chmod +x /opt/antigravity/run_agy.sh

SESSION_ID=${1:-default}
exec tmux -f /etc/tmux.conf new-session -A -s agy_$SESSION_ID "/opt/antigravity/run_agy.sh"
