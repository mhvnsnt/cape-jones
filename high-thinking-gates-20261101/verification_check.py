#!/usr/bin/env python3
"""Gate 5 test: verification-before-claim.
Usage: python3 verification_check.py claim.json
PASS only if verified_on_main is true and evidence is non-empty."""
import json, sys
def main():
    if len(sys.argv) < 2:
        print("usage: verification_check.py claim.json", file=sys.stderr); return 2
    c = json.load(open(sys.argv[1]))
    if c.get("verified_on_main") and c.get("evidence"):
        print("VERIFICATION GATE: PASS"); return 0
    print("VERIFICATION GATE: FAIL — claim not verified, do not say landed/approved"); return 1
if __name__ == "__main__":
    sys.exit(main())
