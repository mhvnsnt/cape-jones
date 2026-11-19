import base64, json, subprocess, sys

REPO = "mhvnsnt/cape-jones"
PARENT = "ed7a22a05c31893d6d86e22cbc104b4b5fbcf77b"
BRANCH = "feature/cj-dance-proof-3d-v3-20261030"
FILES = [
    ("production/dance-proof-3d/build_dance.py", "pr-wt/production/dance-proof-3d/build_dance.py"),
    ("production/dance-proof-3d/render_frames.py", "pr-wt/production/dance-proof-3d/render_frames.py"),
    ("production/dance-proof-3d/README.md", "pr-wt/production/dance-proof-3d/README.md"),
]

def api(method, path, payload=None):
    cmd = ["gh", "api", f"repos/{REPO}/{path}", "-X", method]
    inp = None
    if payload is not None:
        cmd += ["--input", "-"]
        inp = json.dumps(payload)
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        print("API FAIL", method, path, r.stderr.strip()[:400]); sys.exit(1)
    return json.loads(r.stdout)

parent_commit = api("GET", f"git/commits/{PARENT}")
base_tree = parent_commit["tree"]["sha"]
print("base_tree:", base_tree)

entries = []
for repo_path, local in FILES:
    with open(local, "rb") as f:
        raw = f.read()
    blob = api("POST", "git/blobs", {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
    print("blob:", repo_path, blob["sha"], len(raw), "bytes")
    entries.append({"path": repo_path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

new_tree = api("POST", "git/trees", {"base_tree": base_tree, "tree": entries})
print("new_tree:", new_tree["sha"])

msg = ("3D dance proof v3: full EN song, full world cycle, closer camera, foot-skate fix\n\n"
       "- build_dance.py: scene_v3 - full 75.79 s timeline (1824 frames), five-section\n"
       "  world cycle (day / LED magenta / LED cyan / night / day), camera closer\n"
       "  (0,-2.45,0.60 @ 38 mm), narrowed plant peaks + dwell-hold anchors to cut\n"
       "  foot-skate; v2 one-piece parametric cape carried over unchanged.\n"
       "- render_frames.py: per-frame save verification (size + JPEG end-marker)\n"
       "  with a long retry ladder - this box's storage intermittently drops writes.\n"
       "- README.md: v3 section with measured spec results (torso 10.3%, foot 17.7%,\n"
       "  ratio 1.72, 48/48 distinct) and zoom-check results (one continuous cloth).\n"
       "No files deleted.")
commit = api("POST", "git/commits", {"message": msg, "tree": new_tree["sha"], "parents": [PARENT]})
print("commit:", commit["sha"])

ref = api("POST", "git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit["sha"]})
print("ref created:", ref["ref"], ref["object"]["sha"])
