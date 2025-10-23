# PacketShadow

PacketShadow — a compact, dark-themed GUI for managing Wi-Fi monitor mode using airmon-ng.
Think neon-green console vibes + one-click control over monitor mode, check/kill, and NetworkManager restarts.

# Overview
PacketShadow is a lightweight Tkinter GUI wrapper around common airmon-ng workflows aimed at power users who want a tidy, dark-mode interface to enable/disable monitor mode, kill interfering processes, and restart NetworkManager when needed.

It is deliberately compact: small buttons, tight layout, and a neon-green-on-black “hacker” aesthetic that resembles a terminal but remains fully clickable.

This tool is truly built for those of us who switch between monitor mode and managed mode a lot, use check kill a lot, and those that hate having to restart Network Manager constantly.

# Features
* Lists available wireless adapters (via iw / ip link)
* Start monitor mode (airmon-ng start <iface>)
* Stop monitor mode (airmon-ng stop <iface|ifacemon>)
* airmon-ng check kill to kill interfering processes
* Attempt to restart NetworkManager (systemctl → service → init.d fallback)
* Compact fixed-size window that fits typical laptop screens
* Dark "hacker" theme (neon green on dark background)
* Output console integrated into the GUI for immediate feedback


# Requirements
* Linux (tested on Ubuntu / Debian / Pop!_OS)
* Python 3.8+
* tkinter (Python GUI toolkit)
* aircrack-ng (for airmon-ng)
* iw and ip utilities (usually present on modern distros)
* sudo / root privileges to control interfaces and restart services

# Usage
* Start the script as shown above.
* Select a wireless adapter from the list (click or enter its number).
* Click Enable to start monitor mode (runs airmon-ng start <iface>).
* Click Disable to stop monitor mode (tries <iface> and <iface>mon).
* Click Check Kill to run airmon-ng check kill (kills processes that interfere).
* Click Restart NM to restart NetworkManager (warns before disrupting connectivity).
* Check the console area at the bottom for stdout/stderr and status messages.

# Example Workflow
1. Open PacketShadow (sudo ./monitor_mode_gui_dark.py).
2. Select wlp3s0 (or type its number).
3. Click Check Kill — see warnings/logs in the console.
4. Click Enable to put the adapter into monitor mode.
5. Use Wi-Fi tools (e.g., airodump-ng) as needed.
6. When finished, Disable monitor mode and optionally Restart NM to restore normal networking.

# Troubleshooting
* No wireless adapters listed
  * Ensure iw and ip are installed.
  * Run iw dev or ip -brief link in a terminal to check.
* airmon-ng not found
  * Install aircrack-ng (sudo apt install aircrack-ng).
* Commands fail with permission denied
  * Make sure you launched the GUI with sudo or as root.
* NetworkManager restart fails
  * Check /var/log/syslog or journalctl -xe for service errors.
* Buttons are unresponsive
  * Look at the GUI console output for Python exceptions printed by the script.


# Security & Safety Notes
* Running as root: many operations require elevated privileges. Be careful — airmon-ng check kill will kill processes and Restart NM will drop connectivity temporarily. Only run this tool on systems you own or have permission to test.
* Not a hacking tool: PacketShadow is a GUI for controlling monitor mode. It does not provide packet injection, decoding, or automated attacks. Use all network tools ethically and legally.

# Contributing
Contributions welcome!
* Fix bugs, add features, or improve the UI.
* Please fork, make your changes on a branch, and open a PR with a clear description.
* For significant UI changes, include screenshots or short GIFs.

Suggested improvements:
* Preferences panel (theme toggle, font size)
* Persisted log file (e.g., /var/log/packetshadow.log)
* optional command-line flags (headless mode, auto-enable monitor for a chosen iface)
* Internationalization / translations

# Credits
* Built with Python + Tkinter
* Uses airmon-ng from the aircrack-ng suite for monitor mode operations
* Inspired by terminal aesthetics and minimalist GUI utilities
