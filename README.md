# Antigravity CLI - Home Assistant Add-on

![Antigravity Logo](https://raw.githubusercontent.com/Aaronhrndz/antigravity-cli-addon/main/logo.png)

Antigravity CLI is an advanced AI Agent environment packed into a native Home Assistant Add-on. It provides total control over your domotics, configurations, and systems through the Home Assistant Supervisor API directly from a powerful web-based terminal interface.

## Features

- **Web-based Terminal**: Powered by `ttyd`, giving you a fully featured terminal directly within the Home Assistant UI via Ingress.
- **Session Persistence**: Built on top of `tmux` to guarantee that your agent's processes, sessions, and screen layouts are preserved even if you close the browser tab.
- **Multi-Tab Support**: Run multiple isolated AI sessions or environments concurrently with a slick, Chrome-like tabbed UI.
- **Vibecoding Optimized UI**: A mobile-first, responsive custom interface overlaid on the terminal that includes macro buttons (`/resume`, `/new`, `/quota`) and quick keyboard shortcuts (`Ctrl+C`, `Ctrl+V`, `Ctrl+Z`) to operate flawlessly on touch screens.
- **Native MCP Integration**: Dynamically generates `mcp.json` to expose the Home Assistant and Zigbee2MQTT ecosystems directly to the AI, giving it immediate context of your house.
- **File Uploads**: Drag and drop images or files into the terminal window to upload them to the ephemeral storage, automatically pasting their paths into the prompt.
- **Smooth Mobile Scrolling**: Features a custom momentum physics engine providing 120Hz-smooth scrolling on mobile devices without relying on native scrollbars that break the terminal view.
- **One-Click Updates**: Embedded updater banner that alerts you of new versions and installs them with a single click inside the terminal overlay.

## Installation

1. Navigate to **Settings > Add-ons > Add-on Store** in your Home Assistant instance.
2. Click the 3 dots in the top right corner and select **Repositories**.
3. Add this repository URL: `https://github.com/Aaronhrndz/antigravity-cli-addon`
4. Find **Antigravity CLI** in the store and click **Install**.
5. Go to the Configuration tab and verify the settings (MQTT, tokens, etc.).
6. Click **Start**.
7. Click **Open Web UI** or check the "Show in sidebar" option for easy access.

## Configuration

The add-on requires minimal configuration. Most values can be left as default:

- `ha_token`: (Optional) Long-lived access token for Home Assistant API. If left empty, it will use the Supervisor's internal token automatically.
- `mqtt_host`: Your MQTT broker host (defaults to `core-mosquitto`).
- `mqtt_port`: MQTT port (defaults to `1883`).
- `mqtt_user`: MQTT username (defaults to `addons`).
- `mqtt_pass`: MQTT password.

*These variables are injected securely into the container and fed into the AI's MCP configuration.*

## Keyboard Shortcuts & Mobile Controls

The custom web UI includes a footer designed for quick interactions:
- **Logo Button**: Toggles the advanced keyboard shortcuts grid (Arrows, F-keys, Home, End).
- **COPY / PASTE**: Dedicated visual badges to indicate quick copy/paste shortcuts. Note: On mobile devices, right-clicking (long press) is natively passed to the terminal to avoid interfering with the browser's context menu.
- **Tab & Esc**: Dedicated buttons in the center of the screen to quickly send Tab completions and Escape characters to the CLI.

## License

This project is licensed under the MIT License.
