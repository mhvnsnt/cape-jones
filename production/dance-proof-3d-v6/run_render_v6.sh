#!/bin/bash
# V6 production render driver: 24-frame sub-ranges, unlimited retries,
# completion verified per sub-range by file stats. Resume-safe.
exec 9>~/workspace/_cj_v6_work/render_driver.lock
flock -n 9 || exit 0
cd ~/workspace/_cj_v6_work
mkdir -p frames_v6
echo "driver v6 start $(date -u +%F_%H:%M:%S) pid $$" >> render_driver.log
range_complete() {
  local s=$1 e=$2 f p
  for ((f=s; f<=e; f++)); do
    p=$(printf 'frames_v6/f%04d.png' $f)
    [ -f "$p" ] && [ $(stat -c%s "$p") -gt 20000 ] || return 1
  done
  return 0
}
run_sub() {
  local s=$1 e=$2 attempt=0
  while ! range_complete $s $e; do
    attempt=$((attempt + 1))
    echo "=== sub $s-$e attempt $attempt $(date -u +%H:%M:%S)" >> render_driver.log
    timeout 20000 env -u PYTHONPATH xvfb-run -a \
      ~/workspace/_cj_v5_work/blender-5.2.3-linux-x64/blender -b ~/workspace/_cj_v6_work/scene_v6.blend \
      --python ~/workspace/_cj_v6_work/render_v6_eevee.py -- ~/workspace/_cj_v6_work/frames_v6 $s $e \
      >> render_chunks.log 2>&1
    range_complete $s $e || sleep 20
  done
  echo "=== sub $s-$e COMPLETE $(date -u +%H:%M:%S)" >> render_driver.log
}
s=1
while [ $s -le 1824 ]; do
  e=$((s + 23)); [ $e -gt 1824 ] && e=1824
  run_sub $s $e
  s=$((e + 1))
done
echo "RENDER_ALL_DONE" >> render_driver.log
