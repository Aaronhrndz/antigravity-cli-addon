#!/bin/bash
SESSION_ID=${1:-1}
SESSION_NAME="agy_${SESSION_ID}"

export TERM=xterm-256color
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US:en

# Start or attach to tmux session cleanly using /etc/tmux.conf
exec tmux -f /etc/tmux.conf new-session -A -s "$SESSION_NAME" "/usr/local/bin/agy"

