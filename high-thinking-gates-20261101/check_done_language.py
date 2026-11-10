#!/usr/bin/env python3
"""Anti-overconfidence draft scan (Gate 6: done-language).
Usage: python3 check_done_language.py draft.txt [--evidence evidence.txt]
FAIL (exit 1) if the draft:
  - says 'done' in a Done section for a step flagged delegated/pending/
    waiting/started/spawned/browser-task in the same draft, or
  - uses banned acknowledgement phrasing: 'done: i understand', 'done: noted',
    'done: received', 'done: acknowledged', or a bare 'Done:' followed only
    by an acknowledgement with no verified step, or
  - cites a PR number / merge SHA / file size with no evidence line
    (evidence file, or a line containing 'verified', 'sha', 'bytes', or
    a workspace path) in the draft.
PASS (exit 0) otherwise. This is a wording guard, not proof of truth:
a PASS still requires the author to have actually checked the evidence.
"""
import re, sys
BANNED = [
    r"done:\s*(i understand|noted|received|acknowledged|got it|ok)\b",
    r"done:\s*starting\b", r"done:\s*started\b", r"done:\s*running\b",
    r"done:\s*waiting\b", r"done:\s*spawned\b", r"done:\s*delegated\b",
]
def main():
    if len(sys.argv) < 2:
        print("usage: check_done_language.py draft.txt", file=sys.stderr); return 2
    text = open(sys.argv[1]).read()
    low = text.lower()
    fails = []
    for pat in BANNED:
        if re.search(pat, low): fails.append(f"banned acknowledgement-done: {pat}")
    # Done-section lines that themselves admit delegation/pending status
    done_lines = re.findall(r"(?im)^\s*[-*]?\s*done[:\s].*$", text)
    for ln in done_lines:
        if re.search(r"\b(spawned|delegated|pending|waiting|started|running|browser task accepted)\b", ln.lower()):
            fails.append(f"done claimed for non-completed step: {ln.strip()}")
    # PR / SHA / size claims without any evidence marker
    has_evidence = bool(re.search(r"verified|sha|bytes|workspace/|high-thinking-gates", low))
    if re.search(r"\bpr #\d+\b|merge sha|merge commit [0-9a-f]{7,}", low) and not has_evidence:
        fails.append("PR/merge claim with no evidence marker")
    if fails:
        print("DONE-LANGUAGE GATE: FAIL")
        for f in fails: print(" -", f)
        return 1
    print("DONE-LANGUAGE GATE: PASS")
    return 0
if __name__ == "__main__":
    sys.exit(main())
