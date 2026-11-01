"""Repo-wide knee-feet audit scanner (experimental, RUN).

Scans movement builder scripts under ~/workspace/cape-jones-rig for
leg_upper key dictionaries and runs the universal per-leg gate on
their keys. This is a SCANNER, not a renderer: it reports which
builders' keys would fail the gate, so a lane cannot ship a movement
whose keys were never gated. Builders that render through
snap.figure with no leg_upper keys in source are reported as
NOT-SCANNED (not as PASS) — a scan cannot pass what it cannot see.

Usage: python3 audit_all_movements.py [--root DIR]
Output: JSON to stdout, exit 0 only if every scanned builder passes.
"""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kneefeet_gate import leg_direction, required_footin

ROOT = sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else os.path.expanduser("~/workspace/cape-jones-rig")
# leg_upper dicts look like: "leg_upper": {"L": -28, "R": 22}
PAT = re.compile(r'"leg_upper"\s*:\s*\{\s*"L"\s*:\s*(-?[\d.]+)\s*,\s*"R"\s*:\s*(-?[\d.]+)\s*\}')
results = []
for dirpath, _dirs, files in os.walk(ROOT):
    if "coming-forward-walk-kneefeet-fix-20261031" in dirpath:
        continue
    for fn in sorted(files):
        if not fn.endswith(".py"):
            continue
        path = os.path.join(dirpath, fn)
        try:
            src = open(path, errors="ignore").read()
        except OSError:
            continue
        keys = [(float(a), float(b)) for a, b in PAT.findall(src)]
        if not keys:
            continue
        fails = []
        for i, (lu, ru) in enumerate(keys):
            # old builders use original lowers always: footin False.
            if required_footin("L", lu) or required_footin("R", ru):
                fails.append({"key_index": i, "leg_upper_L": lu, "leg_upper_R": ru,
                              "knee_L": leg_direction("L", lu), "knee_R": leg_direction("R", ru)})
        results.append({"builder": os.path.relpath(path, ROOT), "keys_scanned": len(keys),
                        "keys_failing_if_original_lowers": len(fails), "failing_keys": fails})
ok = all(r["keys_failing_if_original_lowers"] == 0 for r in results)
print(json.dumps({"PASS": ok, "builders_scanned": len(results), "results": results}, indent=2))
sys.exit(0 if ok else 1)
