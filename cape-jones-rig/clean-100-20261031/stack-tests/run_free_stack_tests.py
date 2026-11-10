#!/usr/bin/env python3
"""Free-stack tests, Cape Jones Workstream G, 2026-10-31.
Each test: import a clean Cape Jones piece/pose, do one operation, export something
in stack-tests/. Versions + outputs logged to free-stack-results.json.
No proprietary character/logo/asset copied; inputs are our own v7c clean rig pieces."""
import json, os, subprocess, sys
RIG = "/home/hatch/workspace/cape-jones-rig"
OUT = "/home/hatch/workspace/cape-jones-rig/clean-100-20261031/stack-tests"
os.makedirs(OUT, exist_ok=True)
results = {}

def run(name, cmd, timeout=180):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        ok = p.returncode == 0
        print(f"[{name}] rc={ok} {p.stdout.strip()[:300]} {p.stderr.strip()[:300]}")
        return {"rc": p.returncode, "ok": ok, "stdout": p.stdout[:500], "stderr": p.stderr[:500]}
    except Exception as e:
        print(f"[{name}] ERROR {e}")
        return {"rc": None, "ok": False, "error": str(e)}

# --- versions ---
results["versions"] = {}
for tool, cmd in [("blender", [f"{RIG}/../tools-industry/blender-5.2.3-linux-x64/blender", "--version"]),
                  ("ffmpeg", ["ffmpeg", "-version"]), ("python_pil", ["python3", "-c", "import PIL; print(PIL.__version__)"]),
                  ("krita", ["krita", "--version"]), ("pencil2d", ["pencil2d", "--version"]),
                  ("synfig", ["synfig", "--version"])]:
    # GUI tools need xvfb for --version in some cases; use xvfb-run for krita/pencil2d
    c = (["xvfb-run", "-a"] + cmd) if tool in ("krita", "pencil2d") else cmd
    r = run(f"version-{tool}", c, timeout=60)
    results["versions"][tool] = (r["stdout"] + r["stderr"]).strip().splitlines()[:2]

# --- PIL: contact sheet, OutFixed vs original per-row check ---
from PIL import Image
orig = Image.open(f"{RIG}/cut-limbs-v7c/Arm_Front_Lower.png").convert("RGBA")
outf = Image.open(f"{RIG}/cut-limbs-v7c-gauntlet-out-fixed/Arm_Front_Lower_OutFixed.png").convert("RGBA")
sheet = Image.new("RGBA", (orig.width * 2 + 20, orig.height), (128, 128, 128, 255))
sheet.paste(orig, (0, 0), orig); sheet.paste(outf, (orig.width + 20, 0), outf)
sheet_path = f"{OUT}/pil-outfixed-vs-original-20261031.png"
sheet.convert("RGB").save(sheet_path)
# per-row alpha span preservation (the OutFixed rule)
import numpy as np
def spans(im):
    a = np.array(im)[:, :, 3] > 0
    out = []
    for row in a:
        xs = np.where(row)[0]
        out.append((int(xs[0]), int(xs[-1])) if len(xs) else None)
    return out
so, sf = spans(orig), spans(outf)
same = sum(1 for a, b in zip(so, sf) if a == b)
results["pil"] = {"output": sheet_path, "size_bytes": os.path.getsize(sheet_path),
                  "rows_compared": len(so), "rows_same_span": same,
                  "operation": "PIL composite: original lower + OutFixed lower side by side; per-row alpha-span check"}
print("PIL rows same span:", same, "/", len(so))

# --- gauntlet regression (existing test, run, no file output) ---
r = run("gauntlet-regression", ["python3", f"{RIG}/check_gauntlet_flip.py"])
results["gauntlet_regression"] = r

# --- FFmpeg: LUT grade + 24f beat encode ---
r = run("ffmpeg-lut", ["ffmpeg", "-y", "-i", f"{RIG}/rig-apose-v7c-clean-transparent.png",
                       "-vf", f"lut3d={RIG}/showcase/lut-neutral.cube",
                       f"{OUT}/ffmpeg-lut-neutral-apose-20261031.png"])
results["ffmpeg_lut"] = {**r, "output": f"{OUT}/ffmpeg-lut-neutral-apose-20261031.png",
                         "exists": os.path.exists(f"{OUT}/ffmpeg-lut-neutral-apose-20261031.png")}
frames = f"{RIG}/showcase/free-stack-tests/frames-24"
r = run("ffmpeg-beat-mp4", ["ffmpeg", "-y", "-framerate", "24", "-i", f"{frames}/frame-%02d.png",
                            "-c:v", "libx264", "-pix_fmt", "yuv420p", f"{OUT}/ffmpeg-24f-beat-20261031.mp4"])
results["ffmpeg_mp4"] = {**r, "output": f"{OUT}/ffmpeg-24f-beat-20261031.mp4"}
r = run("ffprobe-mp4", ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                        "-show_entries", "stream=nb_read_frames,r_frame_rate",
                        "-of", "default=noprint_wrappers=1", f"{OUT}/ffmpeg-24f-beat-20261031.mp4"])
results["ffprobe_mp4"] = r

# --- Synfig: render the prior .sif tween to PNG (single frame at 12f) ---
r = run("synfig-render", ["synfig", f"{RIG}/showcase/free-stack-tests/synfig-cape-jones-tween-20261031.sif",
                          "-o", f"{OUT}/synfig-tween-frame12-20261031.png", "--time", "12f"], timeout=120)
results["synfig"] = {**r, "output": f"{OUT}/synfig-tween-frame12-20261031.png",
                     "exists": os.path.exists(f"{OUT}/synfig-tween-frame12-20261031.png")}

# --- Krita: open clean apose, export (paint-op equivalent: import + export round-trip) ---
r = run("krita-export", ["xvfb-run", "-a", "krita", f"{RIG}/rig-apose-v7c-clean-transparent.png",
                         "--export", "--export-filename", f"{OUT}/krita-apose-export-20261031.png"], timeout=180)
results["krita"] = {**r, "output": f"{OUT}/krita-apose-export-20261031.png",
                    "exists": os.path.exists(f"{OUT}/krita-apose-export-20261031.png")}

# --- Tahoma2D: project level folder (24 frames + xsheet JSON) in stack-tests ---
import shutil
tdir = f"{OUT}/tahoma-cape-jones-24f"
os.makedirs(f"{tdir}/inputs", exist_ok=True)
for i in range(1, 25):
    shutil.copy(f"{frames}/frame-{i:02d}.png", f"{tdir}/inputs/frame-{i:02d}.png")
spec = {"project": "cape-jones-24f", "fps": 24, "frames": 24, "beat_markers": [1, 7, 13, 19],
        "columns": [{"column": 1, "level": "inputs/frame-##.png", "frames": "1-24",
                    "note": "xsheet-style: one level, 24 cells, beat every 6 frames"}],
        "source_plate": "rig-apose-v7c-clean-transparent.png",
        "limb_piece": "cut-limbs-v7c/Arm_Front_Lower.png",
        "status": "level folder ready; Tahoma GUI scene open + render NOT run in this batch (see log)"}
json.dump(spec, open(f"{tdir}/xsheet-beat-grid-20261031.json", "w"), indent=2)
results["tahoma_project"] = {"folder": tdir, "frames_copied": len(os.listdir(f"{tdir}/inputs"))}
r = run("tahoma-version", ["xvfb-run", "-a", "/home/hatch/workspace/tools-industry/tahoma2d-1.6.3/Tahoma2D.AppImage", "--help"], timeout=120)
results["tahoma_appimage"] = r

json.dump(results, open(f"{OUT}/free-stack-results.json", "w"), indent=2)
print("DONE")
