#!/usr/bin/env python3
"""Natron headless finishing comp for the show pipeline.

Graph (all nodes exist in Natron 2.5.0's shipped Misc bundle):

    Read(beauty) -> Grade -> Saturation -> Sharpen -> Merge(over, bg) -> Write

Usage (headless, the supported form per CAPE-JONES-WIRING.md gotchas):

    NATRON_BEAUTY=/path/beauty.png NATRON_OUT=/path/final.png \\
        ~/workspace/tools/natron/natron-render.sh natron_comp_finish.py < /dev/null

Env params:
    NATRON_BEAUTY        required -- beauty pass (PNG, RGB or RGBA)
    NATRON_BG            optional -- background plate PNG (skipped = comp on black)
    NATRON_OUT           required -- output PNG path
    NATRON_MULTIPLY      optional -- grade gain on beauty (default 1.0)
    NATRON_GAMMA         optional -- grade gamma on beauty (default 1.0)
    NATRON_SATURATION    optional -- saturation on beauty (default 1.0)
    NATRON_SHARPEN       optional -- sharpen amount on beauty (default 0.0)

Self-test (does not need Natron): python3 natron_comp_finish.py --selftest
runs the full headless comp on synthetic plates and checks the output pixels.

Exit 0 = comp rendered. Non-zero = broken (see stderr).
"""
import os
import subprocess
import sys
import tempfile

WRAPPER = os.path.expanduser("~/workspace/tools/natron/natron-render.sh")

BUILD_SCRIPT = r'''
import os
app = NatronEngine.natron.getInstance(0)

beauty_path = os.environ["NATRON_BEAUTY"]
bg_path = os.environ.get("NATRON_BG", "")
out_path = os.environ["NATRON_OUT"]
multiply = float(os.environ.get("NATRON_MULTIPLY", "1.0"))
gamma = float(os.environ.get("NATRON_GAMMA", "1.0"))
saturation = float(os.environ.get("NATRON_SATURATION", "1.0"))
sharpen = float(os.environ.get("NATRON_SHARPEN", "0.0"))

def node(app, pid):
    n = app.createNode(pid)
    if n is None:
        raise RuntimeError("Natron: createNode returned None for %s" % pid)
    return n

beauty = node(app, "fr.inria.built-in.Read")
beauty.getParam("filename").set(beauty_path)
# Still PNGs report frame range 0-0; normalize to the project's frame.
beauty.getParam("firstFrame").set(1)
beauty.getParam("lastFrame").set(1)
# NOTE: inputs must share the project format (true for render passes).
# The Write node conforms the comp to the project format; Reformat is
# intentionally NOT in this chain (its "project" mode misbehaves headless).
beauty_src = beauty

grade = node(app, "net.sf.openfx.GradePlugin")
grade.connectInput(0, beauty_src)
grade.getParam("multiply").set(multiply, multiply, multiply, 1.0)
grade.getParam("gamma").set(gamma, gamma, gamma, 1.0)

sat = node(app, "net.sf.openfx.SaturationPlugin")
sat.connectInput(0, grade)
sat.getParam("saturation").set(saturation)

# Misc bundle has no standalone Sharpen node; DenoiseSharpen covers it.
# Denoise amount forced to 0 so this step sharpens only.
sharp = node(app, "net.sf.openfx.DenoiseSharpen")
sharp.connectInput(0, sat)
sharp.getParam("denoiseAmount").set(0.0)
sharp.getParam("sharpenAmount").set(sharpen)

tail = sharp
if bg_path:
    bg = node(app, "fr.inria.built-in.Read")
    bg.getParam("filename").set(bg_path)
    bg.getParam("firstFrame").set(1)
    bg.getParam("lastFrame").set(1)
    merge = node(app, "net.sf.openfx.MergePlugin")
    merge.getParam("operation").set("over")
    # Natron Merge wiring (verified by render test): input 0 = B (background),
    # input 1 = A (foreground). Swapping these silently drops the foreground.
    merge.connectInput(0, bg)      # B = background
    merge.connectInput(1, sharp)   # A = foreground
    tail = merge

write = node(app, "fr.inria.built-in.Write")
write.connectInput(0, tail)
write.getParam("filename").set(out_path)
# Stills only: pin the project frame range so NatronRenderer renders exactly
# one frame (otherwise it renders 0-250 onto the same filename).
app.getProjectParam("frameRange").set(1, 1)
'''


def render(build_script: str, env: dict) -> "subprocess.CompletedProcess":
    """Run a Natron build script headless through the wrapper."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, prefix="natron-comp-"
    ) as f:
        f.write(build_script)
        path = f.name
    try:
        full_env = dict(os.environ)
        full_env.update(env)
        return subprocess.run(
            [WRAPPER, path],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=300,
            env=full_env,
        )
    finally:
        os.unlink(path)


def run_selftest() -> int:
    """Full comp on synthetic plates, pixel-verified."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("FAIL: PIL not installed for selftest", file=sys.stderr)
        return 1
    tmp = tempfile.mkdtemp(prefix="natron-comp-test-")
    # Beauty: opaque red disc on transparent, 256x256
    beauty = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    ImageDraw.Draw(beauty).ellipse([48, 48, 208, 208], fill=(255, 0, 0, 255))
    beauty_p = os.path.join(tmp, "beauty.png")
    beauty.save(beauty_p)
    # BG: solid blue 256x256
    bg = Image.new("RGB", (256, 256), (0, 0, 255))
    bg_p = os.path.join(tmp, "bg.png")
    bg.save(bg_p)
    out_p = os.path.join(tmp, "final.png")

    r = render(BUILD_SCRIPT, {"NATRON_BEAUTY": beauty_p,
                              "NATRON_BG": bg_p,
                              "NATRON_OUT": out_p})
    if not os.path.exists(out_p) or os.path.getsize(out_p) < 1000:
        print("FAIL: comp did not produce output PNG", file=sys.stderr)
        print((r.stderr or "")[-2000:], file=sys.stderr)
        return 1
    img = Image.open(out_p).convert("RGB")
    w, h = img.size
    # Natron places the 256px plates bottom-left in the 1920x1080 project
    # canvas (Write conforms to project format).
    center = img.getpixel((128, h - 128))  # disc center -> red disc over blue
    plate_bg = img.getpixel((30, h - 30))  # inside plate, off disc -> blue bg
    outside = img.getpixel((1000, 100))    # outside both plates -> black
    print(f"center={center} (expect ~red) plate_bg={plate_bg} (expect ~blue) "
          f"outside={outside} (expect ~black)")
    ok = True
    if not (center[0] > 200 and center[1] < 80 and center[2] < 80):
        print("FAIL: disc center is not red -- beauty chain broken", file=sys.stderr)
        ok = False
    if not (plate_bg[2] > 200 and plate_bg[0] < 80 and plate_bg[1] < 80):
        print("FAIL: off-disc plate area is not blue -- over op broken", file=sys.stderr)
        ok = False
    if not (outside[0] < 40 and outside[1] < 40 and outside[2] < 40):
        print("FAIL: off-plate area is not black", file=sys.stderr)
        ok = False
    if not ok:
        return 1
    print(f"PASS: finishing comp rendered {out_p} ({os.path.getsize(out_p)} bytes)")
    print(f"      test plates + output left in {tmp} for own-eyes check")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(run_selftest())
    try:
        import NatronEngine  # noqa: F401
        in_natron = True
    except ImportError:
        in_natron = False
    if in_natron:
        # Executed by NatronRenderer: build the graph; NatronRenderer renders
        # the project automatically because it contains a Write node.
        exec(compile(BUILD_SCRIPT, "natron_comp_finish", "exec"))
    else:
        print(__doc__)
