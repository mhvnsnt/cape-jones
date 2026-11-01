#!/bin/bash
# Way 1 checklist ONLY - does NOT download, install, or activate Harmony.
# Run on a Rocky Linux 9.4 / CentOS Stream 9 machine, not on Ubuntu.
echo "=== Way 1: Native Linux Harmony 27 checklist ==="
echo "Distro (need Rocky 9.4 / CentOS Stream 9):"; cat /etc/os-release 2>/dev/null | head -3
echo "RAM (need 8GB+):"; free -h | head -2
echo "Disk (need 2.3GB+):"; df -h / | tail -1
echo "GPU (need GTX 960+ / Vulkan 1.1):"; lspci 2>/dev/null | grep -i vga || echo "no lspci/GPU found"
echo "Steps, in order:"
echo " 1. Sign in to toonboom.com as fmmg.mars@gmail.com ONLY, download Harmony 27 Premium for GNU/Linux (.tar.gz) - NOT the Windows .exe"
echo " 2. Install deps per docs (CentOS/Rocky package lists in report)"
echo " 3. tar -xvzf ./name-of-package.tar.gz && sudo ./install  (choose STANDALONE, agree licence)"
echo " 4. License Wizard: sign in as fmmg.mars@gmail.com, activate, record edition/start/end shown by the app"
echo " 5. Import CapeJones_Sitting pack, run harmony_check.js, save .tpl, export .plt, render one frame"
