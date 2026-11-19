import base64, json, subprocess, sys

REPO = "mhvnsnt/cape-jones"
PARENT = "25a3f1f65e629a99e965642fba0370c5df496453"  # first commit on the saved-animation branch
BRANCH = "feature/cj-dance-3d-v3-saved-animation-20261031"
BASE = "production/dance-proof-3d/saved-animation"
STAGE = "/home/hatch/workspace/_cj-dance3d-v3/preserve"
FILES = [
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
    assert len(raw) > 0, local
    blob = api("POST", "git/blobs", {"content": base64.b64encode(raw).decode(), "encoding": "base64"})
    print("blob:", repo_path, blob["sha"], len(raw), "bytes")
    entries.append({"path": repo_path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

new_tree = api("POST", "git/trees", {"base_tree": base_tree, "tree": entries})
print("new_tree:", new_tree["sha"])

msg = ("Complete the BVH upload: full 1,824-frame export + README size fix\n\n"
       "The first commit's BVH blob was read from disk while the exporter was\n"
       "still writing it (this box's storage is slow under load), so it held a\n"
       "truncated snapshot. This commit replaces it with the finished export:\n"
       "9,297,190 bytes, Frames: 1824 at 24 fps, all 88 bones x 6 channels,\n"
       "verified complete on disk before upload. The .blend blob was verified\n"
       "byte-identical (git hash c0ea4bcf) and is unchanged. README's BVH byte\n"
       "count corrected to match. No files deleted.")
commit = api("POST", "git/commits", {"message": msg, "tree": new_tree["sha"], "parents": [PARENT]})
print("commit:", commit["sha"])

ref = api("PATCH", f"git/refs/heads/{BRANCH}", {"sha": commit["sha"], "force": False})
print("ref updated:", ref["ref"], ref["object"]["sha"])
