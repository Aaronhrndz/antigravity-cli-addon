#!/bin/bash
set -e

echo "Starting Antigravity CLI Add-on..."

# Create configuration directory for MCP
mkdir -p /data/.gemini/antigravity-cli

# Create mcp_config.json pointing to Supervisor API
cat << JSON > /data/.gemini/antigravity-cli/mcp_config.json
{
  "mcpServers": {
    "homeassistant": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-everything"],
      "env": {
        "HA_URL": "http://supervisor/core/api",
        "HA_TOKEN": "${SUPERVISOR_TOKEN}"
      }
    }
  }
}
JSON

echo "Configured MCP server with Supervisor Token."
echo "Starting ttyd on port 8099..."

exec ttyd -p 8099 bash
