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

- 📱 **Mobile-First Vibecoding with Adaptive Docking**: A distraction-free UI wrapper around `ttyd` designed for mobile screens. Features adaptive toolbar docking (positioned on TOP above session tabs on mobile by default) so virtual keyboards never obstruct terminal inputs or buttons.
- 🌍 **Full Multi-Language Support (i18n)**: Automatically localizes the interface according to your Home Assistant or browser language (English by default, Spanish, German, French, Italian, Portuguese).
- 🌓 **Dynamic Theme System**: Seamlessly switch between Dark, Light (sunlight high-contrast with `#2188ff` selection), and Auto (syncs automatically with Home Assistant theme changes).
- 🗂️ **Dynamic Multi-Session Tabs**: Spawn new AI sessions with 1 click (`+`) without reloading or losing memory context. Switch instantly between active conversations.
- 🤖 **MCP Domotics Integration**: Automatically connects the AI agent to your home using Model Context Protocol (MCP) to control lights, inspect sensors, and run automations via natural language.
- 🔄 **Seamless Persistence & 50k History**: Powered by `tmux`, your terminal sessions stay live across reconnects with 50,000 lines of scrollback and native mouse/touch selection.
- 🔑 **1-Click Copy Auth Link**: Auto-detects and extracts multiline Google OAuth login URLs from terminal canvas and cleans up line-break split artifacts.
- 📦 **Optimized Light Backups**: Instant full config exports (<15 MB) preserving 100% of agent memory, skills, and past chat histories.
- ⌨️ **Mobile Macros & Virtual D-Pad**: High-precision SVG arrow keys, dedicated `Esc`/`Tab` keys, one-tap command macros (`/resume`, `/new`, `/quota`, `/model`), and clipboard helpers.
- 🖼️ **Direct Image Uploads**: Upload photos directly from your phone; images are saved securely to `/tmp/uploads` and their paths are pasted into the terminal automatically.
- 🔒 **Deep & Secure Integration**: Securely sandboxed integration with Home Assistant Supervisor Token API.

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

## 📚 Documentation
For detailed information about the internal architecture, UI design, and development workflows, please see the [Antigravity Wiki](WIKI.md).
