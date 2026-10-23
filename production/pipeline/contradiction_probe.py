#!/usr/bin/env python3
"""
contradiction_probe.py — Adversarial self-check before reporting anything as "done."

The problem it solves: agents present unverified claims as fact because nothing
forces them to consider disconfirming evidence. This script structures the
adversarial question: "what would prove this claim FALSE?"

Usage:
    python3 contradiction_probe.py --claim "chunk 5 saved to Kaggle"

    The script prompts interactively:
      1. What evidence would prove this TRUE? Do you have it?
      2. What evidence would prove this FALSE? Have you checked for it?
      3. What channel did the work? What INDEPENDENT channel verifies it?
      4. Confidence tag: verified | single-source | unverified | contradicted

    It writes a JSON record to stdout. Exit 0 only if confidence is
    "verified" or "single-source" AND disconfirming evidence was checked.

    For non-interactive use:
      python3 contradiction_probe.py --claim "..." --confirming "gh pr view #40" \\
          --disconfirming "checked: no contradicting evidence found" \\
          --channel "gh CLI (independent of browser task)" --confidence single-source

The rule: if you cannot name what would prove the claim false, you have not
verified it. Do not report it as done.
"""

import argparse
import json
import sys
from datetime import datetime, timezone


def prompt(q, required=True):
    """Prompt for input. Empty answer to a required question aborts."""
    try:
        ans = input(f"{q}\n> ").strip()
    except EOFError:
        ans = ""
    if required and not ans:
        print("ABORTED: this question is required. Unanswered = unverified.",
              file=sys.stderr)
        sys.exit(3)
    return ans


def main():
    p = argparse.ArgumentParser(
        description="Contradiction probe: adversarial check before claiming done.")
    p.add_argument("--claim", required=True, help="The claim to probe")
    p.add_argument("--confirming", default=None,
                   help="Evidence that would prove it TRUE (and that you have)")
    p.add_argument("--disconfirming", default=None,
                   help="Evidence you checked that would prove it FALSE")
    p.add_argument("--channel", default=None,
                   help="Independent verification channel (not the one that did the work)")
    p.add_argument("--confidence", default=None,
                   choices=["verified", "single-source", "unverified", "contradicted"],
                   help="Confidence tag")
    p.add_argument("--non-interactive", action="store_true",
                   help="Fail instead of prompting when args are missing")
    args = p.parse_args()

    def get(name, value, question):
        if value:
            return value
        if args.non_interactive:
            print(f"ABORTED: --{name} is required in non-interactive mode.",
                  file=sys.stderr)
            sys.exit(3)
        return prompt(question)

    confirming = get("confirming", args.confirming,
                     "1. What evidence would prove this claim TRUE — and do you actually have it?\n   (Name the specific check: file path + hash, command + output, URL, etc.)")
    disconfirming = get("disconfirming", args.disconfirming,
                        "2. What evidence would prove this claim FALSE — and did you check for it?\n   (If you cannot name disconfirming evidence, you have not verified the claim.)")
    channel = get("channel", args.channel,
                  "3. What channel did the work, and what INDEPENDENT channel verifies it?\n   (Two-channel rule: never verify through the same channel that did the work.)")
    confidence = get("confidence", args.confidence,
                     "4. Confidence tag: verified | single-source | unverified | contradicted\n   (verified = 2+ independent sources checked yourself)")

    # The gate: disconfirming evidence must have been actively checked,
    # and confidence must not be unverified/contradicted.
    disconfirming_checked = bool(disconfirming and
                                "not checked" not in disconfirming.lower() and
                                "n/a" not in disconfirming.lower() and
                                "none" not in disconfirming.lower())
    confidence_ok = confidence in ("verified", "single-source")

    passed = disconfirming_checked and confidence_ok

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": "contradiction_probe",
        "claim": args.claim,
        "confirming_evidence": confirming,
        "disconfirming_evidence_checked": disconfirming,
        "disconfirming_actively_checked": disconfirming_checked,
        "independent_channel": channel,
        "confidence": confidence,
        "verdict": "CLEARED" if passed else "BLOCKED",
        "block_reason": None if passed else (
            "disconfirming evidence not actively checked"
            if not disconfirming_checked else
            f"confidence is '{confidence}' — do not report as done"
        ),
    }
    print(json.dumps(record, indent=2))

    if not passed:
        print(f"\nBLOCKED: {record['block_reason']}", file=sys.stderr)
        print("Do not report this claim as done.", file=sys.stderr)
        sys.exit(1)
    print("\nCLEARED: claim may be reported with its confidence tag.")
    sys.exit(0)


if __name__ == "__main__":
    main()
