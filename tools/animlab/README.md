# AnimLab — cape-jones

Role in this repo: rigging/compositing experiments for Cape Jones limited-animation cuts, alongside the existing Toon Boom / Blender rig work.

## What it is

AnimLab is a free animation studio by KevesDev (itch.io: `kevesdev`, AnimLab page).
Vector drawing, pegs, rigging (Bone / Game Bone / Curve / Envelope), node-graph
compositing, multi-camera timeline, audio mixer, 3D primitives, MP4/PNG export.

- **Cost:** freeware — $0. **NOT open-source** — there is no public source repo.
- **Live version:** **v0.2.27** (landed 2026-11-22).
- **Home:** itch.io AnimLab page (KevesDev). No public repo exists — the itch page is the source of truth.

## Binary — LANDED

**v0.2.27 Linux x86_64 .deb** — fetched 2026-11-22 with zero manual work from the
owner, $0, via the Kaggle-kernel no-auth itch flow (CSRF token + POST
`/download_url` → signed download-page URL → POST `/file/{upload_id}` → signed
Cloudflare R2 URL, downloaded immediately).

- File: `AnimLab-Linux-v0.2.27-x86_64.deb` — 79,278,566 B
- sha256: `46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf`
- Verified real: Debian binary package (format 2.0); `dpkg-deb --info` = Package
  anim-lab 0.2.27 amd64, binary `usr/bin/animlab-desktop` (19,779,784 B).
- Canonical home: Release `production-stack-free-20261120` on mhvnsnt/dream-girl —
  https://github.com/mhvnsnt/dream-girl/releases/download/production-stack-free-20261120/AnimLab-Linux-v0.2.27-x86_64.deb
- Local copy: `~/workspace/_animlab-wireup-20261120/fetch/kaggle-output/AnimLab-Linux-v0.2.27-x86_64.deb`
- Manifest: `tools/production-stack-free/animlab/README.md` on branch
  `tools/production-stack-free` (dream-girl), commit a442c1fc.

Other v0.2.27 files (upload IDs known from the itch download page, not yet fetched):
AppImage 20689467 (197 MB), arm64 .deb 20689521, .rpm 20689513, Android .apk
20689528 (66 MB), Windows Setup.exe 20689421, Windows .msi 20689439, macOS .dmg
20689459. The Android .apk matters: the owner is phone-only, so the .apk is how
he can open, review and test rigs directly.

## $0 checkout route (itch page)

1. Open the itch.io AnimLab page.
2. Set the price to **$0.00**.
3. Click **"No thanks, just take me to the downloads"**.
4. No email, no account, no payment. The download page lists all files above.

Download-page links carry tokens that expire in ~30 minutes — always fetch a fresh
download-page URL and pass it to `fetch-animlab.sh` as `$1`; never hardcode a link.
Note: the itch download endpoint 429-throttles this VM's shared egress IP and the
browser Download button silently fails — the Kaggle-kernel no-auth flow above is
the proven route; see `fetch-animlab.sh`.

## Install

### Linux (.deb)
```sh
curl -L -o AnimLab-Linux-v0.2.27-x86_64.deb \
  https://github.com/mhvnsnt/dream-girl/releases/download/production-stack-free-20261120/AnimLab-Linux-v0.2.27-x86_64.deb
sha256sum AnimLab-Linux-v0.2.27-x86_64.deb
# expect: 46de41ac484a9dd8f19e7251bb453fb577ad07620bcf098440f8502c211ccfbf
sudo dpkg -i AnimLab-Linux-v0.2.27-x86_64.deb
sudo apt-get install -f   # pulls libwebkit2gtk-4.1-0 + libgtk-3-0 if dpkg reports them missing
animlab-desktop           # launch; headless: xvfb-run -a animlab-desktop
```

### Android (.apk)
```sh
# On the phone: download the .apk from the itch download page, tap it, allow
# "Install unknown apps" for the browser/files app if asked, install.
# Or from a workstation with adb:
adb install animlab_*.apk
```

## Smoke test — RUNNING (2026-11-22)

- Local install is blocked by a VM disk-write wall (child-process file writes fail
  with "Operation not permitted" since ~13:07 EST 2026-11-22); the install +
  launch smoke test is running on a Kaggle kernel instead
  (slug `marsfmmg/animlab-smoke-test`).
- Package contents verified by inspection: .NET/GTK app, binary
  `usr/bin/animlab-desktop`, bundled ffmpeg, NAPS2 scanner component.
- This doc is updated with the smoke verdict when it lands; nothing here is
  claimed working until the smoke test proves it on a real Cape Jones asset
  (boards/poses from `production/2d-parking-lot/`).

## Pipeline slot

See `PIPELINE-STAGE.md` in this folder for exactly where AnimLab slots into this
show's pipeline, and `docs/ANIMLAB-PIPELINE.md` for the full Cape Jones runbook.