<div align="center">
  <img src="https://raw.githubusercontent.com/Aaronhrndz/antigravity-cli-addon/main/logo.png" alt="Antigravity Logo" width="120"/>

  # Antigravity CLI Add-on for Home Assistant
  
  **The ultimate AI agent terminal designed for seamless vibecoding across any device.**
</div>

<br/>

Antigravity CLI Add-on integrates a powerful AI agent directly into your Home Assistant environment. With deep access to the Home Assistant Supervisor API and your domotics, this terminal acts as your central command for writing code, executing tasks, and managing your smart home.

What makes this add-on special is its **zero-friction mobile experience**. You can start coding a complex project on your PC, grab your phone, and seamlessly continue vibecoding on the couch with a custom mobile-first UI.

---

## ✨ Key Features

- 📱 **Built for Mobile Vibecoding**: A distraction-free UI wrapper around `ttyd` completely tailored for touch screens. Say goodbye to wonky scrolling, weird keyboard overlays, or unreadable text.
- 🗂️ **Dynamic Multi-Session Tabs**: Want to work on your Python scripts and your Lovelace dashboards at the same time? Click the `+` button in the top tab bar to dynamically spawn new AI sessions. You can switch between them instantly without losing context, and close (`x`) the ones you don't need to instantly free up memory.
- 🤖 **MCP Domotics Integration**: Automatically connects the AI agent to your home using Model Context Protocol (MCP). It can talk directly to Home Assistant and Zigbee2MQTT to control your lights, read sensors, and execute scripts using natural language.
- 🔄 **Seamless Device Transitions**: Powered by `dtach`, your terminal sessions remain persistent. You can start a process on your PC, switch to your tablet, and open it on your phone without losing your command history or interrupting running tasks.
- ⌨️ **Mobile-Optimized Macros & Controls**: Features a built-in virtual keypad specifically designed for terminal usage on mobile:
  - **High-Precision D-Pad**: Vectorized SVG arrow keys that render perfectly centered on any iOS or Android device.
  - **Terminal Essentials**: Dedicated `Esc` and `Tab` keys.
  - **Macro Actions**: Instantly execute common commands like `/resume`, `/new` (new chat) and `/quota` (check usage) with a single tap.
  - **Elegant Shortcut Badges**: Bottom footer includes styled virtual key badges for `Ctrl+C`, `Ctrl+V`, and `Ctrl+Z` that adapt cleanly to your screen. On mobile, the right-click menu is suppressed natively to prevent the browser's context menu from interrupting your workflow.
  - **Smart Login Button**: A dedicated login button appears in the bottom navigation bar when authentication is required, bypassing the need to copy text from the terminal.
- 🖼️ **Direct Image Uploads**: Need to give the AI visual context? Tap the "Upload Image" button on your phone, select a photo, and it is instantly uploaded to an ephemeral secure container directory (`/tmp/uploads`) and the path is automatically typed into your terminal prompt.
- 🔒 **Deep & Secure Integration**: Automatically bridges the AI with your Home Assistant Supervisor Token in a secure sandbox.
- 🎨 **Beautiful Aesthetics**: Complete with a dynamic mesh-gradient footer that feels right at home on modern devices.

---

## ⚠️ Important: Multi-Session Concurrency

When using the **Dynamic Multi-Session Tabs**, you will have multiple AI agents running simultaneously. 
**Avoid catastrophic file conflicts** by following this golden rule: **Do not ask two different sessions to edit the exact same file (e.g., `automations.yaml`) at the same time.** 

The AI does not natively use file locks. If Session 1 and Session 2 write to the same file simultaneously, they will create a race condition and overwrite each other's work. 
**Best Practice**: Use different tabs for entirely different files or projects (e.g., Tab 1 for `configuration.yaml`, Tab 2 for `python_scripts/`).

*Tip: If you absolutely need concurrency safety, you can instruct the agent in your prompt to "check if `.filename.lock` exists before editing, and create it while working", acting as a human-enforced semaphore.*

### ⚠️ Disclaimer
**Use at your own risk.** The authors of this add-on are not responsible for any damage, data loss, or system instability caused by the AI agents. Vibecoding with multiple autonomous agents concurrently is inherently dangerous if they are not properly isolated. It can lead to catastrophic file corruption or system misconfigurations if multiple agents attempt to modify the same configurations simultaneously without locking. **You are fully responsible for the actions the AI takes on your system.**

---

## 🚀 Installation Guide

Since this is a custom Home Assistant Add-on, you need to add this repository to your Supervisor.

### Step 1: Add the Repository
1. Open your Home Assistant web interface.
2. Navigate to **Settings** > **Add-ons** > **Add-on Store** (bottom right button).
3. Click the three dots (⋮) in the top right corner and select **Repositories**.
4. Paste the URL of this GitHub repository and click **Add**.

### Step 2: Install the Add-on
1. Close the Repositories modal.
2. Scroll down to find the newly added **Antigravity CLI** section, or search for it.
3. Click on the **Antigravity CLI** add-on and click **Install**.

### Step 3: Configuration & Start
1. Go to the **Configuration** tab to enter your integration credentials (see the Configuration Guide below).
2. Once installed, toggle on **Show in sidebar** for easy access.
3. Click **Start**.
4. Check the **Log** tab to ensure the add-on started correctly.
5. Click on the **Antigravity** icon in your sidebar to open the terminal.

---

## ⚙️ Configuration Guide

To allow the AI to interact with your smart home, you must configure the following fields in the Add-on's **Configuration** tab before starting it:

### Home Assistant Integration
- `ha_token`: **(Required)** Your Long-Lived Access Token. 
  - *How to get it:* Go to your Home Assistant Profile (bottom left corner) > Security > Long-Lived Access Tokens > Create Token. 
  - *Example:* `eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp...`

### Zigbee2MQTT Integration
These fields are used to connect the AI directly to your Zigbee network.
- `mqtt_host`: The IP address or hostname of your MQTT Broker.
  - *Example:* `core-mosquitto` (if you use the official HA Add-on) or `192.168.1.100`.
- `mqtt_port`: The port of your MQTT Broker.
  - *Example:* `1883`
- `mqtt_user`: Your MQTT username.
  - *Example:* `homeassistant`
- `mqtt_pass`: Your MQTT password.
  - *Example:* `my_secure_password`

---

## 🛡️ Security & Privacy

This add-on is designed with security in mind:
- **No Path Traversal**: Image uploads are strictly sanitized (`os.path.basename`) and securely stored in an ephemeral, non-persistent `/tmp/uploads` directory.
- **Auto-Purging**: The upload directory is automatically wiped every time the add-on restarts to prevent storage bloat and ensure privacy.
- **Sandboxed Execution**: Runs fully inside the Home Assistant Docker supervisor ecosystem.

---

<div align="center">
  <i>Supercharge your smart home with AI-driven vibecoding.</i>
</div>
# Antigravity CLI Add-on Wiki

Welcome to the internal documentation for the **Antigravity CLI** Home Assistant Add-on. 
This wiki explains the architecture, components, and key design decisions.

## Architecture Overview

The Add-on runs in a Docker container inside Home Assistant Supervisor. It exposes a web-based terminal interface with a dedicated backend.

### 1. Web Frontend (`index.html`)
The frontend is built with vanilla HTML/JS/CSS to ensure minimal overhead. It contains:
- **Terminal Viewport:** Renders the TTYD shell session via `<iframe>`.
- **Keyboard Shortcut Menu:** An on-screen menu (`#footer`) providing quick access to complex shortcuts (Ctrl+C, Ctrl+V, PgUp, /resume, etc.) essential for mobile users or quick macros.
- **Scroll Inertia Fix:** Includes a custom script to inject smooth kinetic scrolling and fix Apple/Android virtual keyboard issues within the TTYD `xterm.js` canvas.
- **Modal Overlays:** Features a full-screen `fixed` overlay (`#loader-modal`) with `backdrop-filter: blur(8px)` for blocking user interaction during critical operations (like backup/restore).

### 2. Python Backend (`upload.py`)
This is a lightweight HTTP server (`http.server`) running alongside `ttyd`. It handles:
- **File Uploads:** Intercepts image/file uploads from the UI and passes them into the current active terminal session (`/upload`).
- **Tab Management:** Allows killing terminal sessions when tabs are closed (`/kill`).
- **Self-Updating:** Pulls the latest version from GitHub automatically via `/update_cli`.
- **Backup & Restore System:**
  - `/export_backup`: Streams a `.tar.gz` archive of `root/.gemini`, `data/.gemini`, and `config/.gemini` directories directly to the network `stdout` to avoid RAM/disk exhaustion.
  - `/import_backup`: Accepts an uploaded `.tar.gz` file, stops the AI agent process, wipes the current memory, extracts the backup, and reboots the agent.

### 3. NGINX Reverse Proxy (`nginx.conf`)
NGINX acts as the gateway between Home Assistant Ingress and the internal services.
- Ports: Listens on `8099`.
- Routes `/ttyd/` to the internal `ttyd` daemon on port `7681`.
- Routes all other traffic to the Python backend on port `8000`.
- **Cache-Busting:** Crucially configured with `add_header Cache-Control "no-store, no-cache...` on the root location to prevent Home Assistant Companion apps from caching `index.html` aggressively.

### 4. Startup Script (`run.sh`)
The entrypoint script that:
1. Copies default configurations to `/opt/antigravity`.
2. Restores persistent storage from Home Assistant's `/data` volume.
3. Starts the Python backend, the Node.js AI agent, and `ttyd`.
4. Keeps everything running via a bash `wait` loop.

## Development & Testing Workflow

Because Home Assistant Supervisor caches images and Ingress caches static files, the typical development cycle is:
1. Edit code locally.
2. Push to GitHub and sync files to the local `\\addons\antigravity-cli` Samba share.
3. For Python/Shell changes: **Rebuild** the Add-on from the Supervisor panel.
4. For HTML/JS/CSS changes (Hot-swapping): Copy `index.html` directly to `/opt/antigravity/html/index.html` inside the running container and force-refresh the browser (`Ctrl+F5`).

## Roadmap & Changelog
- **Recent Update:** Integrated full Backup/Restore UI with full-screen blurred loading modals. Prevented OOM crashes by streaming the `tar` backup. Fixed mobile touch scrolling issues inside the terminal iframe.
