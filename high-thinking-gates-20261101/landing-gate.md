# Landing Gate — Gate 4 of 5: High-Thinking Gates (Cape Jones, 2026-11-01)

## Pipeline (in order, no skipping)
1. **Stage** — files staged on a branch, never direct to main.
2. **Branch** — a new dated branch per landing batch
   (e.g. `feature/cape-jones-high-thinking-gates-20261101`).
3. **PR** — pull request, PR-only, 0 file deletions unless Mars approved
   that exact deletion in writing (see below).
4. **Merge gate** — merge ONLY when `mergeable_state` is `clean` (GREEN).
   If it is dirty, blocked, or behind, STOP: fix conflicts without
   clobbering other lanes, re-check, and only then merge. No force-push,
   no history rewrite, no merge on a red gate.
5. **Verify on main** — AFTER merge, verify EVERY file on main by
   size + SHA (blob SHA via the GitHub API, compared against the local
   file). A PR number, a merge receipt, or a local commit is NOT
   verification.
6. **Claim** — only after step 5 passes for every file may the batch be
   called "landed". Until then it is "PR merged, verification pending".

## Deletion rule
No deletions unless Mars approved that exact deletion in writing, naming
the exact files/versions. A general "clean up" or "delete old versions"
does NOT authorize a specific deletion. Checkpoint files are never
deleted. A PR containing an unapproved deletion is blocked.

## Verification record
Per file: repo path, local size, remote size, local SHA-256 / git blob
SHA, remote blob SHA, match YES/NO. Any mismatch = that file is still
owed, reported by name, and the batch is not 100% landed.
See landing-checklist.md for the per-run checklist.
