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
  - `/import_chunk`: Accepts chunked `.tar.gz` file uploads (10MB slices) to completely bypass Home Assistant's strict 16MB Ingress request body limit. Once the final chunk is received, it extracts the backup and uses the Supervisor API to restart the Add-on automatically.

### 3. NGINX Reverse Proxy (`nginx.conf`)
NGINX acts as the gateway between Home Assistant Ingress and the internal services.
- Ports: Listens on `62899` (a non-standard port to avoid `host_network` collisions).
- Routes `/ttyd/` to the internal `ttyd` daemon on port `62898`.
- Routes all other traffic to the Python backend on port `62897`.
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
