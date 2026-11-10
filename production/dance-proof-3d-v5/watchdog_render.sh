#!/bin/bash
# Relaunch the render driver if no render Blender is alive and frames
# are incomplete. The driver self-locks, so a spurious launch is a no-op.
exec 8>~/workspace/_cj_v5_work/render_watchdog.lock
flock -n 8 || exit 0
while true; do
  n=$(ls ~/workspace/_cj_v5_work/frames_eevee/*.png 2>/dev/null | wc -l)
  if [ "$n" -ge 1824 ]; then echo "watchdog: all frames present, exit $(date -u +%H:%M:%S)" >> ~/workspace/_cj_v5_work/render_driver.log; exit 0; fi
  if ! ps aux | grep -q '[b]lender-4.0.2-linux-x64/blender'; then
    setsid nohup ~/workspace/_cj_v5_work/run_render_chunks.sh > /dev/null 2>&1 < /dev/null &
    echo "watchdog: no blender alive, launched driver $(date -u +%H:%M:%S) frames=$n" >> ~/workspace/_cj_v5_work/render_driver.log
  fi
  sleep 240
done
