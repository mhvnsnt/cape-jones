# Landing Checklist — Gate 4 of 5 (companion to landing-gate.md)

Run per landing batch. Check each box in order; do not claim "landed"
until the verification section is complete.

## Before upload
- [ ] Branch name is new and dated; branch created from current main.
- [ ] File list is final; every file is an addition (0 deletions) unless
      Mars approved that exact deletion in writing — quote the approval.
- [ ] No checkpoint file, no Mars-seen version, is overwritten or deleted.
- [ ] Local size + SHA recorded per file before upload.

## PR + merge
- [ ] PR opened from the branch to main; PR number/URL recorded.
- [ ] `mergeable_state` checked and = `clean` (GREEN) before merging.
- [ ] If not clean: stopped, conflicts resolved without clobbering, re-checked.
- [ ] No force-push, no history rewrite.
- [ ] Merge SHA recorded.

## Verification on main (after merge, per file)
- [ ] File present on main via GitHub API (200, correct path).
- [ ] Remote size matches local size.
- [ ] Remote blob SHA matches local git blob SHA.
- [ ] Mismatch / 404 recorded as still-owed by filename, not hidden.

## Report (compact)
- Files uploaded: N
- PR number + URL:
- Merge SHA:
- Verified: N / total
- Still owed (by name, or "none"):

## No-claim rule
Until verified = total, the report line is "PR merged, verification
pending (N/total verified)" — never "landed".
