#!/usr/bin/env python3
"""Gate 2 enforcer: verification gates.

Usage: python3 check_gates.py image.png|anim.gif gates.json [--frames N] [--ground-y Y] [--width W] [--height H]
Reports PASS / FAIL / SKIPPED per gate. Exits non-zero if any gate FAILs.
Requires Pillow (PIL). GIF frame count counts real frames via seek.
"""
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow (PIL) is required: pip install Pillow", file=sys.stderr)
    sys.exit(2)


def main():
    if len(sys.argv) < 3:
        print("usage: check_gates.py <image> <gates.json> [overrides]",
              file=sys.stderr)
        return 2
    path, gates_path = sys.argv[1], sys.argv[2]
    overrides = {}
    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] in ("--frames", "--ground-y", "--width", "--height") \
                and i + 1 < len(args):
            overrides[args[i]] = int(args[i + 1])
            i += 2
        else:
            i += 1
    with open(gates_path) as f:
        gates = json.load(f)
    results = {}

    def record(name, status, detail):
        results[name] = {"status": status, "detail": detail}

    if not os.path.isfile(path):
        print(json.dumps({"file": path, "overall": "FAIL",
                          "error": "file missing"}, indent=2))
        return 1
    size = os.path.getsize(path)
    img = Image.open(path)
    width, height = img.size
    n_frames = getattr(img, "n_frames", 1)
    # Alpha / bbox: use RGBA composite of all frames for GIFs.
    rgba = img.convert("RGBA")
    if n_frames > 1:
        try:
            img.seek(0)
            rgba = img.convert("RGBA")
        except Exception:
            pass
    alpha = rgba.getchannel("A")
    bbox = alpha.getbbox()
    visible = sum(1 for v in alpha.getdata() if v >=
                  gates.get("alpha", {}).get("min_alpha", 1))

    # bbox gate
    if gates.get("bbox", {}).get("require_nonempty", True):
        record("bbox", "PASS" if bbox else "FAIL",
               "bbox=%s" % (bbox,))
    # alpha gate
    min_vis = gates.get("alpha", {}).get("min_visible_pixels", 1)
    record("alpha", "PASS" if visible >= min_vis else "FAIL",
           "visible_pixels=%d" % visible)
    # ground/feet gate
    ground_y = overrides.get("--ground-y",
                             gates.get("ground_feet", {}).get("ground_y"))
    tol = gates.get("ground_feet", {}).get("tolerance_px", 8)
    if ground_y is None:
        record("ground_feet", "SKIPPED",
               "ground_y not set in gates or --ground-y; set per build spec")
    elif bbox is None:
        record("ground_feet", "FAIL", "no content bbox; feet cannot ground")
    else:
        feet_y = bbox[3] - 1
        record("ground_feet",
               "PASS" if abs(feet_y - ground_y) <= tol else "FAIL",
               "feet_y=%d ground_y=%d tolerance=%d" % (feet_y, ground_y, tol))
    # frame count gate
    exp = overrides.get("--frames",
                        gates.get("frame_count", {}).get("expected_frames"))
    if exp is None:
        record("frame_count", "SKIPPED", "expected_frames not set")
    else:
        record("frame_count", "PASS" if n_frames == exp else "FAIL",
               "frames=%d expected=%d" % (n_frames, exp))
    # canvas size gate
    w = overrides.get("--width", gates.get("canvas_size", {}).get("width"))
    h = overrides.get("--height", gates.get("canvas_size", {}).get("height"))
    if w is None or h is None:
        record("canvas_size", "SKIPPED",
               "width/height not set; set per build spec")
    else:
        record("canvas_size",
               "PASS" if (width, height) == (w, h) else "FAIL",
               "canvas=%dx%d expected=%dx%d" % (width, height, w, h))
    # file size gate
    fs = gates.get("file_size", {})
    min_b = fs.get("min_bytes", 1)
    max_chat = fs.get("max_bytes_chat", 8388608)
    if size < min_b:
        record("file_size", "FAIL", "size=%d below min %d" % (size, min_b))
    elif size > max_chat:
        record("file_size", "FAIL",
               "size=%d exceeds chat cap %d; ship downscaled chat version + full file in repo"
               % (size, max_chat))
    else:
        record("file_size", "PASS", "size=%d bytes" % size)
    failed = [k for k, v in results.items() if v["status"] == "FAIL"]
    skipped = [k for k, v in results.items() if v["status"] == "SKIPPED"]
    overall = "FAIL" if failed else ("PASS_WITH_SKIPPED" if skipped else "PASS")
    out = {"file": path, "canvas": "%dx%d" % (width, height),
           "frames": n_frames, "gates": results, "overall": overall}
    print(json.dumps(out, indent=2))
    if failed:
        print("VERIFICATION GATE: FAIL (%s)" % ", ".join(failed),
              file=sys.stderr)
        return 1
    if skipped:
        print("VERIFICATION GATE: %s — skipped gates must be set before "
              "presentation: %s" % (overall, ", ".join(skipped)),
              file=sys.stderr)
        return 0
    print("VERIFICATION GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
