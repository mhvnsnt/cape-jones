#!/bin/bash
# V6 production render driver: 24-frame sub-ranges, unlimited retries,
# completion verified per sub-range by file stats. Resume-safe.
exec 9>~/workspace/_cj_v6_work/render_driver.lock
flock -n 9 || exit 0
cd ~/workspace/_cj_v6_work
mkdir -p frames_v6
echo "driver v6 start $(date -u +%F_%H:%M:%S) pid $$" >> render_driver.log

# PERMANENT ARM FIX (owner pt98u 2026-11-10): the v6 scene's rig goes through the shared guarded loader
# before any render — build an arm-fixed copy with the existing pipeline tool (original untouched) and
# render from it. The loader call (ensure_arm_fix) runs inside build_rig_v2.py, the pipeline's thin
# wrapper over it. If the loader refuses (unknown arm chain), stop: do not render H arms.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARD_TOOLS="${CJ_TOOLS:-$SCRIPT_DIR/../guard-stance-v2-20261110/tools}"
SCENE="$HOME/workspace/_cj_v6_work/scene_v6.blend"
FIXED_SCENE="$HOME/workspace/_cj_v6_work/scene_v6_fixed.blend"
BLENDER_BIN="${BLENDER:-$HOME/workspace/_cj_v5_work/blender-5.2.3-linux-x64/blender}"
if [ ! -f "$FIXED_SCENE" ] || [ "$SCENE" -nt "$FIXED_SCENE" ]; then
  echo "guard: building arm-fixed scene copy $FIXED_SCENE" >> render_driver.log
  CJ_TOOLS="$GUARD_TOOLS" timeout 20000 env -u PYTHONPATH xvfb-run -a "$BLENDER_BIN" -b "$SCENE" \
    --python "$GUARD_TOOLS/build_rig_v2.py" -- "$FIXED_SCENE" >> render_chunks.log 2>&1 \
    || { echo "GUARD FAILED: arm fix refused on $SCENE — not rendering" >> render_driver.log; exit 1; }
fi
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
      ~/workspace/_cj_v5_work/blender-5.2.3-linux-x64/blender -b "$FIXED_SCENE" \
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
