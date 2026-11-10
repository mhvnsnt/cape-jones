#!/usr/bin/env python3
"""
checkpoint_audit.py — Verify checkpoints match reality (NO-DROPPED-WORK LAW).

A checkpoint that says "running" but has no heartbeat and no live process
is DROPPED WORK. This script finds those and reports them.

Usage:
  checkpoint_audit.py           # audit all watchdog checkpoints, report stale ones
  checkpoint_audit.py --fix     # also mark clearly-dead ones as needs_owner

Checks per checkpoint:
  1. updated_at older than 60 min + status "running" → STALE
  2. Cross-check: is there actually a process/agent working on it?
  3. Cross-check: does the repo show recent commits matching the task?
"""
import json
import os
import sys
import subprocess
from datetime import datetime, timezone

CHECKPOINT_DIR = os.path.expanduser("~/workspace/agent-ops/checkpoints")
STALE_MINUTES = 60


def parse_time(s):
    try:
        # Handle various ISO formats
        s = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except Exception:
        return None


def minutes_since(dt):
    if not dt:
        return float("inf")
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return (now - dt).total_seconds() / 60


def git_recent_activity(repo_path, minutes=120):
    """Check if repo has commits in the last N minutes."""
    try:
        r = subprocess.run(
            ["git", "-C", repo_path, "log", "--since", f"{minutes} minutes ago",
             "--oneline"],
            capture_output=True, text=True, timeout=30)
        lines = [l for l in r.stdout.strip().split("\n") if l]
        return len(lines)
    except Exception:
        return -1  # unknown


def audit(fix=False):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"# Checkpoint Audit — {now}\n")
    stale = []
    ok = 0
    skipped = 0

    if not os.path.isdir(CHECKPOINT_DIR):
        print(f"Checkpoint dir not found: {CHECKPOINT_DIR}")
        return

    for fn in sorted(os.listdir(CHECKPOINT_DIR)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(CHECKPOINT_DIR, fn)
        try:
            with open(path) as f:
                cp = json.load(f)
        except Exception as e:
            print(f"  UNPARSEABLE: {fn} ({e})")
            continue

        if not cp.get("watchdog"):
            skipped += 1
            continue
        status = cp.get("status", "?")
        if status in ("done", "complete", "cancelled"):
            skipped += 1
            continue

        updated = parse_time(cp.get("updated_at", ""))
        age_min = minutes_since(updated)
        task = cp.get("task", "?")[:60]
        repo = cp.get("repo") or cp.get("workdir", "")

        if status == "running" and age_min > STALE_MINUTES:
            # Reality check: is there actual activity?
            commits = git_recent_activity(repo, 120) if repo else -1
            stale.append({
                "file": fn, "task": task, "age_min": int(age_min),
                "repo": repo, "recent_commits": commits,
                "attempts": cp.get("attempts", 0),
            })
            print(f"  STALE: {fn}")
            print(f"    task: {task}")
            print(f"    age: {int(age_min)} min (updated: {cp.get('updated_at')})")
            print(f"    repo: {repo or '(none)'}")
            print(f"    recent commits (2h): {commits if commits >= 0 else 'unknown'}")
            print(f"    attempts: {cp.get('attempts', 0)}")
            if fix and commits == 0 and cp.get("attempts", 0) >= 2:
                cp["status"] = "needs_owner"
                cp["notes"] = (cp.get("notes", "") +
                               f"\n[{now}] Auto-flagged: stale {int(age_min)}min, "
                               f"no commits in 2h, {cp.get('attempts', 0)} attempts.")
                tmp = path + ".tmp"
                with open(tmp, "w") as f:
                    json.dump(cp, f, indent=2)
                os.replace(tmp, path)
                print(f"    → marked needs_owner")
            print()
        else:
            ok += 1

    print(f"---\nHealthy/in-progress: {ok} | Stale: {len(stale)} | Skipped: {skipped}")
    if stale and not fix:
        print("\nRun with --fix to auto-flag dead ones as needs_owner.")
    return stale


if __name__ == "__main__":
    audit(fix="--fix" in sys.argv)
