#!/bin/bash
# V3 render driver v2: fill passes until all 1824 frames are VALID on disk.
# Storage on this box intermittently denies/drops writes under load, and GL
# via Xvfb broke mid-run on 2026-10-30; rendering now runs EGL-surface-less
# (Mesa llvmpipe via the local egl-stack vendor dir), no X server involved.
# render_frames_v3.py skips frames that verify (size + JPEG EOI), retries
# each frame on a long ladder, and this loop re-runs whole passes so any
# frame lost to a bad window is retried on the next pass.
# NOTE: range starts at frame 1 (not 17 as in driver v1) because
# assemble.sh consumes frames 1..1819.
cd /home/hatch/workspace/_cj-dance3d-v3 || exit 1
export LD_LIBRARY_PATH=$HOME/workspace/tools/egl-stack/usr/lib/x86_64-linux-gnu
export LIBGL_ALWAYS_SOFTWARE=1
export EGL_PLATFORM=surfaceless
export __EGL_VENDOR_LIBRARY_DIRS=$HOME/workspace/tools/egl-stack/usr/share/glvnd/egl_vendor.d
BLENDER=$HOME/workspace/tools/blender/blender-4.0.2-linux-x64/blender
valid_count() {
  python3 -c "
import os
d='frames'; n=0
for i in range(1,1825):
    p=os.path.join(d,'f%04d.jpg'%i)
    try:
        if os.path.getsize(p)>10000:
            with open(p,'rb') as fh:
                fh.seek(-2,2)
                if fh.read(2)==b'\xff\xd9': n+=1
    except Exception: pass
print(n)"
}
for pass in 1 2 3 4 5 6 7 8 9 10 11 12; do
  echo "=== PASS $pass $(date) valid=$(valid_count) ===" >> render.log
  for range in "1 250" "251 500" "501 750" "751 1000" "1001 1250" "1251 1500" "1501 1750" "1751 1824"; do
    set -- $range
    echo "=== CHUNK $1 $2 pass$pass $(date) ===" >> render.log
    env -u PYTHONPATH -u DISPLAY "$BLENDER" -b scene_v3.blend --python render_frames_v3.py -- frames $1 $2 >> render.log 2>&1
    echo "=== CHUNK $1 $2 pass$pass done rc=$? $(date) ===" >> render.log
  done
  n=$(valid_count)
  echo "=== PASS $pass END valid=$n $(date) ===" >> render.log
  if [ "$n" -ge 1824 ]; then
    touch RENDER_ALL_DONE
    echo "=== ALL 1824 VALID $(date) ===" >> render.log
    exit 0
  fi
done
echo "=== DRIVER GAVE UP after 12 passes, valid=$(valid_count) $(date) ===" >> render.log
exit 1
