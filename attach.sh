#!/bin/bash
SESSION_ID=${1:-1}

# If session log exists, print it so xterm.js gets the scrollback history
if [ -f /data/session_${SESSION_ID}.log ]; then
    cat /data/session_${SESSION_ID}.log
fi

# Attach to the running dtach session, or create it if it doesn't exist
exec dtach -A /tmp/agy_${SESSION_ID}.socket script -q -f -a /data/session_${SESSION_ID}.log -c "/usr/local/bin/agy"
