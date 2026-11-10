#!/usr/bin/env bash
# Cape Jones guard shot — the ONLY supported way to render the w5r rig in fight/guard poses.
# Gate-first: the arm-chain repair is rebuilt from the repo blend and the guard-arm gate must PASS
# before any bake/render. The raw w5r_clean blend (arm joints one segment out => "H" arms) is rejected.
# usage: guard_shot_pipeline.sh RIG_W5R_CLEAN.blend STANCE.glb WORKDIR [render_pct]
set -euo pipefail
RIG=$1; GLB=$2; W=$3; PCT=${4:-100}; T=$(cd "$(dirname "$0")" && pwd); B=${BLENDER:-blender}
mkdir -p "$W"; export CJ_TOOLS="$T" CJ_WORK="${CJ_WORK:-$W}"
echo "[1/5] gate must FAIL on the raw rig (proves the gate still detects the defect)"
if "$B" -b "$RIG" --python "$T/../tests/test_guard_arms.py" -- "$GLB" "$W/gate_raw.json" >"$W/gate_raw.log" 2>&1; then
  echo "raw rig PASSED the arm gate: either the repo blend was fixed upstream or the gate is broken — stop and inspect"; exit 3; fi
echo "[2/5] build arm-fixed rig (new file, original untouched)"
"$B" -b "$RIG" --python "$T/build_rig_v2.py" -- "$W/rig_v2_arms.blend" >"$W/build_rig.log" 2>&1
echo "[3/5] gate must PASS on the fixed rig"
"$B" -b "$W/rig_v2_arms.blend" --python "$T/../tests/test_guard_arms.py" -- "$GLB" "$W/gate_fixed.json" >"$W/gate_fixed.log" 2>&1 || { echo "FIXED RIG FAILED ARM GATE — no render"; exit 4; }
[ "${STOP_AFTER_GATE:-0}" = 1 ] && { echo "gate OK, stopping (STOP_AFTER_GATE=1)"; exit 0; }
echo "[4/5] cloth (needs $CJ_WORK/body_islands.npy + body_texcol.npy from precompute_cape_islands*.py): proxy+pins+surface-deform, then ellipsoid collision + grounding + bake"
"$B" -b "$W/rig_v2_arms.blend" --python "$T/build_cloth.py" -- "$GLB" "$W/rig_v2_cloth_b.blend" >"$W/build_cloth.log" 2>&1
"$B" -b "$W/rig_v2_cloth_b.blend" --python "$T/bake_v3.py" -- "$W/rig_v3_cloth_g.blend" >"$W/bake_v3.log" 2>&1
echo "[5/5] render frames 51..288"
"$B" -b "$W/rig_v3_cloth_g.blend" --python "$T/render_guard.py" -- 51 288 "$W/fr/f_" "$PCT" >"$W/render.log" 2>&1
