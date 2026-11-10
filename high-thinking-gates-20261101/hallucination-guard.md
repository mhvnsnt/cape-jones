# 5. Hallucination / Bullshit Guard
- No invented numbers, dates, PR numbers, file names, sizes, or SHAs.
  If it is not in a tool result or a file just read, it is UNKNOWN.
- Run check_done_language.py on any draft that claims "done":
  it fails a draft that (a) says "done" for a delegated/pending step,
  (b) cites a PR/file/size with no evidence line, or (c) contains a
  banned acknowledgement-"done" phrasing.
- A failed scan means: rewrite the draft, downgrade the claim, or
  gather the evidence first — never ship the draft as-is.
- Human sign-off gate (tkmd-style pending-close): landing claims
  stay pending-close until the main-tree check passes; only then may
  a reply call them landed.
