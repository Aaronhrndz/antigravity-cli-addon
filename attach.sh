#!/bin/bash
SESSION_ID=${1:-1}
SESSION_LOG="/data/session_${SESSION_ID}.log"
SOCKET="/tmp/agy_${SESSION_ID}.socket"

export TERM=xterm-256color
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US:en

# Siempre imprime el historial completo al conectar
if [ -f "$SESSION_LOG" ]; then
    cat "$SESSION_LOG"
fi

exec dtach -A "$SOCKET" -r winch /usr/bin/script -q -f -a "$SESSION_LOG" -c "/usr/local/bin/agy"
