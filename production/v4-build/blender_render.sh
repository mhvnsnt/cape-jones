#!/bin/bash
# EGL-surfaceless render launcher (v3 lane's proven recipe on this box).
export LD_LIBRARY_PATH=$HOME/workspace/tools/egl-stack/usr/lib/x86_64-linux-gnu
export LIBGL_ALWAYS_SOFTWARE=1
export EGL_PLATFORM=surfaceless
export __EGL_VENDOR_LIBRARY_DIRS=$HOME/workspace/tools/egl-stack/usr/share/glvnd/egl_vendor.d
exec env -u PYTHONPATH -u DISPLAY $HOME/workspace/tools/blender/blender-4.0.2-linux-x64/blender "$@"
