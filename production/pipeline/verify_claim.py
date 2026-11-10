#!/usr/bin/env python3
"""
verify_claim.py — Verification checklist before reporting anything as "done."

Usage:
    python3 verify_claim.py --claim "chunk 5 rendered" --type file \
        --path /kaggle/working/pantera_chunk05.zip --sha256 abc123...

    python3 verify_claim.py --claim "PR merged" --type github-pr \
        --repo mhvnsnt/cape-jones --pr 37

    python3 verify_claim.py --claim "upload complete" --type terabox \
        --path "/game-files/tekken7/" --expected-size 3221225472

The point: "the agent says it is done" is not evidence.
Every claim gets checked against the source of truth before it's reported.

Exit codes:
    0 = VERIFIED (all checks passed)
    1 = UNVERIFIED (checks failed or couldn't run)
    2 = CONTRADICTED (evidence disagrees with claim)
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def log(result, claim, evidence, confidence):
    """Print a structured verification record."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "claim": claim,
        "verdict": result,  # VERIFIED | UNVERIFIED | CONTRADICTED
        "confidence": confidence,  # verified | single-source | unverified | contradicted
        "evidence": evidence,
    }
    print(json.dumps(record, indent=2))
    return record


def verify_file(path, expected_sha256=None, expected_size=None, claim=""):
    """Verify a file exists with optional hash/size check."""
    evidence = {"path": path}
    if not os.path.exists(path):
        return log("CONTRADICTED", claim,
                    {**evidence, "error": "file does not exist"},
                    "contradicted"), 2

    actual_size = os.path.getsize(path)
    evidence["size_bytes"] = actual_size

    if expected_size is not None and actual_size != expected_size:
        return log("CONTRADICTED", claim,
                    {**evidence, "expected_size": expected_size,
                     "error": "size mismatch"},
                    "contradicted"), 2

    if expected_sha256:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        actual_hash = h.hexdigest()
        evidence["sha256"] = actual_hash
        if actual_hash != expected_sha256.lower():
            return log("CONTRADICTED", claim,
                        {**evidence, "expected_sha256": expected_sha256,
                         "error": "hash mismatch"},
                        "contradicted"), 2

    confidence = "verified" if expected_sha256 else "single-source"
    return log("VERIFIED", claim, evidence, confidence), 0


def verify_github_pr(repo, pr_number, claim=""):
    """Verify a PR exists and is merged via gh CLI."""
    evidence = {"repo": repo, "pr": pr_number}
    try:
        out = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--repo", repo,
             "--json", "state,mergedAt,url"],
            capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return log("UNVERIFIED", claim,
                        {**evidence, "error": out.stderr.strip()},
                        "unverified"), 1
        data = json.loads(out.stdout)
        evidence["state"] = data.get("state")
        evidence["merged_at"] = data.get("mergedAt")
        evidence["url"] = data.get("url")
        if data.get("state") == "MERGED":
            return log("VERIFIED", claim, evidence, "verified"), 0
        return log("CONTRADICTED", claim,
                    {**evidence, "error": f"PR state is {data.get('state')}, not MERGED"},
                    "contradicted"), 2
    except Exception as e:
        return log("UNVERIFIED", claim,
                    {**evidence, "error": str(e)}, "unverified"), 1


def verify_github_release(repo, tag, claim=""):
    """Verify a release exists and is published (not draft)."""
    evidence = {"repo": repo, "tag": tag}
    try:
        out = subprocess.run(
            ["gh", "release", "view", tag, "--repo", repo,
             "--json", "isDraft,assets"],
            capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return log("UNVERIFIED", claim,
                        {**evidence, "error": out.stderr.strip()},
                        "unverified"), 1
        data = json.loads(out.stdout)
        evidence["is_draft"] = data.get("isDraft")
        evidence["asset_count"] = len(data.get("assets", []))
        if data.get("isDraft"):
            return log("CONTRADICTED", claim,
                        {**evidence, "error": "release is DRAFT, not published"},
                        "contradicted"), 2
        return log("VERIFIED", claim, evidence, "verified"), 0
    except Exception as e:
        return log("UNVERIFIED", claim,
                    {**evidence, "error": str(e)}, "unverified"), 1


def verify_command(cmd, expect_in_output=None, claim=""):
    """Run a command and check it succeeds (optionally check output)."""
    evidence = {"command": cmd}
    try:
        out = subprocess.run(cmd, shell=True, capture_output=True,
                             text=True, timeout=60)
        evidence["returncode"] = out.returncode
        evidence["stdout_tail"] = out.stdout.strip()[-500:]
        if out.returncode != 0:
            return log("CONTRADICTED", claim,
                        {**evidence, "stderr": out.stderr.strip()[-500:]},
                        "contradicted"), 2
        if expect_in_output and expect_in_output not in out.stdout:
            return log("CONTRADICTED", claim,
                        {**evidence, "error": f"expected '{expect_in_output}' in output"},
                        "contradicted"), 2
        return log("VERIFIED", claim, evidence, "single-source"), 0
    except Exception as e:
        return log("UNVERIFIED", claim,
                    {**evidence, "error": str(e)}, "unverified"), 1


def main():
    p = argparse.ArgumentParser(
        description="Verify a claim against its source of truth before reporting it.")
    p.add_argument("--claim", required=True, help="The claim to verify")
    p.add_argument("--type", required=True,
                   choices=["file", "github-pr", "github-release", "command"],
                   help="What kind of evidence to check")
    p.add_argument("--path", help="File path (for --type file)")
    p.add_argument("--sha256", help="Expected SHA256 (for --type file)")
    p.add_argument("--size", type=int, help="Expected size in bytes (for --type file)")
    p.add_argument("--repo", help="GitHub repo like mhvnsnt/cape-jones")
    p.add_argument("--pr", type=int, help="PR number (for --type github-pr)")
    p.add_argument("--tag", help="Release tag (for --type github-release)")
    p.add_argument("--cmd", help="Shell command (for --type command)")
    p.add_argument("--expect", help="String expected in command output")
    args = p.parse_args()

    if args.type == "file":
        if not args.path:
            print("ERROR: --path required for --type file", file=sys.stderr)
            return 1
        _, code = verify_file(args.path, args.sha256, args.size, args.claim)
    elif args.type == "github-pr":
        if not args.repo or not args.pr:
            print("ERROR: --repo and --pr required", file=sys.stderr)
            return 1
        _, code = verify_github_pr(args.repo, args.pr, args.claim)
    elif args.type == "github-release":
        if not args.repo or not args.tag:
            print("ERROR: --repo and --tag required", file=sys.stderr)
            return 1
        _, code = verify_github_release(args.repo, args.tag, args.claim)
    elif args.type == "command":
        if not args.cmd:
            print("ERROR: --cmd required for --type command", file=sys.stderr)
            return 1
        _, code = verify_command(args.cmd, args.expect, args.claim)

    return code


if __name__ == "__main__":
    sys.exit(main())
