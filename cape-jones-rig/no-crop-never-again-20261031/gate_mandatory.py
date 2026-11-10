#!/usr/bin/env python3
"""MANDATORY pre-delivery gate for Cape Jones work, 2026-10-31.

NO-CROP-WINDOW RULE, now enforced, not optional (Mars, 2026-10-31
19:47 CDT: wire it up 100% so it never happens again):
  No figure, frame, or piece ships unless this gate PASSES on the
  RGBA file that will ship (or, for an RGB display save, on the RGBA
  pre-save file -- a .convert("RGB") save does not make an opaque
  canvas pass, and it does not hide a clip).

Usage:
  python3 gate_mandatory.py <file-or-dir> [--log gate_logs/delivery-log.jsonl]
  python3 gate_mandatory.py --check-builder <builder.py>
  python3 gate_mandatory.py --protected-square 420,420,1500,1500 <file>

Exit codes: 0 = PASS (ship), 1 = FAIL (edge touch / margin <= 0 /
  figure outside protected square -- DO NOT SHIP), 2 = FLAGGED
  (source builder contains a banned crop-window pattern -- migrate
  it first, or ship only with an explicit FLAG entry in the log).
Every run appends one JSON line per file to the log (default:
gate_logs/delivery-log.jsonl in this folder). Use the rig venv
python for the OpenCV cross-check (cv2 5.0.0); system python falls
back to numpy/Pillow and says so, it does not fail on that account.
"""
import json, os, re, sys, time, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from check_no_clip import check

LOG = pathlib.Path(__file__).parent / "gate_logs" / "delivery-log.jsonl"
BANNED = [
    ("expand=False", r"expand\s*=\s*False"),
    ("rotate() without expand=True (Pillow default is expand=False)",
     r"\.rotate\([^)]*\)"),
]


def run_gate(paths, protected=None):
    files = []
    for a in paths:
        if os.path.isdir(a):
            files += sorted(os.path.join(a, f) for f in os.listdir(a)
                            if f.lower().endswith(".png"))
        else:
            files.append(a)
    results, bad = [], []
    for f in files:
        r = check(f)
        if protected:
            x0, y0, x1, y1 = protected
            bb = r["bbox"]
            if bb and not (bb[0] >= x0 and bb[1] >= y0 and bb[2] <= x1 and bb[3] <= y1):
                r["verdict"] = "FAIL"
                r["fail_reasons"].append(f"figure bbox {bb} outside protected square {protected}")
        r["checked_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        results.append(r)
        if r["verdict"] == "FAIL":
            bad.append(f)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a") as fh:
        for r in results:
            fh.write(json.dumps(r) + "\n")
    print(f"GATE_MANDATORY: {len(results) - len(bad)}/{len(results)} PASS, log -> {LOG}")
    for r in results:
        print(json.dumps(r))
    return 1 if bad else 0


def check_builder(path):
    txt = pathlib.Path(path).read_text(errors="ignore")
    flags = []
    padded_safe = ("no_crop" in txt) or ("PAD" in txt and "trim(" in txt)
    if re.search(r"expand\s*=\s*False", txt) and not padded_safe:
        flags.append("expand=False present without padded-canvas + trim migration")
    if not padded_safe:
        for m in re.finditer(r"\.rotate\([^)]*\)", txt):
            if "expand=True" not in m.group(0):
                flags.append(f"rotate() without expand=True: {m.group(0)[:60]}")
                break
    if "128,128,128" in txt:
        flags.append("grey opaque canvas (128,128,128) present -- figure layer must be transparent")
    if "paste_at" in txt and "paste_nocrop" not in txt and not padded_safe:
        flags.append("paste_at() without paste_nocrop -- off-canvas paste clips silently")
    if padded_safe and not flags:
        flags = []
    print(json.dumps({"builder": str(path), "flags": flags,
                      "padded_safe_migration": padded_safe,
                      "verdict": "FLAGGED" if flags else "PASS"}, indent=2))
    return 2 if flags else 0


def main(argv):
    if argv[:1] == ["--check-builder"]:
        return check_builder(argv[1])
    protected = None
    if argv[:2] == ["--protected-square"]:
        protected = tuple(int(v) for v in argv[1].split(","))
        argv = argv[2:]
    return run_gate(argv, protected)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
