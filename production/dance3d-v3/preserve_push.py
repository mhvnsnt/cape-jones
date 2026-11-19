import base64, json, subprocess, sys

REPO = "mhvnsnt/cape-jones"
PARENT = "daf7cef19fa4b61f16afb811eb21121e5023c562"  # head of feature/cj-dance-proof-3d-v3-20261030 (PR #272)
BRANCH = "feature/cj-dance-3d-v3-saved-animation-20261031"
BASE = "production/dance-proof-3d/saved-animation"
STAGE = "/home/hatch/workspace/_cj-dance3d-v3/preserve"
FILES = [
    (f"{BASE}/cj-dance-3d-v3.blend", f"{STAGE}/cj-dance-3d-v3.blend"),
    (f"{BASE}/cj-dance-3d-v3.bvh", f"{STAGE}/cj-dance-3d-v3.bvh"),
    (f"{BASE}/README.md", f"{STAGE}/README.md"),
]

def api(method, path, payload=None):
    cmd = ["gh", "api", f"repos/{REPO}/{path}", "-X", method]
    inp = None
    if payload is not None:
        cmd += ["--input", "-"]
        inp = json.dumps(payload)
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    if r.returncode != 0:
        print("API FAIL", method, path, r.stderr.strip()[:500]); sys.exit(1)
    return json.loads(r.stdout)

parent_commit = api("GET", f"git/commits/{PARENT}")
base_tree = parent_commit["tree"]["sha"]
print("base_tree:", base_tree)

entries = []
for repo_path, local in FILES:
    with open(local, "rb") as f:
        raw = f.read()
    if len(raw) == 0:
        print("EMPTY FILE, ABORT:", local); sys.exit(1)
    blob = api("POST", "git/blobs", {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
    print("blob:", repo_path, blob["sha"], len(raw), "bytes")
    entries.append({"path": repo_path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

new_tree = api("POST", "git/trees", {"base_tree": base_tree, "tree": entries})
print("new_tree:", new_tree["sha"])

msg = ("Save the literal 3D dance v3 ANIMATION (owner order 2026-10-31)\n\n"
       "The rendered v3 video is not the only artifact - this saves the dance\n"
       "itself, reopenable and reusable, stacked on PR #272 (nothing overwritten,\n"
       "no files deleted, v4 lane untouched):\n\n"
       "- cj-dance-3d-v3.blend: the full v3 scene as rendered (CapeJones_Rig,\n"
       "  88 bones, BlenRig-style FK/IK rig). The original dance action is named\n"
       "  CJ_Dance_3D_V3. A second armature, CapeJones_Rig_BAKED (collection\n"
       "  SAVED_ANIMATION_BAKED), carries CJ_Dance_3D_V3_BAKED - the same motion\n"
       "  visual-baked onto every bone with constraints cleared, so the dance\n"
       "  plays back with no rig logic. Bake verified numerically against the\n"
       "  original rig (deform-bone world matrices, 10 sample frames).\n"
       "- cj-dance-3d-v3.bvh: portable motion export of the baked dance\n"
       "  (frames 1-1824, 24 fps = the full 75.79 s song length), retargetable\n"
       "  onto future rigs.\n"
       "- README.md: what this is, the loop structure, and reuse notes.\n\n"
       "The five lighting sections (day / LED magenta / LED cyan / night / day)\n"
       "are render-side world state in the .blend; the dance action is the\n"
       "character motion itself.")
commit = api("POST", "git/commits", {"message": msg, "tree": new_tree["sha"], "parents": [PARENT]})
print("commit:", commit["sha"])

ref = api("POST", "git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": commit["sha"]})
print("ref created:", ref["ref"], ref["object"]["sha"])
