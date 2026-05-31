#!/bin/bash
# If session log exists, print it so xterm.js gets the scrollback history
if [ -f /data/session.log ]; then
    cat /data/session.log
fi

# Attach to the running dtach session
exec dtach -a /tmp/agy.socket
