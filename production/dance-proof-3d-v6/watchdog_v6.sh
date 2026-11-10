#!/bin/bash
# Relaunch the v6 render driver if no render Blender is alive and
# frames are incomplete. The driver self-locks, so this is a no-op
# when a driver is already running.
exec 8>~/workspace/_cj_v6_work/render_watchdog.lock
flock -n 8 || exit 0
while true; do
  n=$(ls ~/workspace/_cj_v6_work/frames_v6/*.png 2>/dev/null | wc -l)
  if [ "$n" -ge 1824 ]; then echo "watchdog: all frames present, exit $(date -u +%H:%M:%S)" >> ~/workspace/_cj_v6_work/render_driver.log; exit 0; fi
  if ! pgrep -f "render_v6_eevee" > /dev/null; then
    setsid nohup ~/workspace/_cj_v6_work/run_render_v6.sh > /dev/null 2>&1 < /dev/null &
    echo "watchdog: no render alive, launched driver $(date -u +%H:%M:%S) frames=$n" >> ~/workspace/_cj_v6_work/render_driver.log
  fi
  sleep 240
done
