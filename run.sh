#!/bin/bash
set -e

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANGUAGE=en_US:en

echo "Starting Antigravity CLI Add-on..."

# Create configuration directory for MCP
mkdir -p /data/.gemini/antigravity-cli

# Configure readline for Spanish/UTF-8 character input (no meta conversion)
cat << 'EOF' > /data/.inputrc
set input-meta on
set output-meta on
set convert-meta off
EOF

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
for log in /data/session_*.log; do
  if [ -f "$log" ]; then
    tail -n 10000 "$log" > "${log}.tmp"
    mv "${log}.tmp" "$log"
  fi
done
export COLORTERM=truecolor
export TERM=xterm-256color
export PAGER=cat

# Run ttyd connected to the attach script
# Generate mcp.json for Antigravity CLI
echo "Configuring MCP Servers..."
HA_TOKEN=$(jq -r '.ha_token // empty' /data/options.json)
MQTT_HOST=$(jq -r '.mqtt_host // empty' /data/options.json)
MQTT_PORT=$(jq -r '.mqtt_port // "1883"' /data/options.json)
MQTT_USER=$(jq -r '.mqtt_user // empty' /data/options.json)
MQTT_PASS=$(jq -r '.mqtt_pass // empty' /data/options.json)

mkdir -p /homeassistant

cat << 'EOF' > /homeassistant/mcp.json
{
  "mcpServers": {}
}
EOF

if [ -n "$HA_TOKEN" ]; then
    echo "Adding Home Assistant MCP server..."
    jq '.mcpServers.homeassistant = {"command": "npx", "args": ["-y", "mcp-server-home-assistant"], "env": {"HA_URL": "http://supervisor/core", "HA_TOKEN": "'"$HA_TOKEN"'"}}' /homeassistant/mcp.json > /tmp/mcp.json && mv /tmp/mcp.json /homeassistant/mcp.json
fi

if [ -n "$MQTT_HOST" ]; then
    echo "Adding Zigbee2MQTT MCP server..."
    MQTT_URL="mqtt://${MQTT_HOST}:${MQTT_PORT}"
    jq --arg url "$MQTT_URL" --arg user "$MQTT_USER" --arg pass "$MQTT_PASS" '.mcpServers.zigbee2mqtt = {"command": "npx", "args": ["-y", "mcp-server-zigbee2mqtt"], "env": {"MQTT_URL": $url, "MQTT_USERNAME": $user, "MQTT_PASSWORD": $pass}}' /homeassistant/mcp.json > /tmp/mcp.json && mv /tmp/mcp.json /homeassistant/mcp.json
fi

# Set the environment variable so agy picks up the MCP configuration
export MCP_CONFIG_PATH=/homeassistant/mcp.json

# Using disableResizeOverlay=true -t scrollback=100000 removes the annoying 100x40 banner
ttyd -a -b /ttyd -t enableZmodem=true -t disableLeaveAlert=true -t disableResizeOverlay=true -t scrollback=100000 -t 'theme={"background": "#2b2b2b"}' -p 62898 /opt/antigravity/attach.sh &

echo "Starting NGINX reverse proxy on port 62899..."
exec nginx -c /etc/nginx/nginx.conf -g "daemon off;"
