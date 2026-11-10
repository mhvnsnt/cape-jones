#!/usr/bin/env python3
"""Apply Mars's eye corrections. Input: proposals.json + a corrections
file in the mars_corrections.txt format (piece_id = name | status).
Output: corrected.json + a change report printed on stdout.
Mars never touches code: he edits plain text, this script applies it.
Usage: apply_corrections.py <proposals.json> <mars_corrections.txt> <out.json>
Statuses: keep (no change), rename (new canonical name), reject, good
(confirm the proposal as correct — counts as Mars-verified).
"""
import sys, json

def main():
    props = json.load(open(sys.argv[1]))
    plist = props["proposals"] if isinstance(props, dict) else props
    by_id = {p["piece_id"]: p for p in plist}
    changes = []
    for line in open(sys.argv[2]):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        pid, rest = [x.strip() for x in line.split("=", 1)]
        name, _, status = rest.partition("|")
        name, status = name.strip(), status.strip() or "keep"
        p = by_id.get(pid)
        if not p:
            changes.append({"piece_id": pid, "result": "UNKNOWN piece_id, skipped"})
            continue
        old = (p["canonical"], p["status"])
        if status == "keep":
            continue
        if status == "rename":
            p["canonical"], p["mars_corrected"] = name, True
        elif status == "reject":
            p["status"] = "reject"
        elif status == "good":
            p["mars_verified"] = True
        changes.append({"piece_id": pid, "from": old, "to": (p["canonical"], p["status"]), "action": status})
    out = {"count": len(plist), "changes": changes, "proposals": plist}
    json.dump(out, open(sys.argv[3], "w"), indent=2)
    print(json.dumps({"changed": len(changes), "changes": changes}, indent=2))

if __name__ == "__main__":
    main()
