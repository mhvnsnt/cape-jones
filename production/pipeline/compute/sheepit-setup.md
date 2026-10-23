# SheepIt — free community render farm (signup + headless client + jobs)

**Why:** the only *ongoing* free render farm. Point economy: you earn ~4× what you contribute. Run the headless client on OUR VM 24/7 earning points on CPU, spend them on community GPU renders. No card, no trial that expires.

**Caveat:** volunteers see thumbnails of frames they render — no NDA-sensitive or unreleased-commercial work. Our living-room scenes are fine.

## Step 1 — Owner creates account (2 minutes)

1. Go to **sheepit-renderfarm.com** → sign up.
2. New accounts get **starter points** — enough for a first test project without contributing first.

> Status 2026-10-18: signup OPEN, waiting on owner. One of the two open signup items.

## Step 2 — Run the headless client on our VM (earn points 24/7)

```bash
mkdir -p ~/workspace/tools/sheepit && cd ~/workspace/tools/sheepit
# latest client: https://www.sheepit-renderfarm.com/client.php (check for new versions)
wget -q https://www.sheepit-renderfarm.com/media/applet/client-latest.php -O sheepit-client.jar
# run headless, CPU, low priority — earns points whenever the VM is idle
java -jar sheepit-client.jar -login <user> -password <pass> -compute-method CPU \
  -cores 1 -priority 10 -cache-dir ~/workspace/tools/sheepit/cache
```

- Use **1 core** so our agent work isn't starved; the VM is idle most of the night.
- Points accrue per frame rendered for others (~4× spend ratio).
- Keep the client in a supervised loop (cron `@reboot` or a watchdog) — it must survive daemon restarts to earn steadily.

## Step 3 — Submit a job

1. **Package the .blend:** all textures packed (File → External Data → Pack Resources) or shipped alongside; use a supported Blender version (SheepIt tracks Blender releases — check their supported-versions list before submitting).
2. Upload at sheepit-renderfarm.com → "Add project". Set frame range, samples, resolution.
3. Cost is deducted in points based on scene complexity × frames × resolution. Our 1320-frame walkthrough at 960×540/24spp is a medium job — well within a few weeks of 1-core earning + starter points.
4. Download finished frames from the project page.

## Step 4 — Job packaging checklist (for our scenes)

- [ ] .blend under their size limit (check current limit on the upload page)
- [ ] All textures packed or relative paths intact
- [ ] No custom add-ons the farm doesn't have (bake everything first)
- [ ] Cycles (not EEVEE) for GPU volunteers; either is fine for CPU
- [ ] Test with a 3-frame submission before the full 1320

## Earning math

- 1 frame rendered for others ≈ points for ~4 of our frames.
- Our VM: 2 CPUs, 1 core donated → slow per-frame, but 24/7 = steady trickle.
- Strategy: earn continuously in the background; spend on the big walkthrough renders.
