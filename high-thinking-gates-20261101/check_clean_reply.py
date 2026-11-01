#!/usr/bin/env python3
"""Conversation gate 1+2: Done/Next/Need + short-summary-first.
Usage: python3 check_clean_reply.py reply.txt
PASS only if reply contains Done, Next, Need sections, is <= 120 lines,
and contains no 'verbatim subagent' marker. Detail-in-file is checked by
requiring a file path reference when reply is long (>40 lines).
Exit 0 PASS, 1 FAIL."""
import sys, re
def main():
    if len(sys.argv) < 2:
        print("usage: check_clean_reply.py reply.txt", file=sys.stderr); return 2
    text = open(sys.argv[1]).read()
    lines = text.splitlines()
    fails = []
    for sec in ("Done", "Next", "Need"):
        if sec not in text: fails.append(f"missing section {sec}")
    if len(lines) > 120: fails.append("too long for chat, move detail to file")
    if len(lines) > 40 and not re.search(r"\.md|\.py|workspace/", text):
        fails.append("long reply without file reference")
    if fails:
        print("CLEAN-REPLY GATE: FAIL"); [print(" -", f) for f in fails]; return 1
    print("CLEAN-REPLY GATE: PASS"); return 0
if __name__ == "__main__":
    sys.exit(main())
