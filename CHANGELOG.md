## [1.8.6]
- fix: Make touch scroll listener robust to DOM recreation by tracking dataset instead of clearing interval
- fix: Change dtach redraw method to 'winch' to prevent clearing of terminal scrollback buffer on reconnect
- fix: Re-add check for session log existence before printing history on connect
- fix: Use proper dtach syntax (dtach -A socket -r mode)

## [1.8.5]
- feat: Remove tmux completely and revert to dtach + script for perfect native scroll and session persistence without alternate screen buffer conflicts
- chore: Remove ResizeObserver polling that interfered with scroll tracking

## [1.8.4]
- revert: Reverted to tmux implementation temporarily during diagnostic phase
## [1.8.6] - 2026-06-03
### Fixed
- Fixed critical mobile scroll bug by completely reverting terminal core from tmux back to dtach+script while maintaining full multi-tab support.
- Fixed a bug where closing the Android keyboard caused the terminal to snap to the top instead of the bottom by unconditionally enforcing multiple timed scroll resets.
- Fixed an issue where the contextual extra keys menu would remain open after interacting with a tool button.
- Cleaned up Dockerfile missing dependencies from the tmux-to-dtach migration.
# Changelog

## [1.8.3]
- fix: reduce backup upload chunk size to 10MB to comply with Home Assistant Ingress hard 16MB request body limit

## [1.8.2]
- feat: implement 100MB chunked multipart uploads to bypass Home Assistant Ingress timeout and memory limits for massive backups

## [1.8.1]
- fix: change internal proxy ports to 62897-62899 to avoid host_network conflicts
- fix: remove nginx client_max_body_size limit for large backups
## [1.8.0]
- feat: Full Backup and Restore system with blurred UI modals
- feat: Streaming tar export and import to prevent RAM/disk exhaustion
- feat: Add Wiki and Documentation architecture
- fix: Correct touch physics and UI button scaling
- fix: Remove contextMenu blocks preventing proper desktop interaction
All notable changes to the Antigravity CLI Home Assistant Add-on will be documented in this file.

## [1.7.8]
- chore: release v1.7.8 with Import/Export Backup tool
- docs: remove localdev references from changelog
- feat: implement automatic addon restart on successful backup restore
- feat: add Import/Export backup tool for agent memory and addon configs
- docs: use python script to generate full chronological changelog with all version tags
- docs: restore rich README.md and write exhaustive CHANGELOG.md
- docs: generate comprehensive README and CHANGELOG
- style: use kbd badges for shortcut legend
- style: capitalize copy and paste shortcut labels
- style: reorder buttons to CtrlC, CtrlV, CtrlZ, /resume
- style: increase /resume font size
- feat: remove F1-F5 and Ctrl+D, add /resume button
- fix: remove toggleContextMenu from right click so it just blocks browser menu without opening shortcut grid
- fix: restore contextmenu event listener inside iframe
- fix: restore contextmenu event listener
- style: perfectly center shortcut text in its gap
- style: increase size of shortcut text
- style: make shortcut text smaller and hide on mobile
- style: revert shortcuts to context menu and remove separators
- fix: restore localdev version
- feat: add copy/paste text info and move shortcuts to footer
- fix: move paste to context menu and fix shortcut events
- fix: shortcut buttons and paste functionality
- revert: allow native context menu again

## [1.7.7]
- revert: remove google login url capture and banner
- fix: suppress native context menu
- fix: broaden google login url regex

## [1.7.6]
- chore: bump version to 1.7.6 and add footer login button
- Add CHANGELOG.md to display release notes in Home Assistant UI

## [1.7.5]
- Implement dynamic Google Login floating action button in frontend and tmux capture-pane endpoint in backend
- Fix logo.png path in README to use absolute raw GitHub URL

## [1.7.4]
- Fix character encoding, add locales package, configure .inputrc for UTF-8 support and bump version to 1.7.4

## [1.7.1]
- feat: Add configuration translations for UI hints and update default placeholders in config.yaml
- docs: Update README with Configuration Guide for MCP integration and remove outdated Telegram references

## [1.7.0]
- feat: Add MCP integration for Home Assistant and Zigbee2MQTT via dynamically generated mcp.json

## [1.6.2]
- style: Restore the original logo.png in the footer instead of the SVG triangle

## [1.6.1]
- chore: Remove Telegram bridge integration completely

## [1.6.0]
- refactor: Telegram bridge now uses synchronous expect, eliminating splash screens and fragmented output completely

## [1.5.6]
- fix: Don't discard the entire message buffer if it ends with a prompt

## [1.5.5]
- fix: Revert TERM to xterm-256color and add auto-restart to prevent CLI from crashing/hanging

## [1.5.4]
- fix: Send native Telegram text instead of markdown blocks, adjust timeout and filter empty prompts

## [1.5.3]
- fix: Robust ANSI parsing, carriage return handling, and buffering for Telegram bridge

## [1.5.2]
- feat: Telegram bridge now spawns its own isolated CLI session

## [1.5.1]
- fix: Pass -a to ttyd to enable URL arguments (fixes tab isolation), and restore SVG logo with context menu

## [1.5.0]
- feat: Replace dtach with tmux for proper session persistence and screen redraw

## [1.4.19]
- fix: Simplify attach.sh (remove script/cat) and fix scroll timing

## [1.4.18]
- debug: Add visible session ID output to attach.sh

## [1.4.17]
- fix: Remove aggressive auto-scroll that hides CLI splash on load

## [1.4.16]
- fix: Resolve SyntaxError causing blank terminal on init

## [1.4.15]
- feat: Add extra keyboard shortcuts context menu

## [1.4.14]
- style: Replace upload button with minimalist image icon

## [1.4.13]
- style: Restore footer buttons background and remove footer shadow

## [1.4.12]
- style: Make Esc and Tab buttons bold

## [1.4.11]
- style: Match tab bar background to footer

## [1.4.10]
- style: Change entire theme base to #2b2b2b for cohesive aesthetic

## [1.4.9]
- style: Change footer buttons background to match tab bar

## [1.4.8]
- fix: Parse ttyd JSON theme correctly to force absolute black terminal

## [1.4.7]
- fix: Ensure exact terminal background match and remove all inactive tab borders

## [1.4.6]
- style: Clean up footer borders and add true Chrome tabs

## [1.4.5]
- feat: Add in-app update banner and one-click updater for CLI
- chore: Add MIT License

## [1.4.4]
- style: Update tabs to match Google Chrome dark mode aesthetic
- docs: Add disclaimer for liability and multi-agent concurrency risks
- fix: Translate tabs to English

## [1.4.2]
- feat: Dynamic Multi-Session Tabs UI and Lazy session spawning

## [1.4.1]
- feat: Experimental Telegram Bot integration

## [1.4.0]
- Bump version to 1.4.0 for stability release

## [1.3.44]
- Increase button sizes on mobile and adjust gaps using flex to fill the available space evenly

## [1.3.43]
- Restore logo on mobile, shrink tool buttons, and override inline margins using !important in mobile media query

## [1.3.42]
- Optimize footer layout for mobile by hiding logo, reducing gaps and margin width

## [1.3.41]
- Fix vertical alignment of the plus icon in the /new button SVG
- Update README with detailed features, mobile vibecoding focus, and installation guide

## [1.3.40]
- Change macro buttons to use icons, remove /mod, and auto-press Enter by using carriage return \r

## [1.3.39]
- Add /quota macro button

## [1.3.38]
- Add macro buttons for /new and /mod commands

## [1.3.37]
- Remove Ctrl+C and Ctrl+D buttons as they are not needed for a monopolized CLI environment

## [1.3.36]
- Add Ctrl+D button next to Ctrl+C for closing shells/EOF

## [1.3.35]
- Replace Unicode arrows with consistent SVG icons to fix mobile rendering misalignment

## [1.3.34]
- Use ellipses to blend the mesh gradient smoothly and remove the hard orange dot

## [1.3.33]
- Soften the orange color to create a more natural transition from yellow to red

## [1.3.32]
- Unify arrow keys font family and size to 24px Arial to prevent mobile rendering discrepancies

## [1.3.31]
- Adjust radial gradients to let blue base predominate more from the bottom

## [1.3.30]
- Update upload button to use a smooth radial mesh gradient with dominant bottom blue

## [1.3.29]
- Update upload button to use an exact 3-band horizontal gradient matching the logo

## [1.3.28]
- Update upload button gradient and save files to ephemeral addon storage with auto-paste logic

## [1.3.27]
- Update upload button color to Antigravity blue-purple gradient

## [1.3.26]
- Increase font size of arrow keys for better visibility on mobile

## [1.3.25]
- Add Esc button to toolbar for exiting modes in terminal

## [1.3.24]
- Update upload button to say Upload Image in stacked text with smaller font

## [1.3.23]
- Add spacing between button groups for better usability

## [1.3.22]
- Update tool-btn labels to Tab and ^C for better UX

## [1.3.21]
- Disable predictive text (autocomplete, autocorrect, spellcheck) on the terminal textarea to fix duplicate keystrokes on mobile

## [1.3.20]
- Fix layout sizing issues, move header to footer, remove text next to logo, keep arrows on desktop

## [1.3.19]
- Fix mobile toolbar by moving it into the top header next to the upload button

## [1.3.18]
- Add mobile toolbar for quick key commands

## [1.3.17]
- Fix resize scrolling bug to preserve scroll position if not at bottom

## [1.3.16]
- Fix momentum by preventing touchcancel and using window.requestAnimationFrame. Add panel_icon to config.yaml

## [1.3.14]
- Fix syntax error causing physics failure and 100vh height issue

## [1.3.13]
- Fix momentum scroll physics by using a robust 100ms sample window instead of naive instant velocity decay

## [1.3.12]
- Implement intelligent DOM MutationObserver to hide resize banners and auto-reconnect WebSocket on disconnect

## [1.3.11]
- Fix resize overlay CSS selector (targets div:not([class]) because older ttyd uses no inline styles)

## [1.3.10]
- Fix resize overlay CSS selector (targets inline styles since ttyd creates it without class or id)

## [1.3.9]
- Hide resize overlay via CSS injection

## [1.3.8]
- Force scroll to bottom on load and window resize (keyboard close) to prevent jumping to top

## [1.3.7]
- Fix momentum physics for 120Hz displays by implementing frame-rate independent time delta tracking
- Update README with latest features

## [1.3.6]
- Use scrollTop manipulation instead of WheelEvents for pixel-smooth touch scroll

## [1.3.5]
- Revert to momentum JS engine with refined physics (0.95 friction, 15px/line)

## [1.3.4]
- Fix white screen: use passive event interceptors instead of cloneNode

## [1.3.3]
- Replace JS physics engine with native CSS touch scrolling via xterm-viewport

## [1.3.2]
- Implement momentum physics engine for native-feel touch scrolling

## [1.3.1]
- Fix Dockerfile reference to deleted start.sh

## [1.3.0]
- Replace tmux with dtach+script for perfect native mobile scrolling

## [1.2.10]
- Hide tmux status bar and refine touch scroll logic

## [1.2.9]
- Update sidebar icon to Antigravity logo (triangle-outline)

## [1.2.8]
- Add touch-to-scroll translation for mobile devices

## [1.2.7]
- Create unified /homeassistant directory structure

## [1.2.6]
- Enable mouse scrolling in tmux

## [1.2.5]
- Change working directory to /config and map Home Assistant volumes

## [1.2.4]
- Fix relative paths for ingress

## [1.2.3]
- Fix proxy path, translate UI to english, and fix logo

## [1.2.1]
- Fix nginx duplicate daemon directive crash

## [1.2.0]
- Implement custom UI with image upload and fix font rendering

## [1.1.2]
- Enable Zmodem for file upload and fix font rendering issues

## [1.1.1]
- Use tmux for session persistence and sharing

## [1.1.0]
- Add font family and theme to ttyd to fix block character gaps

## [1.0.9]
- Force COLORTERM=truecolor to fix Antigravity logo rendering

## [1.0.8]
- Remove -W flag from ttyd call in run.sh as it is not supported in ttyd 1.6.3

## [1.0.7]
- Switch to ubuntu:22.04 base image to fix ttyd and glibc support

## [1.0.6]
- Switch to debian:12-slim base image to fix glibc incompatibility

## [1.0.5]
- Fix Ingress 404/WebSockets by removing ttyd base-path and update MCP config
- Update Antigravity icon to official brand image
- Add Antigravity (Gemini) icon and logo
- Fix volume shadowing and ingress base path
- Make ttyd writable
- Fix Alpine musl detection for AI CLI installation

## [1.0.3]
- Initial commit: Antigravity CLI Add-on v1.0.3
