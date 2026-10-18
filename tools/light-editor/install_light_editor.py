#!/usr/bin/env python3
"""Headless install + smoke test for Light Editor (free, GPL-3.0).

Installs the vendored copy (tools/pulled/Light-Editor/) into Blender's
user_default extensions repo, registers it by path (headless -b quirk:
auto-enable doesn't fire), and verifies its operators exist.

Usage: BLENDER=/path/to/blender xvfb-run -a env -u PYTHONPATH \
       $BLENDER -b --python tools/light-editor/install_light_editor.py
"""
import os
import subprocess
import sys
import zipfile

BLENDER = os.environ.get("BLENDER", "blender")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "pulled", "Light-Editor")
TMPZIP = "/tmp/light_editor_verify.zip"

INNER = r"""
import bpy, sys, os
extdir = os.path.expanduser('~/.config/blender/4.5/extensions/user_default')
sys.path.insert(0, extdir)
import LightEditor
LightEditor.register()
ops = [x for x in dir(bpy.ops.light_editor)]
need = {'toggle_group', 'toggle_collection', 'toggle_kind'}
assert need <= set(ops), f'missing ops: {need - set(ops)}'
print('LIGHT-EDITOR OPS:', sorted(ops))
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
