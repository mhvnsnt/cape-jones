#!/usr/bin/env bash
# ep1_render_chunk.sh — render ONE frame-range chunk of an Episode 1 show clip.
#
# This is the unit of work a farm runs: one chunk = one Flamenco task, one
# Kaggle kernel, or one manual invocation. Chunks are independent (each
# Blender process renders only its own frames), so N workers cut wall-clock
# time by ~N for frame-parallel work. A single frame is never split.
#
# Usage:
#   ep1_render_chunk.sh <blend> <model.glb> <clip.glb> <rot_deg> <out_dir> \
#       <start_frame> <end_frame> [preset] [res] [blender_bin]
#
# Defaults: preset=eevee_show, res=1920x1080,
#   blender_bin=$BLENDER (else ~/workspace/tools/blender/blender-4.2.0-linux-x64/blender)
# Env: XVFB=1 to wrap in xvfb-run -a (needed on headless GPU-less machines
#   for Eevee; harmless for Cycles).
#
# Example — episode split into 4 chunks of 2,160 frames (24 fps, 6 min = 8,640):
#   ep1_render_chunk.sh 3d-assets/living_room.blend model.glb idle.glb 0 out/chunk1 1 2160 eevee_show 1920x1080
#   ep1_render_chunk.sh 3d-assets/living_room.blend model.glb idle.glb 0 out/chunk2 2161 4320 eevee_show 1920x1080
#   ...
# Assemble when all chunks land:
#   ffmpeg -framerate 24 -i out/chunk%d/f_%04d.png -c:v libx264 -pix_fmt yuv420p ep01.mp4
set -euo pipefail

BLEND="$1"; MODEL="$2"; CLIP="$3"; ROT="$4"; OUT="$5"; START="$6"; END="$7"
PRESET="${8:-eevee_show}"
RES="${9:-1920x1080}"
BLENDER_BIN="${10:-${BLENDER:-$HOME/workspace/tools/blender/blender-4.2.0-linux-x64/blender}}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# PERMANENT ARM FIX (owner pt98u 2026-11-10): the episode blend's embedded rig goes through the shared
# guarded loader before rendering — build an arm-fixed copy (original untouched) and render from it.
# The loader call (ensure_arm_fix) runs inside build_rig_v2.py, the pipeline's thin wrapper over it.
# If the loader refuses (the embedded rig is not the known w5r chain), fall back to the original blend
# with a loud warning: this render HIDES the room rig and plays a GLB cast model, so a non-w5r embedded
# chain is not a reason to refuse the render. The in-memory guard in ep1_render.py still repairs the
# known defect whenever it is present.
GUARD_TOOLS="${CJ_TOOLS:-$SCRIPT_DIR/../guard-stance-v2-20261110/tools}"
GUARD_TMP="$(mktemp -d)"
trap 'rm -rf "$GUARD_TMP"' EXIT
FIXED_BLEND="$GUARD_TMP/living_room_fixed.blend"
RENDER_BLEND="$BLEND"
GUARD_CMD=("$BLENDER_BIN" -b "$BLEND" --python "$GUARD_TOOLS/build_rig_v2.py" -- "$FIXED_BLEND")
if [ "${XVFB:-0}" = "1" ]; then
  if CJ_TOOLS="$GUARD_TOOLS" xvfb-run -a "${GUARD_CMD[@]}" >"$GUARD_TMP/guard.log" 2>&1; then
    RENDER_BLEND="$FIXED_BLEND"; echo "guard: rendering from arm-fixed copy" >&2
  else
    echo "GUARD WARNING: arm fix refused on $BLEND (see $GUARD_TMP/guard.log) — rendering original blend; room rig is hidden in this render" >&2
  fi
else
  if CJ_TOOLS="$GUARD_TOOLS" "${GUARD_CMD[@]}" >"$GUARD_TMP/guard.log" 2>&1; then
    RENDER_BLEND="$FIXED_BLEND"; echo "guard: rendering from arm-fixed copy" >&2
  else
    echo "GUARD WARNING: arm fix refused on $BLEND (see $GUARD_TMP/guard.log) — rendering original blend; room rig is hidden in this render" >&2
  fi
fi

CMD=("$BLENDER_BIN" -b "$RENDER_BLEND" --python "$SCRIPT_DIR/ep1_render.py" -- \
  "$MODEL" "$CLIP" "$ROT" "$OUT" '[1.2,0.9,0]' \
  --start "$START" --end "$END" --preset "$PRESET" --res "$RES")

if [ "${XVFB:-0}" = "1" ]; then
  xvfb-run -a "${CMD[@]}"
else
  "${CMD[@]}"
fi
