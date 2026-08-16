#!/bin/bash
unset GODEBUG
sleep 0.5
exec /usr/local/bin/agy "$@"
