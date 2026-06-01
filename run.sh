#!/bin/bash
set -e

echo "Starting Antigravity CLI Add-on..."

# Create configuration directory for MCP
mkdir -p /data/.gemini/antigravity-cli

# Create mcp_config.json pointing to our lightweight local bridge
cat << JSON > /data/.gemini/antigravity-cli/mcp_config.json
{
  "mcpServers": {
    "homeassistant": {
      "command": "node",
      "args": ["/config/mcp_bridge.js"]
    }
  }
}
JSON

echo "Configured MCP server with Supervisor Token."

# Get Ingress URL for ttyd
INGRESS_URL=$(curl -s -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" http://supervisor/addons/self/info | jq -r '.data.ingress_url')

# If INGRESS_URL ends with /, remove it (ttyd doesn't expect trailing slash in base path)
INGRESS_URL=${INGRESS_URL%/}

echo "Ingress URL is $INGRESS_URL"
# Start Python Upload server on port 8097
python3 /opt/antigravity/upload.py &

# Run the CLI via dtach to support session persistence natively without alternate screen (perfect mobile scrolling)
export COLORTERM=truecolor
export TERM=xterm-256color

# Keep log small
if [ -f /data/session.log ]; then
    tail -n 1000 /data/session.log > /tmp/session.log.tmp
    mv /tmp/session.log.tmp /data/session.log
fi

# Clean socket
rm -f /tmp/agy.socket

# Start dtach background process recording to session.log
dtach -n /tmp/agy.socket script -q -f -a /data/session.log -c "/usr/local/bin/agy" &

# Run ttyd connected to the attach script
# Using disableResizeOverlay=true removes the annoying 100x40 banner
ttyd -b /ttyd -t enableZmodem=true -t disableLeaveAlert=true -t disableResizeOverlay=true -t "theme={'background': '#000000'}" -p 8098 /opt/antigravity/attach.sh &

# Check and start Telegram Bridge
TELEGRAM_TOKEN=$(jq -r '.telegram_bot_token // empty' /data/options.json)
TELEGRAM_CHAT_ID=$(jq -r '.telegram_chat_id // empty' /data/options.json)
if [ -n "$TELEGRAM_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    echo "Starting Telegram Bridge..."
    export TELEGRAM_BOT_TOKEN="$TELEGRAM_TOKEN"
    export TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID"
    python3 /opt/antigravity/telegram_bridge.py &
fi

echo "Starting NGINX reverse proxy on port 8099..."
exec nginx -c /etc/nginx/nginx.conf -g "daemon off;"
