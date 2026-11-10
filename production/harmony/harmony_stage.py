#!/usr/bin/env python3
"""Cape Jones pipeline stage: Harmony.
If a Harmony binary is present (find_harmony.sh exit 0) render the given .xstage in batch mode;
otherwise fall back to Cape Jones Toon (cape-jones-rig/toon-boom-own-version-20261101) and
say so plainly — never report a Harmony render that did not happen."""
import json, pathlib, subprocess, sys, datetime
HERE = pathlib.Path(__file__).resolve().parent; REPO = HERE.parents[1]
def find():
    p = subprocess.run(["bash", str(HERE / "find_harmony.sh")], capture_output=True, text=True)
    kv = dict(l.split("=", 1) for l in p.stdout.splitlines() if "=" in l and not l.startswith("#"))
    return p.returncode, kv
def main(argv):
    scene = argv[1] if len(argv) > 1 else str(REPO / "wire-up-cannot-do-20261101/exporter/CapeJonesToon-scene/CapeJonesToon.xstage")
    rc, kv = find(); rep = {"when": datetime.datetime.now().astimezone().isoformat(), "scene": scene, "find_rc": rc, **kv}
    if rc == 0:
        cmd = [kv["HARMONY_BIN"].split()[0], "-batch", "-scene", scene]   # renders the scene's Write nodes
        r = subprocess.run(cmd, capture_output=True, text=True); rep.update(engine="harmony", cmd=cmd, rc=r.returncode, tail=r.stdout[-2000:] + r.stderr[-2000:])
    else:
        fb = REPO / "cape-jones-rig/toon-boom-own-version-20261101/own_version/build_own_version.py"
        # cjtoon hardcodes ~/workspace/cape-jones-rig (Muse VM layout): give it a HOME whose workspace -> this repo
        import tempfile, os; h = pathlib.Path(tempfile.mkdtemp(prefix="cjtoon-home-")); (h / "workspace").symlink_to(REPO)
        r = subprocess.run([sys.executable, str(fb)], capture_output=True, text=True, cwd=fb.parent.parent, env={**os.environ, "HOME": str(h)})
        rep.update(engine="cape-jones-toon-fallback (NOT Harmony)", rc=r.returncode, tail=r.stdout[-2000:])
    print(json.dumps(rep, indent=2)); return rep["rc"]
if __name__ == "__main__": sys.exit(main(sys.argv))
