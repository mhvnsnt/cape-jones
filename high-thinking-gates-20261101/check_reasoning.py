#!/usr/bin/env python3
"""Gate 1 enforcer: reasoning checklist.

Usage: python3 check_reasoning.py manifest.json [--log reasoning-log-YYYYMMDD.json]
Exits 0 only if every piece exists, is not hand-drawn, and is not guessed.
Writes a JSON log recording the decision (never overwrites an existing log
unless --force is passed; default refuses to overwrite).
"""
import hashlib
import json
import os
import sys


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("usage: check_reasoning.py manifest.json [--log out.json] [--force]",
              file=sys.stderr)
        return 2
    manifest_path = sys.argv[1]
    log_path = None
    force = False
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--log" and i + 1 < len(args):
            log_path = args[i + 1]
            i += 2
        elif args[i] == "--force":
            force = True
            i += 1
        else:
            i += 1
    with open(manifest_path) as f:
        manifest = json.load(f)
    pieces = manifest.get("pieces", [])
    results = []
    failures = []
    for p in pieces:
        part = p.get("part", "?")
        src = p.get("source", "")
        entry = {"part": part, "source": src,
                 "hand_drawn": bool(p.get("hand_drawn", False)),
                 "guessed": bool(p.get("guessed", False))}
        if not src or not os.path.isfile(src):
            entry["status"] = "FAIL"
            entry["reason"] = "source missing: %s" % src
            failures.append(entry["reason"])
        elif entry["hand_drawn"]:
            entry["status"] = "FAIL"
            entry["reason"] = "piece flagged hand-drawn"
            failures.append("%s: hand-drawn" % part)
        elif entry["guessed"]:
            entry["status"] = "FAIL"
            entry["reason"] = "piece flagged guessed label"
            failures.append("%s: guessed label" % part)
        else:
            entry["status"] = "PASS"
            entry["size_bytes"] = os.path.getsize(src)
            entry["sha256"] = sha256_of(src)
            entry["reason"] = "ok"
        results.append(entry)
    log = {"build": manifest.get("build", "?"),
           "pieces": results,
           "overall": "FAIL" if failures else "PASS",
           "failures": failures}
    if log_path:
        if os.path.exists(log_path) and not force:
            print("refusing to overwrite existing log: %s" % log_path,
                  file=sys.stderr)
            return 2
        with open(log_path, "w") as f:
            json.dump(log, f, indent=2)
    print(json.dumps(log, indent=2))
    if failures:
        print("REASONING GATE: FAIL (%d failure(s)) — do not build"
              % len(failures), file=sys.stderr)
        return 1
    print("REASONING GATE: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
