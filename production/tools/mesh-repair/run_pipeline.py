#!/usr/bin/env python3
"""run_pipeline.py — one-shot mesh seam repair for a character blend.

Pipeline: detect seams -> weld (modifier) -> verify -> save repaired blend.

    python3 run_pipeline.py --input scene.blend --output scene_repaired.blend \
        --body CapeJones_Body [--threshold 0.02] [--blender /path/to/blender]

* Never overwrites the input: the repaired scene is always a NEW file.
* The fix is a Weld modifier placed before the Armature modifier, so it
  applies to every pose/animation automatically (standing pipeline).
* Headless Blender does the work; this driver just sequences the steps.
* Memory-safe on 910k-vert meshes: numpy only, no bmesh, no edit mode.

Requires: Blender 3.x/4.x with bundled numpy, xvfb-run on headless Linux.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = os.environ.get(
    "BLENDER_BIN",
    os.path.expanduser("~/workspace/tools/blender/blender-4.0.2-linux-x64/blender"),
)


def run_blender(blend, script, args, tag):
    cmd = (["xvfb-run", "-a", "env", "-u", "PYTHONPATH", BLENDER,
            "-b", blend, "--python", script, "--"] + args)
    print(f"[{tag}] {' '.join(cmd[:6])} ...", flush=True)
    p = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(p.stdout[-3000:])
    if p.returncode != 0:
        print(p.stderr[-3000:], file=sys.stderr)
        raise SystemExit(f"[{tag}] blender step failed (exit {p.returncode})")
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--rig", default="CapeJones_Rig")
    ap.add_argument("--threshold", type=float, default=0.02)
    ap.add_argument("--workdir", default=None)
    ap.add_argument("--skip-align", action="store_true",
                    help="skip the mesh->rig transform alignment step")
    a = ap.parse_args()

    if os.path.abspath(a.input) == os.path.abspath(a.output):
        raise SystemExit("refusing to overwrite the input: --output must be a NEW file")

    workdir = a.workdir or tempfile.mkdtemp(prefix="mesh-repair-")
    os.makedirs(workdir, exist_ok=True)
    npy = os.path.join(workdir, "seam_vert_indices.npy")
    verify_json = os.path.join(workdir, "verify.json")

    # work on a copy; the source blend is never touched
    tmp_blend = os.path.join(workdir, "work.blend")
    shutil.copy2(a.input, tmp_blend)

    if not a.skip_align:
        run_blender(tmp_blend, os.path.join(HERE, "align_mesh_to_rig.py"),
                    [a.body, a.rig], "align")

    run_blender(tmp_blend, os.path.join(HERE, "detect_seams.py"),
                [a.body, workdir], "detect")
    stats = json.load(open(os.path.join(workdir, "seam_stats.json")))
    print(f"[detect] {stats['boundary_edges']} boundary edges, "
          f"{stats['seam_verts']} seam verts", flush=True)

    run_blender(tmp_blend, os.path.join(HERE, "apply_weld.py"),
                [a.body, npy, str(a.threshold)], "weld")

    run_blender(tmp_blend, os.path.join(HERE, "verify_repair.py"),
                [a.body, verify_json], "verify")
    report = json.load(open(verify_json))
    print("[verify] rest boundary edges:  %(rest_boundary_edges)d\n"
          "[verify] posed boundary edges: %(posed_boundary_edges)d\n"
          "[verify] posed loop count:     %(posed_loop_count)d\n"
          "[verify] welded_ok:            %(welded_ok)s" % report, flush=True)

    shutil.copy2(tmp_blend, a.output)
    print(f"[done] repaired blend -> {a.output}", flush=True)
    if not report["welded_ok"]:
        raise SystemExit("[done] WARNING: welded_ok=false — see verify.json")


if __name__ == "__main__":
    main()
