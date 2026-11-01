#!/usr/bin/env python3
"""Gate 4 test: choice-first. A build manifest must list chosen pieces only.
Usage: python3 choice_first_check.py manifest.json
Manifest: {"pieces":[{"part":..,"chosen":true/false,"source":..}]}
PASS only if every piece is chosen=true and has a source. Guessed/unchosen => FAIL, stop, show options."""
import json, sys
def main():
    if len(sys.argv) < 2:
        print("usage: choice_first_check.py manifest.json", file=sys.stderr); return 2
    m = json.load(open(sys.argv[1])); fails = []
    for p in m.get("pieces", []):
        if not p.get("chosen"): fails.append(f"{p.get('part','?')}: not chosen by Mars")
        if not p.get("source"): fails.append(f"{p.get('part','?')}: no source")
    if fails:
        print("CHOICE-FIRST GATE: FAIL"); [print(" -", f) for f in fails]; return 1
    print("CHOICE-FIRST GATE: PASS"); return 0
if __name__ == "__main__":
    sys.exit(main())
