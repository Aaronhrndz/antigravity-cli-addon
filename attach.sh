#!/bin/bash
SESSION_ID=${1:-1}
SESSION_NAME="agy_${SESSION_ID}"

# tmux config: no status bar, truecolor support
export TERM=xterm-256color
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US:en

# If session exists, attach to it. Otherwise, create it.
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    exec tmux attach-session -t "$SESSION_NAME"
else
    exec tmux new-session -s "$SESSION_NAME" \
        -e "COLORTERM=truecolor" \
        -e "TERM=xterm-256color" \
        -e "LANG=en_US.UTF-8" \
        -e "LC_ALL=en_US.UTF-8" \
        -e "LANGUAGE=en_US:en" \
        /usr/local/bin/agy
fi
