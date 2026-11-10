# Lightning AI Studio — signup + render bootstrap

**Why:** best new free GPU wire-up (2026). ~15 credits/mo ≈ 22 T4-hours, up to ~80 free GPU hours after phone verification, 5 credits on signup (+25 with card — card NOT required). Persistent disk (50–100GB) — unlike Colab/Kaggle, your setup survives restarts. T4 / L4 / A10G / L40S available. No credit card for the base free tier.

## Step 1 — Owner signs up (2 minutes, needs HIS phone)

1. Go to **lightning.ai** → Sign up (Google sign-in is fine).
2. **Verify phone number** — this unlocks the GPU hours (up to ~80 free).
3. Skip the card — the free tier works without it.

> Status 2026-10-18: signup OPEN, waiting on owner. This is one of the two open signup items.

## Step 2 — Create a Studio (agent or owner)

1. New Studio → choose **GPU: T4** (cheapest per credit; L4/A10G if T4 is busy).
2. Free-plan Studios restart every 4 hours — storage persists, so this is fine for chunked renders.
3. Open the VS Code-style IDE in the browser.

## Step 3 — Bootstrap for Cape Jones renders (run once per Studio)

```bash
# Blender 4.x (use the version the scene needs)
wget -q https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz
tar -xf blender-4.0.2-linux-x64.tar.xz

# Pull the scene (sparse — we only need the assets for the job)
git clone --filter=blob:none --sparse https://github.com/mhvnsnt/cape-jones.git
cd cape-jones && git sparse-checkout set 3d-assets production

# Grab the render queue CLI
cp production/pipeline/compute/cj-render.py ~/work/ 2>/dev/null || true
```

## Step 4 — Render (resume-safe)

```bash
python3 ~/work/cj-render.py \
  --blend 3d-assets/living-room/scene.blend \
  --frames 1-1320 --out ~/work/renders/walkthrough \
  --target local --samples 24 --res 960x540
# If the Studio restarts mid-render: re-run the SAME command. Done frames skip.
```

## Step 5 — Get frames back

Zip the output dir and download via the Studio's file browser, or push to a Kaggle dataset / GitHub release from the Studio terminal.

## Credit math

- T4 ≈ $0.68/hr → 15 credits ≈ 22 T4-hours/month.
- Our 1320-frame walkthrough ≈ ~3h on T4 → ~2 credits. One month's free credits cover ~7 walkthroughs.
- A10G ($1.80/hr) ≈ 8 hrs/month on free credits — use only when T4 queue is long.
