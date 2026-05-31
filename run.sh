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
exec ttyd -W -p 8099 /usr/local/bin/agy
