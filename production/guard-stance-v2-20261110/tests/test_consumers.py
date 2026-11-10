"""Static gate: every MIGRATED consumer must call the shared loader (ensure_arm_fix / cj_arm_guard / cj_arm_fix check)
before its first pose-bone use. Run from repo root: python3 production/guard-stance-v2-20261110/tests/test_consumers.py"""
import json, os, re, sys
here=os.path.dirname(os.path.abspath(__file__)); root=os.path.abspath(os.path.join(here,"..","..",".."))
man=json.load(open(os.path.join(here,"CONSUMERS.json"))); bad=[]
for c in man["migrated"]:
    p=os.path.join(root,c["path"])
    if not os.path.exists(p): bad.append((c["path"],"missing")); continue
    s=open(p).read(); g=min([i for i in (s.find("ensure_arm_fix("),s.find("cj_arm_fix")) if i>=0] or [-1])
    u=min([m.start() for m in re.finditer(r"pose\.bones|\.matrix\s*=|keyframe_insert",s)] or [10**9])
    if g<0: bad.append((c["path"],"no guard call"))
    elif g>u: bad.append((c["path"],"guard after first pose use"))
for c in man["migrated"]: print("MIGRATED", c["path"])
for c in man["remaining_bypasses_not_migrated"]: print("BYPASS  ", c["path"], "-", c["why"])
print("FAIL" if bad else "PASS", bad); sys.exit(1 if bad else 0)
