#!/usr/bin/env python3
"""Gate for the general mouth-clean pipeline. Exit 0 PASS, 1 FAIL.
Re-reads measurements-general-pipeline-20261031.json and re-checks,
for every entry: kept <= source (G1, subset, no invented pixels) and
kept >= 30 (G2, mouth present)."""
import json, sys, os
p = os.path.join(os.path.dirname(__file__), 'measurements-general-pipeline-20261031.json')
d = json.load(open(p))
bad = [k for k, v in d.items() if not (v['kept_alpha'] <= v['src_alpha'] and v['kept_alpha'] >= 30)]
print(f"{len(d) - len(bad)}/{len(d)} PASS" + (f", FAIL: {bad}" if bad else ""))
sys.exit(1 if bad else 0)
