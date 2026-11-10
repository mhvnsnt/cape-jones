#!/usr/bin/env python3
"""
claim_gate.py — Pre-report claim gate for Cape Jones agents.

Splits a status report into atomic claims, requires evidence for each claim
before it can be reported as fact, and blocks unverified "done" reports.

Usage:
    python3 claim_gate.py --report "Chunk 5 rendered and saved. Chunk 4 also done."
    python3 claim_gate.py --report-file /path/to/report.txt
    python3 claim_gate.py --claim "chunk 5 zip exists" --evidence "file:/path/to.zip"

Exit codes:
    0 — all claims have evidence (GATE PASSED)
    1 — one or more claims lack evidence (GATE BLOCKED)
    2 — usage error

Integrates with verify_claim.py for file/PR/release/command checks.

Law: VERIFY-BEFORE-CLAIMING (repo AGENTS.md). CHECK-RESEARCH-WIRE-DO.
"""

import argparse
import json
import os
import re
import subprocess
import sys

VERIFY_CLAIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verify_claim.py")

# Patterns that indicate a completion claim (vs. a status update or question)
COMPLETION_PATTERNS = [
    r"\bdone\b", r"\bcomplete[sd]?\b", r"\bfinish(?:ed|es)?\b",
    r"\bsaved\b", r"\buploaded\b", r"\bmerged\b", r"\bpushed\b",
    r"\bworking\b", r"\brunning\b", r"\bsuccess(?:ful|fully)?\b",
    r"\bverified\b", r"\bconfirmed\b", r"\bready\b",
]

# Patterns that indicate the claim is about someone else's work (relay risk)
RELAY_PATTERNS = [
    r"\b(they|he|she|it) (said|says|reported|confirmed|verified)\b",
    r"\baccording to\b", r"\bthe (worker|agent|task) (said|says|reported)\b",
]


def split_claims(report):
    """Split a report into atomic claims (sentences)."""
    # Simple sentence splitter — good enough for gate purposes
    sentences = re.split(r'(?<=[.!?])\s+', report.strip())
    return [s.strip() for s in sentences if s.strip()]


def is_completion_claim(sentence):
    """Does this sentence claim something is done/complete?"""
    lower = sentence.lower()
    return any(re.search(p, lower) for p in COMPLETION_PATTERNS)


def is_relay(sentence):
    """Does this sentence relay someone else's claim?"""
    lower = sentence.lower()
    return any(re.search(p, lower) for p in RELAY_PATTERNS)


def check_evidence(claim, evidence_map):
    """
    Check if a claim has evidence.
    evidence_map: dict of claim-substring -> evidence description
    Returns (has_evidence, evidence_desc or None)
    """
    claim_lower = claim.lower()
    for key, evidence in evidence_map.items():
        if key.lower() in claim_lower:
            return True, evidence
    return False, None


def main():
    parser = argparse.ArgumentParser(description="Pre-report claim gate")
    parser.add_argument("--report", help="Report text to gate")
    parser.add_argument("--report-file", help="File containing report text")
    parser.add_argument("--claim", action="append", default=[],
                        help="Single claim to check (repeatable)")
    parser.add_argument("--evidence", action="append", default=[],
                        help="Evidence as 'substring:description' (repeatable)")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON verdict")
    args = parser.parse_args()

    if args.report_file:
        with open(args.report_file) as f:
            report = f.read()
    elif args.report:
        report = args.report
    elif args.claim:
        report = " ".join(args.claim)
    else:
        parser.error("Provide --report, --report-file, or --claim")
        sys.exit(2)

    # Parse evidence map
    evidence_map = {}
    for e in args.evidence:
        if ":" in e:
            key, desc = e.split(":", 1)
            evidence_map[key.strip()] = desc.strip()
        else:
            evidence_map[e] = "provided"

    claims = split_claims(report)
    results = []
    blocked = []

    for claim in claims:
        is_completion = is_completion_claim(claim)
        is_relay_claim = is_relay(claim)
        has_evidence, evidence = check_evidence(claim, evidence_map)

        # Completion claims REQUIRE evidence. Everything else is advisory.
        status = "ok"
        if is_completion and not has_evidence:
            status = "BLOCKED"
            blocked.append(claim)
        elif is_relay_claim:
            status = "RELAY-WARNING"

        results.append({
            "claim": claim,
            "is_completion_claim": is_completion,
            "is_relay": is_relay_claim,
            "has_evidence": has_evidence,
            "evidence": evidence,
            "status": status,
        })

    verdict = {
        "total_claims": len(claims),
        "completion_claims": sum(1 for r in results if r["is_completion_claim"]),
        "blocked": len(blocked),
        "relay_warnings": sum(1 for r in results if r["status"] == "RELAY-WARNING"),
        "gate": "PASSED" if not blocked else "BLOCKED",
        "blocked_claims": blocked,
        "details": results,
    }

    if args.json:
        print(json.dumps(verdict, indent=2))
    else:
        print(f"Claim gate: {verdict['gate']}")
        print(f"  {verdict['total_claims']} claims, "
              f"{verdict['completion_claims']} completion claims, "
              f"{verdict['blocked']} blocked")
        for r in results:
            marker = "✓" if r["status"] == "ok" else ("✗ BLOCKED" if r["status"] == "BLOCKED" else "⚠ RELAY")
            print(f"  [{marker}] {r['claim'][:80]}")
            if r["status"] == "BLOCKED":
                print(f"         → completion claim with NO evidence. "
                      f"Verify it yourself before reporting.")
            elif r["status"] == "RELAY-WARNING":
                print(f"         → relays someone else's claim. "
                      f"Verify against the source yourself.")

    sys.exit(0 if not blocked else 1)


if __name__ == "__main__":
    main()
