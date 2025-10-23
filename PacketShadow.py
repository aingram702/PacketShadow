#!/usr/bin/env python3
"""
Compact Dark-Themed Tkinter GUI for managing Wi-Fi monitor mode using airmon-ng.
Includes smaller buttons, tighter layout, and a dark "hacker" color scheme.
"""

import os
import re
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Utility Functions

def is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

def command_available(cmd):
    return shutil.which(cmd) is not None

def run_command(cmd_list):
    try:
        proc = subprocess.run(cmd_list, capture_output=True, text=True, check=False)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def find_wireless_interfaces():
    interfaces = []
    rc, out, _ = run_command(["iw", "dev"])
    if rc == 0 and out:
        for line in out.splitlines():
            m = re.match(r'\s*Interface\s+(\S+)', line)
            if m:
                name = m.group(1)
                if name not in interfaces:
                    interfaces.append(name)
    else:
        rc2, out2, _ = run_command(["ip", "-brief", "link"])
        if rc2 == 0 and out2:
            for line in out2.splitlines():
                parts = line.split()
                if parts and re.match(r'^(wlan|wl|wifi|ath|wlp)', parts[0]):
                    interfaces.append(parts[0])
    return interfaces  

# GUI 

class MonitorModeGUI:
    def __init__(self, root):
        self.root = root
        root.title("PacketShadow — Dark Edition")
        root.geometry("650x450")
        root.resizable(False, False)

        # --- Theme colors ---
        bg_color = "#0f0f0f"
        fg_color = "#00ff66"      # neon green
        button_bg = "#1a1a1a"
        button_fg = "#00ff99"
        highlight = "#00994d"
        font_main = ("Consolas", 10)
        font_button = ("Consolas", 9, "bold")

        root.configure(bg=bg_color)

        # --- Main frame ---
        main = tk.Frame(root, bg=bg_color)
        main.pack(fill="both", expand=True, padx=8, pady=6)

        # Title label
        tk.Label(main, text="Available Wireless Adapters:",
                 font=("Consolas", 10, "bold"),
                 fg=fg_color, bg=bg_color).pack(anchor="w")

        # Listbox frame
        list_frame = tk.Frame(main, bg=bg_color)
        list_frame.pack(fill="x", pady=(2, 6))

        self.if_listbox = tk.Listbox(list_frame, height=8, width=28,
                                     exportselection=False, bg="#111111",
                                     fg="#00ff88", font=font_main,
                                     selectbackground=highlight,
                                     selectforeground="black",
                                     borderwidth=0, highlightthickness=1,
                                     highlightcolor=highlight)
        self.if_listbox.pack(side="left", fill="y")

        scroll = tk.Scrollbar(list_frame, orient="vertical", command=self.if_listbox.yview)
        scroll.pack(side="right", fill="y")
        self.if_listbox.config(yscrollcommand=scroll.set)
        self.if_listbox.bind("<<ListboxSelect>>", self.on_list_select)

        # Interface selection input
        sel_frame = tk.Frame(main, bg=bg_color)
        sel_frame.pack(fill="x", pady=(0, 6))
        tk.Label(sel_frame, text="Select by number:", fg=fg_color, bg=bg_color,
                 font=font_main).pack(side="left")
        self.number_var = tk.StringVar()
        tk.Entry(sel_frame, width=5, textvariable=self.number_var,
                 bg="#1c1c1c", fg="#00ff66", insertbackground="#00ff66",
                 font=font_main, relief="flat").pack(side="left", padx=(4, 8))

        # Buttons frame
        btn_frame = tk.Frame(main, bg=bg_color)
        btn_frame.pack(fill="x", pady=(4, 6))

        btn_opts = {"bg": button_bg, "fg": button_fg, "activebackground": highlight,
                    "activeforeground": "black", "font": font_button,
                    "relief": "flat", "width": 12, "cursor": "hand2"}

        self.enable_btn = tk.Button(btn_frame, text="Enable", command=self.enable_monitor, **btn_opts)
        self.enable_btn.pack(side="left", padx=2, pady=2)

        self.disable_btn = tk.Button(btn_frame, text="Disable", command=self.disable_monitor, **btn_opts)
        self.disable_btn.pack(side="left", padx=2, pady=2)

        self.checkkill_btn = tk.Button(btn_frame, text="Check Kill", command=self.check_kill, **btn_opts)
        self.checkkill_btn.pack(side="left", padx=2, pady=2)

        self.restart_nm_btn = tk.Button(btn_frame, text="Restart NM", command=self.restart_network_manager, **btn_opts)
        self.restart_nm_btn.pack(side="left", padx=2, pady=2)

        self.refresh_btn = tk.Button(btn_frame, text="Refresh", command=self.refresh_interfaces, **btn_opts)
        self.refresh_btn.pack(side="left", padx=2, pady=2)

        # Root warning label
        self.root_label = tk.Label(main, text="", fg="#ff6666", bg=bg_color, font=font_main)
        self.root_label.pack(anchor="w")
        if not is_root():
            self.root_label.config(
                text="⚠ Not running as root. Some actions may fail."
            )

        # Output console
        tk.Label(main, text="Command Output:", font=("Consolas", 10, "bold"),
                 fg=fg_color, bg=bg_color).pack(anchor="w")
        self.out_text = scrolledtext.ScrolledText(main, height=10, wrap="word",
                                                  bg="#111111", fg="#00ff88",
                                                  insertbackground="#00ff66",
                                                  font=("Consolas", 9),
                                                  borderwidth=0, highlightthickness=1,
                                                  highlightbackground="#00ff66")
        self.out_text.pack(fill="both", expand=True, pady=(2, 4))

        # Populate initial list
        self.interfaces = []
        self.refresh_interfaces()

    # Helpers
    def log(self, text):
        self.out_text.insert("end", text + "\n")
        self.out_text.see("end")

    def refresh_interfaces(self):
        self.out_text.delete("1.0", "end")
        self.interfaces = find_wireless_interfaces()
        self.if_listbox.delete(0, "end")
        if not self.interfaces:
            self.if_listbox.insert("end", "No wireless adapters found.")
            self.log("No wireless adapters found.")
        else:
            for i, iface in enumerate(self.interfaces, start=1):
                self.if_listbox.insert("end", f"{i}. {iface}")
            self.log(f"Found {len(self.interfaces)} adapter(s). Select one or enter its number.")

    def on_list_select(self, event):
        sel = self.if_listbox.curselection()
        if sel:
            self.number_var.set(str(sel[0] + 1))

    def get_selected_interface(self):
        num = self.number_var.get().strip()
        if num:
            try:
                n = int(num)
                if 1 <= n <= len(self.interfaces):
                    return self.interfaces[n - 1]
            except ValueError:
                pass
        sel = self.if_listbox.curselection()
        if sel:
            return self.interfaces[sel[0]]
        messagebox.showerror("Selection Error", "Please select or enter a valid interface number.")
        return None

    def ensure_airmon(self):
        if not command_available("airmon-ng"):
            messagebox.showerror("Missing Tool", "airmon-ng not found. Install aircrack-ng and retry.")
            return False
        return True

    # Command Actions
    def enable_monitor(self):
        iface = self.get_selected_interface()
        if not iface or not self.ensure_airmon():
            return
        self.log(f"Running: airmon-ng start {iface}")
        rc, out, err = run_command(["airmon-ng", "start", iface])
        self._display_result(rc, out, err, f"Enable monitor on {iface}")

    def disable_monitor(self):
        iface = self.get_selected_interface()
        if not iface or not self.ensure_airmon():
            return
        targets = [iface, iface + "mon"] if not iface.endswith("mon") else [iface]
        for t in targets:
            self.log(f"Running: airmon-ng stop {t}")
            rc, out, err = run_command(["airmon-ng", "stop", t])
            if rc == 0:
                self._display_result(rc, out, err, f"Disable monitor on {t}")
                break

    def check_kill(self):
        if not self.ensure_airmon():
            return
        self.log("Running: airmon-ng check kill")
        rc, out, err = run_command(["airmon-ng", "check", "kill"])
        self._display_result(rc, out, err, "Check Kill")

    def restart_network_manager(self):
        if not messagebox.askyesno("Confirm", "Restart NetworkManager? Connectivity will drop."):
            return
        cmds = [
            ["systemctl", "restart", "NetworkManager"],
            ["service", "network-manager", "restart"],
            ["/etc/init.d/networking", "restart"]
        ]
        for cmd in cmds:
            self.log(f"Trying: {' '.join(cmd)}")
            rc, out, err = run_command(cmd)
            if rc == 0:
                self._display_result(rc, out, err, "NetworkManager Restarted")
                self.refresh_interfaces()
                return
        messagebox.showerror("Failed", "Could not restart NetworkManager by any method.")

    def _display_result(self, rc, out, err, action):
        if out:
            self.log(out)
        if err:
            self.log(err)
        if rc == 0:
            messagebox.showinfo("Success", f"{action} completed successfully.")
        else:
            messagebox.showerror("Error", f"{action} failed. See log for details.")
        self.refresh_interfaces()

# Main
def main():
    if not sys.platform.startswith("linux"):
        messagebox.showwarning("Non-Linux", "This tool is for Linux systems.")
    root = tk.Tk()
    MonitorModeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

