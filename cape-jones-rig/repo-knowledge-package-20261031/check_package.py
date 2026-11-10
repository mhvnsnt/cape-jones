#!/usr/bin/env python3
"""Knowledge-package gate: verifies the package is complete and that
the approved true-final-flex file has not changed. Exit 0 = PASS.
Run from ~/workspace/cape-jones-rig/repo-knowledge-package-20261031/ .
This is the wiring that makes the package a CHECK, not just a doc:
a future worker runs this before claiming the knowledge is intact."""
import hashlib, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RIG = os.path.dirname(HERE)
REQUIRED = ["README-INDEX-20261031.md", "CONSOLIDATED-RULES-20261031.md",
    "APPROVALS-LEDGER-20261031.md", "METHODS-INDEX-20261031.md",
    "GAPS-OWED-20261031.md", "MEMORY-NOTE-20261031.md",
    "WIRE100-SWEEP-20261031.md", "ADR-20261031.md",
    "PUSH-HANDOFF-20261031.md"]
GATES = [("face-cowl-snap-wire100-20261031/check_pose_snap.py", True),
    ("face-cowl-snap-wire100-20261031/audit-wire100-20261031.csv", True),
    ("face-cowl-snap-wire100-20261031/snap_figure.py", True),
    ("check_gauntlet_flip.py", True), ("check_arm_alignment.py", True)]
fails = []
for f in REQUIRED:
    if not os.path.exists(os.path.join(HERE, f)): fails.append(f"missing package file: {f}")
for rel, _ in GATES:
    if not os.path.exists(os.path.join(RIG, rel)): fails.append(f"missing gate/tool: {rel}")
tf = os.path.join(RIG, "reposes-v7c-clean/true-final-flex-relaxed-clean-20261031.png")
if os.path.exists(tf):
    md5 = hashlib.md5(open(tf, "rb").read()).hexdigest()
    if md5 != "03d282c8b1c56adf3fb43bb2dfe30b9a":
        fails.append(f"true-final-flex CHANGED: {md5}")
else:
    fails.append("true-final-flex file missing")
proof = {"package_files_present": len(REQUIRED) - sum(1 for f in fails if f.startswith("missing package")),
         "package_files_required": len(REQUIRED),
         "gates_present": sum(1 for rel, _ in GATES if os.path.exists(os.path.join(RIG, rel))),
         "gates_required": len(GATES),
         "true_final_flex_md5": hashlib.md5(open(tf, "rb").read()).hexdigest() if os.path.exists(tf) else None,
         "pass": not fails, "fails": fails}
json.dump(proof, open(os.path.join(HERE, "check_package_proof.json"), "w"), indent=2)
print(json.dumps(proof, indent=2))
sys.exit(0 if not fails else 1)
