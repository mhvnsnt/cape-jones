#!/bin/bash
# GUI launch probe under xvfb-run: launch app, screenshot root window, kill by exact name.
OUT="$HOME/workspace/cape-jones-rig/clean-100-20261031/stack-tests"
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p /tmp/runtime-root
pencil2d >/tmp/pencil2d-gui.log 2>&1 &
P1=$!
sleep 12
import -window root "$OUT/pencil2d-gui-launch-20261031.png" 2>&1 | head -2
echo "pencil2d alive: $(ps -p $P1 -o comm= 2>/dev/null || echo no)"
kill $P1 2>/dev/null; sleep 2
"$HOME/workspace/tools-industry/tahoma2d-1.6.3/squashfs-root/usr/bin/tahoma2d" >/tmp/tahoma-gui.log 2>&1 &
P2=$!
sleep 15
import -window root "$OUT/tahoma-gui-launch-20261031.png" 2>&1 | head -2
echo "tahoma2d alive: $(ps -p $P2 -o comm= 2>/dev/null || echo no)"
kill $P2 2>/dev/null; sleep 2
ls -lh "$OUT"/*gui-launch*.png
echo PROBE_DONE
