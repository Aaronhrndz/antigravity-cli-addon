# Changelog

All notable changes to the Antigravity CLI Home Assistant Add-on will be documented in this file.

## [1.7.7] (Current)
### Added
- MCP Integration with dynamically generated `mcp.json` for Home Assistant and Zigbee2MQTT.
- Added translation support for configuration UI hints (`translations/`).
- Added a new `/resume` macro button to quickly resume workflows.
- Implemented elegant keyboard shortcut badges (`<kbd>`) in the UI footer for `Ctrl+Shift+C` and `Ctrl+Shift+V`.

### Changed
- Improved context menu logic: Right-click now suppresses the Chrome context menu without triggering the visual grid menu, allowing native terminal apps to handle right-clicks properly.
- Reordered keyboard shortcuts in the UI to `Ctrl+C`, `Ctrl+V`, `Ctrl+Z`, and `/resume`.
- Refined and improved layout spacing for mobile devices.

### Fixed
- Fixed bug causing the Chrome browser context menu to overlay and close the terminal menu.
- Restored `contextmenu` event listeners inside the `iframe` document.

## [1.7.4]
### Changed
- Reverted TERM to `xterm-256color` and added auto-restart loops to prevent the CLI from hanging.
- Re-architected Telegram Bridge: Completely removed fragmented output and splash screens using a synchronous expect mechanism.
- Improved ANSI parsing and buffering in the Telegram bridge for native plain text messages instead of markdown blocks.
- Spawns Telegram integration in a completely isolated CLI session.
- Switched back from `dtach` to `tmux` for proper persistent session state and reliable screen redraws.

### Fixed
- Fixed absolute GitHub raw URLs for logos in the UI.
- Fixed UTF-8 character encoding issues using the `locales` package and `.inputrc` configurations.
- Handled carriage return inputs and prompt-filtering in Telegram output gracefully.

## [1.4.0] (Stability Release)
### Added
- Dynamic Multi-Session Tabs UI allowing multiple concurrent terminal tabs.
- Lazy session spawning: terminals are only instantiated when their tab is opened.
- In-app update banner with a one-click CLI updater.
- Added visual macro buttons for `/new` and `/quota` replacing legacy commands.

### Changed
- Overhauled responsive design for mobile (vibecoding focused) with fluid flex layouts, hidden logos on narrow screens, and touch-optimized buttons.
- Transitioned upload button styling to the Antigravity brand blue-purple-red mesh gradient.
- Optimized momentum touch-scrolling engine for 120Hz mobile displays.

### Fixed
- Resolved jumping to top bugs on mobile when the keyboard closes or the window resizes.
- Fixed blank screen syntax errors.

## [1.0.3] (Initial Release)
### Added
- Initial Dockerfile based on `debian:12-slim` running `ttyd`.
- Mapped Home Assistant `/config` and `/share` volumes.
- Automatic Home Assistant Token injection.
- Fully working Ingress reverse-proxy configuration.
