# Flamenco — Blender's own render queue (pull + configure)

**Why:** jobs split into frame-chunks; a dead worker's chunk **retries on another worker**. Daemon restarts stop killing our renders — they just re-queue chunks. This is Blender Studio's own production tool (OSS).

**Upstream:** https://flamenco.blender.org — Manager + Worker are single Go binaries, no DB, no K8s.

## Step 1 — Pull the binaries

```bash
mkdir -p ~/workspace/tools/flamenco && cd ~/workspace/tools/flamenco
# Get the latest release for linux-amd64:
# https://flamenco.blender.org/downloads/  (check for the newest version)
# NOTE 2026-10-18: download the tarball via a browser from the official
# downloads page — do NOT guess versioned URLs (a guessed v3.7 path 404'd).
# Place the tarball in this dir, then:
tar -xzf flamenco-*-linux-amd64.tar.gz
ls flamenco-manager flamenco-worker
```

## Step 2 — Run the manager (on our VM)

```bash
cd ~/workspace/tools/flamenco
./flamenco-manager  # first run opens the Setup Assistant (web UI)
```

- Point it at shared storage both manager and workers can see (for us: a dir under ~/workspace/).
- Point it at our Blender: `~/workspace/tools/blender/blender-4.0.2-linux-x64/blender`.
- The manager serves a web dashboard (default :8080) with the job queue.

Keep it alive across daemon restarts: run under a supervisor loop or cron `@reboot`.

## Step 3 — Run a worker (same VM to start; more later)

```bash
cd ~/workspace/tools/flamenco
./flamenco-worker --manager http://localhost:8080 --register
```

The worker polls for chunks, runs Blender headless per chunk, reports progress. Failed chunks retry; after 3 failures on one job the worker is blocklisted for that job.

## Step 4 — Add cloud GPU workers (when Lightning AI / Kaggle / Colab are up)

Any machine that can reach the manager joins the farm:

1. On the cloud box: install the same Flamenco worker binary + same Blender version.
2. Our VM isn't publicly reachable — use the **existing Tailscale network** (tailscale connector is set up) so cloud workers dial the manager over the private net.
3. `./flamenco-worker --manager http://<tailscale-ip>:8080 --register`

This is how we turn every free GPU we get (Lightning T4, Kaggle 2×T4, Colab T4) into farm workers instead of one-off notebooks.

## Step 5 — Submit from cj-render.py

```bash
python3 production/pipeline/compute/cj-render.py \
  --blend 3d-assets/living-room/scene.blend --frames 1-1320 \
  --out renders/walkthrough --target flamenco --chunk 60
```

Or submit from Blender directly: install the Flamenco add-on (link in the manager's web UI top-right) → Output Properties → Flamenco panel.

## Notes

- Chunk size 60 ≈ a few minutes per chunk on CPU — small enough that a kill wastes little, big enough that scheduling overhead is trivial.
- Blender Studio's cloud reference (GPU droplets + spot instances): https://projects.blender.org/studio/flamenco-orchestra — useful when we outgrow free tiers.
- `cj-render.py --target flamenco` posts to `/api/v3/jobs`; if the pulled Flamenco version uses a different API version, update the endpoint in `cj-render.py` (it's marked with a NOTE).
