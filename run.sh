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
echo "Starting ttyd on port 8099 with Antigravity CLI..."

# Run the CLI
export COLORTERM=truecolor
export TERM=xterm-256color
exec ttyd -t lineHeight=1.0 -t "fontFamily='Cascadia Code', 'Consolas', 'Liberation Mono', monospace" -t "theme={'background': '#0c0c0c'}" -p 8099 tmux new-session -A -s antigravity /usr/local/bin/agy
