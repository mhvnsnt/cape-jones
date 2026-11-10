#!/bin/bash
# Self-contained EEVEE render launcher: restored Mesa/GLVND stack
# (LD_LIBRARY_PATH) + caller's X display (run under xvfb-run).
export LD_LIBRARY_PATH=$HOME/workspace/_cj_v5_work/tools-restore/egl-stack/usr/lib/x86_64-linux-gnu
export LIBGL_ALWAYS_SOFTWARE=1
export __EGL_VENDOR_LIBRARY_DIRS=$HOME/workspace/_cj_v5_work/tools-restore/egl-stack/usr/share/glvnd/egl_vendor.d
unset EGL_PLATFORM
echo -800 > /proc/self/oom_score_adj 2>/dev/null
exec env -u PYTHONPATH $HOME/workspace/_cj_v5_work/tools-restore/blender/blender-4.0.2-linux-x64/blender "$@"
