# Video Pipeline Automation

**Built 2026-10-16.** The owner said: *"We need to get that more automated and autonomous so I don't have to manually kick shit off all the time."*

No more manually advancing render chunks. No more babysitting Kaggle sessions. The queue handles it.

---

## Problem 1: Pantera render needed manual chunk advancement (FIXED)

**Before:** The notebook rendered 250 frames, stopped, waited for a human to change `CHUNK=N` and hit Run All. A 1500-frame render took 2 days of manual babysitting.

**After:** `pantera_kaggle_render_v3.ipynb` — one "Run All" renders ALL chunks sequentially.

### What changed (v2 → v3)

| v2 | v3 |
|----|----|
| `CHUNK = 0` (manual) | `CHUNKS_TO_RUN = "all"` / `"remaining"` / `[3,4,5]` |
| Render → verify → zip for ONE chunk | Loop: render → verify → zip for EACH chunk |
| No resume | `"remaining"` mode skips chunks with existing verified zips |
| Blender re-downloaded if session restarts | Cached check (skips download if present) |

### Files
- Generator: `~/workspace/kaggle-pantera-render/gen_notebook_v3.py`
- Notebook: `~/workspace/kaggle-pantera-render/pantera_kaggle_render_v3.ipynb`
- Same optimization stack as v2 (OptiX, adaptive sampling, persistent data, 1280x720 @ 32spp)

### Usage
1. Upload to Kaggle, set GPU T4 x2 + Internet ON
2. Set `CHUNKS_TO_RUN` (default `"all"`)
3. Run All. Walk away.

Expected: ~15-25 min/chunk, 6 chunks ≈ 2-3h in one session.

---

## Problem 2: Kaggle GPU queue (FIXED)

**Before:** One GPU session at a time. When Task A finished, Task B sat waiting for a human to notice and start it. The ToonCrafter and Viggle videos never ran overnight because nobody kicked them off.

**After:** `kaggle_queue.py` — autonomous GPU queue manager.

### How it works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Queue file  │────▶│ kaggle_queue │────▶│ Kaggle API  │
│ (JSON)      │     │ .py tick     │     │ (batch run) │
└─────────────┘     └──────────────┘     └─────────────┘
       ▲                   │                    │
       │                   ▼                    ▼
       │            ┌──────────────┐     ┌─────────────┐
       └────────────│ Download     │◀────│ Poll status │
                    │ outputs      │     │ every tick  │
                    └──────────────┘     └─────────────┘
```

- **Batch kernels, not interactive sessions.** `kaggle kernels push` triggers a server-side run. No browser needed. Ever.
- **Timer runs every 15 min** via systemd (`kaggle-queue.timer`).
- Each tick: check running jobs → download outputs on completion → start next pending job if GPU free.
- **GPU quota exhaustion** handled gracefully (waits, retries next tick).
- **Hold mode**: `kaggle_queue.py hold "reason"` pauses new starts (e.g. when an interactive session is using the GPU). Monitoring continues.

### Commands

```bash
# One queue pass (timer calls this)
kaggle_queue.py tick

# Show queue state
kaggle_queue.py status

# Add a job
kaggle_queue.py add --notebook PATH --title TITLE \
    --datasets "user/dataset-slug" \
    --pre-copy "dataset/file.mp4:/kaggle/working/input.mp4" \
    --outputs "output.mp4" \
    --output-dir /path/to/save/

# Pause / resume
kaggle_queue.py hold "reason"
kaggle_queue.py release

# Retry failed, clear done
kaggle_queue.py retry JOB_ID
kaggle_queue.py clear-done
```

### Current queue (2026-10-16)

| Job | Status | Notes |
|-----|--------|-------|
| Cape Jones ToonCrafter expressions | pending | Queued, starts when GPU free |
| Cape Jones Viggle body replacement | pending | Queued after ToonCrafter, auto-copies inputs from dataset |

Queue is currently on **HOLD** because the Pantera interactive session is rendering chunks 3-5. Release the hold when Pantera finishes: `kaggle_queue.py release`.

### Files
- Script: `~/workspace/tools/kaggle-queue/kaggle_queue.py`
- Queue: `~/workspace/agent-ops/kaggle-queue.json`
- Log: `~/workspace/agent-ops/kaggle-queue.log`
- Timer: `/etc/systemd/system/kaggle-queue.{service,timer}`

---

## Problem 3: Videos should finish overnight (FIXED)

Same queue system. ToonCrafter → Viggle → auto-download → done. No human clicks.

The timer runs 24/7. When the GPU frees up at 3am, the next job starts at 3:15am. Outputs download automatically. The owner wakes up to finished videos.

---

## Design decisions

1. **Batch > interactive.** Interactive sessions need a browser and a human. Batch kernels run server-side via API. For automation, batch always wins.
2. **Queue file is the source of truth.** JSON on disk, not in memory. Survives restarts.
3. **Idempotent ticks.** Running `tick` twice doesn't double-start jobs. Status checks are read-only until state changes.
4. **Hold, don't kill.** When something else needs the GPU, hold the queue — don't cancel jobs.
5. **Pre-cells for setup.** Jobs that need input files get an injected setup cell (e.g. copy from `/kaggle/input/` dataset to `/kaggle/working/`). The notebook itself doesn't change.

---

## Future improvements

- [ ] Telegram/Discord notification on job completion (owner wants to know when videos are done)
- [ ] Auto-release hold when interactive session ends (detect via API)
- [ ] Priority levels (urgent jobs jump the queue)
- [ ] Retry with backoff on transient Kaggle API errors
- [ ] GPU quota tracking (warn when weekly quota is low)
