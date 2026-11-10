#!/usr/bin/env python3
"""Clip pipeline gate: only finished, QC-passed, non-debug shots enter a clip plan.
Usage: python3 clip_pipeline.py shots.csv
CSV columns: shot_id,status,qc,debug_labels,audio_lufs
Exits 0 if at least one eligible clip exists and no ineligible shot was planned.
Prints a clip plan (15-60s, vertical+horizontal, hook first 2s) for eligible shots only.
No posting, no upload, no paid action."""
import csv, sys
def main():
    if len(sys.argv) < 2:
        print("usage: clip_pipeline.py shots.csv", file=sys.stderr); return 2
    eligible, blocked = [], []
    with open(sys.argv[1], newline="") as f:
        for row in csv.DictReader(f):
            sid = row.get("shot_id", "?")
            if row.get("status") != "finished":
                blocked.append((sid, "not finished")); continue
            if row.get("qc") != "pass":
                blocked.append((sid, "QC not pass")); continue
            if row.get("debug_labels", "no") == "yes":
                blocked.append((sid, "debug labels present")); continue
            eligible.append(sid)
    for sid in eligible:
        print(f"CLIP {sid}: 15-60s, vertical+horizontal, hook first 2s, caption, thumbnail/title, finished work only")
    print(f"ELIGIBLE {len(eligible)} BLOCKED {len(blocked)}")
    for sid, why in blocked:
        print(f"BLOCKED {sid}: {why}")
    return 0 if eligible else 1
if __name__ == "__main__":
    sys.exit(main())
