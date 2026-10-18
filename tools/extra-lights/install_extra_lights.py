#!/usr/bin/env python3
"""Headless install + smoke test for Extra Lights (free, GPL-3.0).

Installs the vendored copy (tools/pulled/extra-lights/) into Blender's
user_default extensions repo, registers it by path (headless -b quirk:
auto-enable doesn't fire), and functionally verifies by adding one
photometric preset light.

Usage: BLENDER=/path/to/blender xvfb-run -a env -u PYTHONPATH \
       $BLENDER -b --python tools/extra-lights/install_extra_lights.py
"""
import os
import subprocess
import zipfile

BLENDER = os.environ.get("BLENDER", "blender")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "pulled", "extra-lights")
TMPZIP = "/tmp/extra_lights_verify.zip"

INNER = r"""
import bpy, sys, os
extdir = os.path.expanduser('~/.config/blender/4.5/extensions/user_default')
sys.path.insert(0, extdir)
import extra_lights
extra_lights.register()
ops = [x for x in dir(bpy.ops.light) if x.startswith('add_')]
assert len(ops) >= 20, f'expected 20+ preset ops, got {len(ops)}'
before = len([o for o in bpy.data.objects if o.type == 'LIGHT'])
getattr(bpy.ops.light, ops[0])()
after = len([o for o in bpy.data.objects if o.type == 'LIGHT'])
assert after == before + 1, 'preset op built no light'
l = [o for o in bpy.data.objects if o.type == 'LIGHT'][-1]
print(f'EXTRA-LIGHTS: {len(ops)} preset ops; added {l.name} ({l.data.type}, energy={l.data.energy})')
print('SMOKE TEST PASSED')
"""


def zip_src(src, dst):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(src):
            for f in files:
                if f.startswith("."):
                    continue
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, src))


def main():
    assert os.path.isdir(SRC), f"vendored source missing: {SRC}"
    zip_src(SRC, TMPZIP)
    subprocess.run([BLENDER, "-b", "--python-expr", f"""
import bpy
bpy.context.preferences.extensions.active_repo = 1
bpy.ops.extensions.package_install_files(filepath='{TMPZIP}', repo='user_default', enable_on_install=True)
print('INSTALLED TO user_default')
"""], check=True)
    subprocess.run(
        ["xvfb-run", "-a", "env", "-u", "PYTHONPATH", BLENDER, "-b",
         "--python-expr", INNER], check=True)


if __name__ == "__main__":
    main()
