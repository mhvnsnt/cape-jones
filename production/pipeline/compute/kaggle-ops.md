# Kaggle ops — push discipline (read before every push)

**Background:** v8–v11 of the living-room walkthrough kernel were cancelled within minutes (CANCEL_ACKNOWLEDGED, zero output, quota untouched at 17min/6h). v7 pushed normally ran fine on 2×T4. No public root cause found (2026-10-18). Working theory: anti-abuse/session limiter tripped by rapid version pushes.

## Rules

1. **Space pushes ≥30 minutes apart.** Never push v+1 while v is still initializing/queued.
2. **One active kernel per task.** `kaggle kernels status <id>` — if the old one is still alive, cancel it explicitly before pushing the new one.
3. **Use the CLI, not the web UI.** `kaggle kernels push -p <payload-dir>` — same path every time, scriptable, logged.
4. **Payloads come from `cj-render.py --target kaggle`.** They are resume-safe: the kernel skips frames already in the output.
5. **Checkpoint to a dataset.** Every kernel uploads rendered frames to an output dataset incrementally (not just at the end). A cancelled run loses nothing already checkpointed.
6. **Watch the first 5 minutes.** `kaggle kernels status` + `kaggle kernels output --tail`. If it goes CANCEL_ACKNOWLEDGED with no log, STOP pushing — see rule 7.
7. **If cancellations persist >24h:** stop pushing entirely. Switch the job to Lightning AI or SheepIt (`lightning-ai-setup.md`, `sheepit-setup.md`). Retry Kaggle after a cooldown, with a single push, spaced.

## Useful commands

```bash
# push
cd <payload-dir> && kaggle kernels push
# status / log tail
kaggle kernels status marsfmmg/<kernel-slug>
kaggle kernels output marsfmmg/<kernel-slug> --tail
# list what's running (avoid duplicates)
kaggle kernels list --mine --sort-by updated
```

## Quota

~30 GPU-hrs/week on 2×T4, 12h max per run. Check current quota in Kaggle account settings — it floats. Track spend per job in the job's notes.
