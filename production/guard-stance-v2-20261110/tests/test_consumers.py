"""Static gate: every MIGRATED consumer must call the shared loader (ensure_arm_fix / cj_arm_guard / cj_arm_fix check)
before its first pose-bone use. Run from repo root: python3 production/guard-stance-v2-20261110/tests/test_consumers.py
Phase 2a landing: also cross-checks the full 201-consumer manifest (CONSUMERS-FULL.json) so no rewire
candidate is left out of the migrated list unnoticed. .sh drivers are guarded when they route through
build_rig_v2.py (the pipeline wrapper that calls ensure_arm_fix) or call ensure_arm_fix() directly."""
import json, os, re, sys
here=os.path.dirname(os.path.abspath(__file__)); root=os.path.abspath(os.path.join(here,"..","..",".."))
man=json.load(open(os.path.join(here,"CONSUMERS.json"))); bad=[]
for c in man["migrated"]:
    p=os.path.join(root,c["path"])
    if not os.path.exists(p): bad.append((c["path"],"missing")); continue
    s=open(p).read()
    if p.endswith(".sh"):
        # shell drivers cannot call ensure_arm_fix() directly; they route through build_rig_v2.py
        if "build_rig_v2.py" not in s and "ensure_arm_fix(" not in s:
            bad.append((c["path"],"shell driver with no guard routing (want build_rig_v2.py or ensure_arm_fix)"))
        continue
    g=min([i for i in (s.find("ensure_arm_fix("),s.find("cj_arm_fix")) if i>=0] or [-1])
    u=min([m.start() for m in re.finditer(r"pose\.bones|\.matrix\s*=|keyframe_insert",s)] or [10**9])
    if g<0: bad.append((c["path"],"no guard call"))
    elif g>u: bad.append((c["path"],"guard after first pose use"))
for c in man["migrated"]: print("MIGRATED", c["path"])
for c in man["remaining_bypasses_not_migrated"]: print("BYPASS  ", c["path"], "-", c["why"])
# ---- full-manifest cross-check (Phase 2a) ----
full_p=os.path.join(here,"CONSUMERS-FULL.json")
if os.path.exists(full_p):
    full=json.load(open(full_p))["consumers"]
    mig={c["path"] for c in man["migrated"]}
    for c in full:
        if c["landing_action"]=="rewire" and c["path"] not in mig:
            bad.append((c["path"],"in full manifest as rewire but NOT in CONSUMERS.json migrated"))
    from collections import Counter
    print("MANIFEST", len(full), "consumers:", dict(Counter(c["landing_action"] for c in full)))
    print("MIGRATED-COUNT", len(mig))
else:
    print("MANIFEST MISSING:", full_p, "(cross-check skipped)")
    bad.append(("CONSUMERS-FULL.json","missing"))
print("FAIL" if bad else "PASS", bad); sys.exit(1 if bad else 0)
