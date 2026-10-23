#!/usr/bin/env python3
"""Headless install + smoke test for Light It Up (free edition).

1. Downloads add-on-light-it-up-v4.0.0.zip from extensions.blender.org
   (sha256-verified against the platform metadata).
2. Installs it into Blender's user_default extensions repo.
3. Registers it by path (headless -b quirk: auto-enable doesn't fire) and
   applies the Butterfly preset, printing the lights created.

Usage: BLENDER=/path/to/blender xvfb-run -a env -u PYTHONPATH \
       $BLENDER -b --python tools/lighting/install_light_it_up.py
"""
import hashlib
import os
import subprocess
import sys
import urllib.request

EXT_ID = "light_it_up"
VERSION = "4.0.0"
ARCHIVE_HASH = "773e46efe54b1048030ed49d06d61c6b05242c14cfe7ba3c18afb3481b9900f9"
URL = (f"https://extensions.blender.org/download/sha256:{ARCHIVE_HASH}/"
       f"add-on-light-it-up-v{VERSION}.zip")

BLENDER = os.environ.get("BLENDER", "blender")
TMPZIP = "/tmp/light_it_up_verify.zip"

INNER = r"""
import bpy, sys, os
extdir = os.path.expanduser('~/.config/blender/4.5/extensions/user_default')
sys.path.insert(0, extdir)
import light_it_up
light_it_up.register()
before = len([o for o in bpy.data.objects if o.type == 'LIGHT'])
bpy.ops.light_it_up.butterfly()
lights = [o for o in bpy.data.objects if o.type == 'LIGHT']
print('LIGHTS BEFORE:', before, '| AFTER:', len(lights))
for l in lights:
    print(' -', l.name, l.data.type, 'energy=', round(l.data.energy, 1))
assert len(lights) > before, 'preset built no lights'
print('SMOKE TEST PASSED')
"""

def main():
    if not os.path.exists(TMPZIP):
        req = urllib.request.Request(URL, headers={"User-Agent": "cape-jones-tools/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(TMPZIP, "wb") as f:
            f.write(r.read())
    h = hashlib.sha256(open(TMPZIP, "rb").read()).hexdigest()
    assert h == ARCHIVE_HASH, f"hash mismatch: {h}"
    print("archive hash OK:", h[:16], "...")

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
