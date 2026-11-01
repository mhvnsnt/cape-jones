#!/bin/bash
# Render each CapeGP preset from its OWN single-preset .blend.
# Reason: in a multi-frame GP object, a layer with no keyframe at a frame
# HOLDS its previous frame, so snap layers from earlier presets leaked
# into later preset renders. Single-preset blends have no holdover.
set -e
D=/home/hatch/workspace/cape-jones-rig/capegp-presets-20261031
BL=~/workspace/tools-industry/blender-5.2.3-linux-x64/blender
i=1
for P in NORMAL APOSE_FLEX FACE_SNAP COWL_SNAP CHEST_SNAP JOINT_SMOOTH; do
  xvfb-run -a $BL -b --python $D/build_capegp.py -- --preset $P $D/single-$P.blend > /dev/null 2>&1
  cat > /tmp/render_one.py << PYEOF
import bpy
bpy.ops.wm.open_mainfile(filepath="$D/single-$P.blend")
sc = bpy.context.scene
sc.frame_set(1)
sc.render.filepath = "$D/preset-$(printf %04d $i).png"
bpy.ops.render.render(write_still=True)
print("RENDERED $P")
PYEOF
  xvfb-run -a $BL -b --python /tmp/render_one.py 2>&1 | grep -E "RENDERED|Saved"
  i=$((i+1))
done
echo "ALL SINGLE PRESETS RENDERED"
