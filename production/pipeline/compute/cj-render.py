#!/usr/bin/env python3
"""
cj-render.py — Cape Jones resume-safe render queue CLI.

Every render job is per-frame checkpointed: re-running the same command skips
frames that already exist. Daemon restarts, killed execs, cancelled kernels —
re-run and it picks up where it died. This is the law (see FREE-COMPUTE-2026.md).

Targets:
  local     run Blender headless on this VM (CPU, xvfb). Good for stills/tests.
  flamenco  submit frame-chunks to the Flamenco manager (see flamenco-setup.md).
  kaggle    generate a kernel payload dir (render.py + manifest) ready for
            `kaggle kernels push`. The payload itself is resume-safe.

Usage:
  cj-render.py --blend scene.blend --frames 1-360 --out renders/walkthrough \\
      --target local [--action idle_heroic_breathe] [--samples 24] [--res 960x540]
  cj-render.py --blend scene.blend --frames 1-1320 --out renders/walkthrough \\
      --target flamenco --chunk 60
  cj-render.py --blend scene.blend --frames 1-1320 --out renders/walkthrough \\
      --target kaggle --payload kaggle-payload/

The done-manifest lives at <out>/frames_done.json. Frames are <out>/frame_%04d.png.
A frame counts as done only if the PNG exists AND is >10KB (catches truncated writes).
"""
import argparse, json, math, os, subprocess, sys, shutil

BLENDER = os.path.expanduser("~/workspace/tools/blender/blender-4.0.2-linux-x64/blender")
MIN_FRAME_BYTES = 10_000

# ---------------------------------------------------------------- inner script
# This is the Blender --python payload for local renders. It is deliberately
# self-contained: it re-checks the done-manifest and skips done frames, so even
# a mid-chunk kill is safe to re-run.
INNER_SCRIPT = r'''
import bpy, math, sys, os, json

argv = sys.argv[sys.argv.index("--") + 1:]
blend_unused, outdir, f0, f1, action_name, samples, resx, resy = argv
f0, f1, samples, resx, resy = int(f0), int(f1), int(samples), int(resx), int(resy)
os.makedirs(outdir, exist_ok=True)

manifest = os.path.join(outdir, "frames_done.json")
done = set()
if os.path.exists(manifest):
    try:
        done = set(json.load(open(manifest))["done"])
    except Exception:
        pass

sc = bpy.context.scene
sc.render.resolution_x = resx
sc.render.resolution_y = resy
sc.render.resolution_percentage = 100
if samples > 0 and sc.render.engine == 'CYCLES':
    sc.cycles.samples = samples

if action_name and action_name != "none":
    act = bpy.data.actions.get(action_name)
    arm = next((o for o in bpy.data.objects if o.type == 'ARMATURE'), None)
    if act and arm:
        if not arm.animation_data:
            arm.animation_data_create()
        arm.animation_data.action = act
        print("POSE SET:", action_name)

def frame_ok(i):
    p = os.path.join(outdir, "frame_%04d.png" % i)
    return os.path.exists(p) and os.path.getsize(p) > MIN_FRAME_BYTES

newly = []
for i in range(f0, f1 + 1):
    if i in done and frame_ok(i):
        print("SKIP %d (done)" % i)
        continue
    sc.frame_set(i)
    sc.render.filepath = os.path.join(outdir, "frame_%04d.png" % i)
    bpy.ops.render.render(write_still=True)
    newly.append(i)
    done.add(i)
    # flush manifest every frame: a kill loses at most the in-flight frame
    json.dump({"done": sorted(done)}, open(manifest, "w"))
    print("RENDERED %d/%d" % (i, f1))
print("INNER DONE: %d new frames" % len(newly))
'''

# inject the byte threshold (can't use % formatting — the script body is full of %)
INNER_SCRIPT = INNER_SCRIPT.replace("MIN_FRAME_BYTES", str(MIN_FRAME_BYTES))


def parse_frames(s):
    a, b = s.split("-")
    return int(a), int(b)


def ensure_manifest(outdir):
    os.makedirs(outdir, exist_ok=True)
    mp = os.path.join(outdir, "frames_done.json")
    if not os.path.exists(mp):
        json.dump({"done": []}, open(mp, "w"))
    return mp


def target_local(args, f0, f1):
    """Run Blender headless locally (CPU via xvfb)."""
    inner = os.path.join(args.out, "_cj_inner.py")
    with open(inner, "w") as fh:
        fh.write(INNER_SCRIPT)
    cmd = [
        "xvfb-run", "-a", "env", "-u", "PYTHONPATH",
        BLENDER, "-b", args.blend, "--python", inner, "--",
        args.blend, args.out, str(f0), str(f1),
        args.action or "none", str(args.samples),
        str(args.res[0]), str(args.res[1]),
    ]
    print("RUN:", " ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print("local render exited %d — re-run the same command to resume" % r.returncode)
    return r.returncode


def target_flamenco(args, f0, f1):
    """Submit chunked job to Flamenco manager via its REST API."""
    try:
        import urllib.request
    except ImportError:
        pass
    import urllib.request as urlreq
    manager = os.environ.get("FLAMENCO_MANAGER", "http://localhost:8080")
    chunks = []
    for s in range(f0, f1 + 1, args.chunk):
        e = min(s + args.chunk - 1, f1)
        chunks.append((s, e))
    job = {
        "name": args.job_name or os.path.basename(args.blend),
        "type": "blender-render",
        "priority": 50,
        "settings": {
            "blendfile": os.path.abspath(args.blend),
            "outdir": os.path.abspath(args.out),
            "chunk_size": args.chunk,
            "frames": "%d-%d" % (f0, f1),
            "action": args.action or "",
            "samples": args.samples,
            "resolution": "%dx%d" % tuple(args.res),
        },
    }
    # NOTE: Flamenco's exact submit endpoint depends on version; this posts to
    # the documented /api/v3/jobs. If the manager version differs, see
    # flamenco-setup.md for the version-pinned call.
    req = urlreq.Request(manager + "/api/v3/jobs",
                         data=json.dumps(job).encode(),
                         headers={"Content-Type": "application/json"})
    try:
        resp = urlreq.urlopen(req, timeout=15)
        print("FLAMENCO SUBMITTED:", resp.status, resp.read()[:200])
    except Exception as ex:
        print("Flamenco submit failed (%s)." % ex)
        print("Is the manager running? See production/pipeline/compute/flamenco-setup.md")
        print("Falling back: chunk list (run each with --target local):")
        for s, e in chunks:
            print("  cj-render.py --blend %s --frames %d-%d --out %s --target local"
                  % (args.blend, s, e, args.out))
        return 1
    return 0


def target_kaggle(args, f0, f1):
    """Generate a resume-safe Kaggle kernel payload dir."""
    payload = os.path.abspath(args.payload or os.path.join(args.out, "_kaggle_payload"))
    os.makedirs(payload, exist_ok=True)
    # kernel-metadata.json
    meta = {
        "id": os.environ.get("KAGGLE_KERNEL_ID", "marsfmmg/cj-render-job"),
        "title": args.job_name or "cj-render-job",
        "code_file": "render.py",
        "language": "python",
        "kernel_type": "script",
        "is_private": True,
        "enable_gpu": True,
        "enable_internet": False,
        "dataset_sources": [],
        "competition_sources": [],
        "kernel_sources": [],
    }
    json.dump(meta, open(os.path.join(payload, "kernel-metadata.json"), "w"), indent=2)
    # render.py — same skip-done logic, paths remapped to /kaggle/working
    render_py = INNER_SCRIPT.replace(
        'argv = sys.argv[sys.argv.index("--") + 1:]',
        'import os as _os\n'
        '_os.makedirs("/kaggle/working/out", exist_ok=True)\n'
        'argv = ["x", "/kaggle/working/out", "%d", "%d", "%s", "%d", "%d", "%d"]'
        % (f0, f1, args.action or "none", args.samples, args.res[0], args.res[1])
    )
    # The blend must be inside the payload (or a dataset). We copy it if small
    # enough, else we emit instructions.
    try:
        size = os.path.getsize(args.blend)
    except OSError:
        size = 0
    if size and size < 200 * 1024 * 1024:
        shutil.copy2(args.blend, os.path.join(payload, os.path.basename(args.blend)))
        print("blend copied into payload (%d MB)" % (size // 1024 // 1024))
    else:
        print("WARN: blend is %.1f MB — attach it as a Kaggle dataset instead "
              "of the payload, then set BLEND_PATH in render.py." % (size / 1024 / 1024))
    open(os.path.join(payload, "render.py"), "w").write(render_py)
    print("KAGGLE PAYLOAD READY:", payload)
    print("Push with: cd %s && kaggle kernels push" % payload)
    print("Rules (kaggle-ops.md): space pushes >=30min apart, one active kernel,")
    print("checkpoint frames to an output dataset every N frames.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Cape Jones resume-safe render queue")
    ap.add_argument("--blend", required=True, help=".blend file to render")
    ap.add_argument("--frames", required=True, help="frame range, e.g. 1-360")
    ap.add_argument("--out", required=True, help="output dir (persistent, never /tmp)")
    ap.add_argument("--target", default="local", choices=["local", "flamenco", "kaggle"])
    ap.add_argument("--action", default=None, help="action name to apply to armature")
    ap.add_argument("--samples", type=int, default=0, help="Cycles samples (0=leave as-is)")
    ap.add_argument("--res", default="960x540", help="resolution WxH")
    ap.add_argument("--chunk", type=int, default=60, help="frames per Flamenco chunk")
    ap.add_argument("--payload", default=None, help="kaggle payload dir")
    ap.add_argument("--job-name", default=None)
    args = ap.parse_args()
    args.res = tuple(int(x) for x in args.res.lower().split("x"))
    if args.out.startswith("/tmp"):
        print("REFUSED: --out must be persistent (never /tmp). See FREE-COMPUTE-2026.md")
        return 2
    f0, f1 = parse_frames(args.frames)
    ensure_manifest(args.out)
    if args.target == "local":
        return target_local(args, f0, f1)
    if args.target == "flamenco":
        return target_flamenco(args, f0, f1)
    return target_kaggle(args, f0, f1)


if __name__ == "__main__":
    sys.exit(main())
