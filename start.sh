#!/bin/bash
# Start NGINX
nginx

# Truncate session log to last 1000 lines to prevent infinite growth
if [ -f /data/session.log ]; then
    tail -n 1000 /data/session.log > /tmp/session.log.tmp
    mv /tmp/session.log.tmp /data/session.log
fi

# Clean up old socket
rm -f /tmp/agy.socket

# Start dtach with script in the background
# script -f flushes output, -q is quiet, -a appends to the log
dtach -n /tmp/agy.socket script -q -f -a /data/session.log -c "/usr/local/bin/agy" &

# Start ttyd
exec ttyd -p 8098 -t disableLeaveAlert=true -t disableResizeOverlay=true /opt/antigravity/attach.sh
