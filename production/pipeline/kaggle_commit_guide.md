# Kaggle Commit Guide — For Browser Operators

**The #1 rule: Quick Save does NOT save your output files. Ever.**

## When to use what

| Situation | Action | Why |
|-----------|--------|-----|
| Chunk finished rendering, need to preserve the zip | **Save & Run All** (commit) | ONLY this captures `/kaggle/working/` files |
| Just saving code changes, no outputs needed | Quick Save | Faster, but captures 0 output files |
| Session might die soon, outputs exist | Run the dataset-publish cell (`save_outputs.py`) | Publishes to Kaggle dataset immediately, no re-run |
| Checking if a version has outputs | Open version → Output tab → count files | Quick Save versions show 0 files. Commits show all files. |

## The trap

The notebook's right-panel Output listing shows **live session files**. It looks saved. It is not.
When the session dies (~20 min idle), those files are gone unless a **completed commit** captured them.

## Checklist after every chunk

- [ ] Verify cell shows "frames on disk: 250 (expect 250)"
- [ ] Zip cell created the zip (note bytes + sha256)
- [ ] Dataset-publish cell ran successfully (saves to Kaggle dataset NOW)
- [ ] **Save & Run All** → wait for "Successful" (not "Running...")
- [ ] Open the new version's Output tab → confirm zip is listed
- [ ] Only then consider the chunk safe

## If a session died before saving

The outputs are gone. There is no recovery. Re-render the chunk.
This is why the dataset-publish cell exists — it saves outputs DURING the run,
so a dead session loses at most one chunk's progress, not all of it.
