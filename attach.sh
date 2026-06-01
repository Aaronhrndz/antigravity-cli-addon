#!/bin/bash
SESSION_ID=${1:-1}

# Attach to existing session or create a new one with agy
# dtach -A: attach if socket exists, create if not
# dtach -r winch: force terminal redraw on re-attach
exec dtach -A /tmp/agy_${SESSION_ID}.socket -r winch /usr/local/bin/agy
