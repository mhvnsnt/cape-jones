# AGENTS.md — Cape Jones

Operating rules for every agent working in this repo.

## VERIFY-BEFORE-CLAIMING LAW (owner 2026-10-16)

**"The agent says it is done" is not evidence.**

Before reporting ANYTHING as done, complete, saved, uploaded, merged, or verified:

1. **Check the source of truth yourself.** Not the worker's report. Not the handoff. The actual thing:
   - File claimed to exist → check it exists (path, size, hash)
   - PR claimed merged → check via `gh pr view` (state = MERGED)
   - Upload claimed complete → check the destination lists it
   - Render claimed done → check the frames/zips are retrievable

2. **Use `production/pipeline/verify_claim.py`** for standard checks:
   ```
   python3 production/pipeline/verify_claim.py --claim "chunk 5 done" \
       --type file --path /path/to/zip --sha256 <hash>
   ```

3. **Tag your confidence:**
   - `verified` — you checked 2+ independent sources yourself
   - `single-source` — you checked one source
   - `unverified` — you haven't checked yet (say so, don't claim it)
   - `contradicted` — sources disagree (report the disagreement, don't pick a side)

4. **When someone says your work is lost:** check YOUR lane first. Don't take another agent's word that your work is gone. Verify against your own task's actual state before agreeing.

5. **Never relay a claim as fact.** If a subagent or browser task says "done," that's a claim. Your report to the user must say what YOU verified, not what you were told.

**The 2026-10-16 incident:** An agent reported render chunks as saved. The owner asked questions. The agent flipped and agreed the work was lost — without checking its own lane. Both the original claim and the retraction were unverified. The work was actually fine. This law exists so that never happens again.

## Existing laws (from workspace AGENTS.md, apply here too)

- Branch → PR → merge. Never direct to main.
- PUSH-AFTER-EVERY-TURN: push after every turn of work.
- NO-DISK-STAGING: nothing on local disk that can go straight to GitHub/TeraBox.
- PULL-STRAIGHT-TO-STORE: clone into repo checkouts, wire up there, push.
- RESEARCH-TO-REPO: all research lands in this repo's docs/, wired up and pulled in.
- ARCHIVE LAW: production materials keep their own home, never modified. Cape Jones assets live ONLY in production/assets/.
- NO-HAND-TOOLING-EDITS: rebuild from clean state, never patch edits.
- NO-CHROMA-KEY-ON-ANIMATION: AI matting or rotoscoping only.
