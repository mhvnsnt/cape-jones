#!/usr/bin/env python3
"""Land duplicate-review-ui-v2-20261031 to mhvnsnt/cape-jones, PR-only, additions only.
New branch only; G1 branch untouched. Verifies size+SHA on main after merge."""
import base64, hashlib, json, os, sys, time
sys.path.insert(0, "/home/hatch/workspace/cape-jones-rig-repo-batch")
from gh_api import req

REPO = "mhvnsnt/cape-jones"
SRC = "/home/hatch/workspace/cape-jones-rig/duplicate-review-ui-v2-20261031"
BRANCH = "feature/duplicate-review-ui-v2-20261031"
FILES = ["README.md", "build_data.py", "patch_v2.py", "index.html", "index.template.html",
         "data/duplicate-groups.json",
         "contacts/ui-layout-proof-20261031.png",
         "contacts/v2-features-proof-20261031.png",
         "contacts/walkthrough-group-DG-01-20261031.png",
         "contacts/walkthrough-group-DG-23-20261031.png"]

def blob_sha(data):
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()

def call(method, path, payload=None, tries=5):
    for i in range(tries):
        s, out = req(method, path, payload)
        if s < 500:
            return s, out
        time.sleep(2 * (i + 1))
    return s, out

def main():
    s, main_br = call("GET", f"/repos/{REPO}/branches/main")
    assert s == 200, main_br
    main_sha = main_br["commit"]["sha"]
    print("main head:", main_sha)
    s, br = call("GET", f"/repos/{REPO}/branches/{BRANCH}")
    if s == 404:
        s, br = call("POST", f"/repos/{REPO}/git/refs", {"ref": f"refs/heads/{BRANCH}", "sha": main_sha})
        assert s in (200, 201), br
        print("branch created:", BRANCH)
    else:
        print("branch already exists, reusing (no force-push):", BRANCH)
    for rel in FILES:
        local = os.path.join(SRC, rel)
        data = open(local, "rb").read()
        remote_path = f"duplicate-review-ui-v2-20261031/{rel}"
        # check existing on branch
        s, cur = call("GET", f"/repos/{REPO}/contents/{remote_path}?ref={BRANCH}")
        if s == 200 and cur.get("sha") == blob_sha(data):
            print("skip identical:", rel); continue
        payload = {"message": f"Add duplicate-review-ui-v2-20261031/{rel} (UI v2, 10 new features, candidates only)",
                   "content": base64.b64encode(data).decode(), "branch": BRANCH}
        if s == 200:
            payload["sha"] = cur["sha"]
        s, out = call("PUT", f"/repos/{REPO}/contents/{remote_path}", payload)
        assert s in (200, 201), (rel, out)
        print("uploaded:", rel, len(data), blob_sha(data))
    s, pr = call("POST", f"/repos/{REPO}/pulls", {
        "title": "Add duplicate-review-ui-v2-20261031 (10 new features, candidates only, no deletions)",
        "head": BRANCH, "base": "main",
        "body": "Duplicate-review UI v2: 5 industry (keyboard shortcuts, bulk select/actions, undo, indexed search, export validation) + 5 experimental (near-duplicate preview, auto-label suggestions, confidence scoring, pixel-diff compare, progress persistence) wired into the static HTML. Data: 24 exact-MD5 groups / 59 items, identical to v1. Additions only, 0 deletions. UI only records keep/delete candidates; it deletes nothing. Note: tile images reference ../transparent-plates-grok-full-sweep-20261031/plates/ which is in the still-running G1 batch, not on main yet — tiles load once G1 merges, or locally next to that folder."})
    assert s in (200, 201), pr
    num = pr["number"]; print("PR:", num, pr["html_url"])
    # merge gate: wait for mergeable
    for _ in range(20):
        s, pr2 = call("GET", f"/repos/{REPO}/pulls/{num}")
        if pr2.get("mergeable"):
            break
        time.sleep(10)
    print("mergeable:", pr2.get("mergeable"), "state:", pr2.get("mergeable_state"))
    assert pr2.get("mergeable"), pr2
    s, merged = call("PUT", f"/repos/{REPO}/pulls/{num}/merge", {"merge_method": "merge"})
    assert s == 200 and merged.get("merged"), merged
    print("merged:", merged.get("sha"))
    # verify on main
    time.sleep(5)
    ok = 0
    for rel in FILES:
        local = open(os.path.join(SRC, rel), "rb").read()
        s, cur = call("GET", f"/repos/{REPO}/contents/duplicate-review-ui-v2-20261031/{rel}?ref=main")
        assert s == 200, (rel, cur)
        match = cur.get("sha") == blob_sha(local) and cur.get("size") == len(local)
        print(("VERIFIED " if match else "MISMATCH ") + rel, cur.get("size"), len(local), cur.get("sha"))
        ok += int(match)
    print(f"VERIFIED {ok}/{len(FILES)}")
    json.dump({"pr": num, "merge_sha": merged.get("sha"), "verified": ok, "total": len(FILES)},
              open("/home/hatch/workspace/cape-jones-rig/duplicate-review-ui-v2-20261031/LANDING-VERIFICATION-20261031.json", "w"), indent=1)
    assert ok == len(FILES)

if __name__ == "__main__":
    main()
