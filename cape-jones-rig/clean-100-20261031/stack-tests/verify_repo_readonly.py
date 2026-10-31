#!/usr/bin/env python3
"""READ-ONLY repo verification for mhvnsnt/cape-jones main.
Uses ~/workspace/cape-jones-rig-repo-batch/gh_api.py (GET only, no token printed).
Writes: repo-main-tree.json (paths only, no content download), repo-verification.json.
No push, no commit, no delete."""
import json, os, sys
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig-repo-batch")
from gh_api import req

OUT = "/home/hatch/workspace/cape-jones-rig/clean-100-20261031/stack-tests"
os.makedirs(OUT, exist_ok=True)

def get(path):
    st, body = req("GET", path)
    print(f"GET {path} -> {st}")
    return st, body

st, repo = get("/repos/mhvnsnt/cape-jones")
st, branch = get("/repos/mhvnsnt/cape-jones/branches/main")
sha = branch.get("commit", {}).get("sha") if isinstance(branch, dict) else None
print("main head:", sha)
st, tree = get(f"/repos/mhvnsnt/cape-jones/git/trees/{sha}?recursive=1" if sha else "/repos/mhvnsnt/cape-jones/git/trees/main?recursive=1")
paths = []
if isinstance(tree, dict):
    for e in tree.get("tree", []):
        if e.get("type") == "blob":
            paths.append({"path": e["path"], "size": e.get("size"), "sha": e.get("sha")})
    print("tree truncated:", tree.get("truncated"), "blobs:", len(paths))
with open(os.path.join(OUT, "repo-main-tree.json"), "w") as f:
    json.dump({"repo": repo.get("full_name") if isinstance(repo, dict) else None,
               "default_branch": repo.get("default_branch") if isinstance(repo, dict) else None,
               "main_head": sha,
               "tree_truncated": tree.get("truncated") if isinstance(tree, dict) else None,
               "blobs": paths}, f, indent=2)
# Checklist: post-#285/#287-era local files to check on main (cape-jones-rig/ prefix on repo)
CHECK = [
 "cape-jones-rig/joint_locked_rig_v7c.py",
 "cape-jones-rig/rig-apose-v7c-clean-transparent.png",
 "cape-jones-rig/cut-limbs-v7c-gauntlet-out-fixed/Arm_Front_Lower_OutFixed.png",
 "cape-jones-rig/cut-limbs-v7c-gauntlet-out-fixed/Arm_Back_Lower_OutFixed.png",
 "cape-jones-rig/cut-limbs-v7c-flex-out/Arm_Front_Lower_FlexOut.png",
 "cape-jones-rig/reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png",
 "cape-jones-rig/reposes-v7c-clean/true-flex-double-bicep-v7c-clean.png",
 "cape-jones-rig/reposes-v7c-clean/true-flex-double-bicep-gauntlet-out-fist-in-roll-v7c-clean.png",
 "cape-jones-rig/clips-v7c-clean-20261031/flex/true-flex-double-bicep-v7c-clean.png",
 "cape-jones-rig/apply_lighting_level2_v2.py",
 "cape-jones-rig/showcase/lighting-level2-v2/level-2-v2-colored-warm-rim-20261031.png",
 "cape-jones-rig/showcase/luts-spectrum-v2/lut-33-blue-violet-normal.cube",
 "cape-jones-rig/showcase/luts-spectrum-v2/lut-33-magenta-rose-deep.cube",
 "cape-jones-rig/showcase/lut-neutral.cube",
 "cape-jones-rig/showcase/lut-warm.cube",
 "cape-jones-rig/LIGHTING-LEVELS-0-5.md",
 "cape-jones-rig/RIM-COLOR-RULE.md",
 "cape-jones-rig/GAUNTLET-FLIP-RULE.md",
 "cape-jones-rig/STATUS-20261031-1428.md",
 "cape-jones-rig/TRACKER-20261031.md",
 "cape-jones-rig/COMPARISON-TESTS.md",
 "cape-jones-rig/FREE-FIRST-WIRING.md",
 "cape-jones-rig/pack4-20261031/PACK4-REPORT-20261031.md",
 "cape-jones-rig/pack4-20261031/pack4-manifest-20261031.json",
 "cape-jones-rig/pack4-20261031/visemes/viseme-01-rest-20261031.png",
 "cape-jones-rig/pack4-20261031/eye-strips/eye-strip-01-determined-focused-20261031.png",
 "cape-jones-rig/pack4-20261031/cape-states/cape-billowing-20261031.png",
 "cape-jones-rig/pack4-20261031/head-34-front-derived-20261031.png",
 "cape-jones-rig/clips-v7c-clean-20261031/walk/walk-01-contact-v7c-clean.png",
 "cape-jones-rig/12-PRINCIPLES-CHECKLIST-20261031.md",
 "cape-jones-rig/UNIVERSAL-PIPELINE.md",
 "cape-jones-rig/UNIVERSE-COLOR-LANGUAGE.md",
]
bymap = {p["path"]: p for p in paths}
results = []
for c in CHECK:
    hit = bymap.get(c)
    local = "/home/hatch/workspace/cape-jones-rig/" + c[len("cape-jones-rig/"):]
    lsize = os.path.getsize(local) if os.path.exists(local) else None
    results.append({"repo_path": c, "on_main": bool(hit),
                    "repo_size": hit["size"] if hit else None,
                    "repo_sha": hit["sha"] if hit else None,
                    "local_size": lsize,
                    "size_match": (hit["size"] == lsize) if hit and lsize is not None else False})
    print(("PRESENT " if hit else "MISSING ") + c, "repo_size=", hit["size"] if hit else None, "local_size=", lsize)
# FLA / 7z filename search in tree only (listing, no download)
fla = [p["path"] for p in paths if p["path"].lower().endswith(".fla")]
z7 = [p["path"] for p in paths if p["path"].lower().endswith((".7z", ".rar", ".zip"))]
print("FLA in cape-jones tree:", fla)
print("ARCHIVES in cape-jones tree:", z7[:50])
out = {"main_head": sha, "total_blobs_on_main": len(paths),
       "checklist_total": len(CHECK),
       "checklist_present": sum(1 for r in results if r["on_main"]),
       "results": results, "fla_paths": fla, "archive_paths": z7}
with open(os.path.join(OUT, "repo-verification.json"), "w") as f:
    json.dump(out, f, indent=2)
print(f"CHECKLIST {out['checklist_present']}/{out['checklist_total']} present on main")
