#!/usr/bin/env python3
"""Natron headless smoke test — verifies NatronRenderer can build a node graph
and render frames on this VM. Run:

    ~/workspace/tools/natron/natron-render.sh natron_smoke_test.py < /dev/null

or: python3 natron_smoke_test.py --selftest   (runs the full render + checks PNG)

Exit 0 = Natron healthy. Non-zero = Natron broken (see stderr).
"""
import os
import subprocess
import sys
import tempfile

WRAPPER = os.path.expanduser("~/workspace/tools/natron/natron-render.sh")
BUILD_SCRIPT = """\
app = NatronEngine.natron.getInstance(0)
const = app.createNode("net.sf.openfx.ConstantPlugin")
const.getParam("color").set(1.0, 0.2, 0.8, 1.0)
write = app.createNode("fr.inria.built-in.Write")
write.connectInput(0, const)
write.getParam("filename").set("__OUT__")
"""


def run_selftest() -> int:
    tmp = tempfile.mkdtemp(prefix="natron-smoke-")
    out = os.path.join(tmp, "smoke.png")
    build = os.path.join(tmp, "build.py")
    with open(build, "w") as f:
        f.write(BUILD_SCRIPT.replace("__OUT__", out))
    if not os.path.exists(WRAPPER):
        print(f"FAIL: wrapper not found at {WRAPPER}", file=sys.stderr)
        return 1
    r = subprocess.run(
        [WRAPPER, build],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if not os.path.exists(out) or os.path.getsize(out) < 1000:
        print("FAIL: render did not produce output PNG", file=sys.stderr)
        print(r.stderr[-2000:], file=sys.stderr)
        return 1
    with open(out, "rb") as f:
        sig = f.read(8)
    if sig != b"\x89PNG\r\n\x1a\n":
        print("FAIL: output is not a valid PNG", file=sys.stderr)
        return 1
    # Own-eyes check on color: read the first pixel via PIL if available
    try:
        from PIL import Image
        px = Image.open(out).convert("RGB").getpixel((10, 10))
        # Constant node outputs LINEAR (1.0, 0.2, 0.8); the Write node applies
        # sRGB conversion on output, so correct pixels are ~(255, 124, 232):
        #   0.2 -> 1.055*0.2^(1/2.4)-0.055 = 0.4845 -> 124
        #   0.8 -> 1.055*0.8^(1/2.4)-0.055 = 0.906  -> 231
        print(f"first-pixel RGB = {px} (expect ~ (255, 124, 232), sRGB of linear (1.0,0.2,0.8))")
        if not (px[0] > 240 and 100 < px[1] < 150 and px[2] > 200):
            print("FAIL: pixel color is wrong — graph did not render Constant", file=sys.stderr)
            return 1
    except ImportError:
        print("PIL not installed; skipped pixel check")
    print(f"PASS: Natron rendered {out} ({os.path.getsize(out)} bytes)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        sys.exit(run_selftest())
    print(__doc__)
