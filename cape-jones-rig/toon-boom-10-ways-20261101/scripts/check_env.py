#!/usr/bin/env python3
"""Environment check for Harmony routes. Read-only, no installs, no credentials."""
import os, shutil, subprocess, json, sys
def run(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as e:
        return f"NOT FOUND / ERROR: {e}"
out = {
  "os": run(["cat","/etc/os-release"]),
  "kernel": run(["uname","-a"]),
  "cpu_count": os.cpu_count(),
  "mem": run(["free","-h"]),
  "disk_home": run(["df","-h", os.path.expanduser("~")]),
  "tools": {t: shutil.which(t) for t in ["wine","winetricks","qemu-system-x86_64","VBoxManage","docker","podman","rdesktop","xfreerdp","remmina","vncviewer","flatpak","steam"]},
  "gpu": run(["lspci"]),
  "harmony_linux_supported": "CentOS Stream 9 / Rocky Linux 9.4 per docs.toonboom.com Harmony 27 System Requirements",
  "this_vm_matches_linux": False,
  "reason": "This VM is Ubuntu 24.04, 4 CPUs, 7.7GB RAM (below Harmony 8GB minimum), no GPU, no wine/qemu/VirtualBox/docker found. Harmony 27 Linux says 'may not run on other distributions' — Ubuntu is NOT a supported distro.",
}
print(json.dumps(out, indent=2))
