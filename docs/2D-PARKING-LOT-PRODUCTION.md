# 2D PURPLE LOT — Production Wiring (2D track)

**Track: 2D** (drawn show — separate from the 3D test-short lane; no 3D files touched)
**Short:** PURPLE LOT — the parking-lot LED remote test short (480 frames @ 24fps = 20s)
**Status:** storyboard 4/7 keys drawn + verified (CJ-PL-01/03/07 missing — see gaps); poses DONE 8/8 + cape study sheet, all own-eyes verified (2026-11-22 ~12:19 EST); Tahoma2D re-pull VERIFIED working end-to-end (see §3); pipeline wired per this doc.
**Canon:** `docs/SHOW-BIBLE.md` (palette locked: suit #FFFFFF, cowl #3E1473, skin #E5B28C, cape #000000; white eyes default, cartoony pupils sometimes; the Cape is the most competent character), `docs/SHOW-PRODUCTION-STATUS.md` (bar: drawn changes on twos at 24fps, Metalocalypse-level, NOT holds/slideshow), `docs/SUPERIOR-TURBINATE-STUDY.md` + `DEEP-STUDY` + `FEELING-STUDY` (packaging/feeling — copy packaging/writing/funnel/cadence, NOT the long holds).

## 1. The pipeline (stage map)

From `~/workspace/_free-anim-stack-20261120/PIPELINE.md` (Draw → Rig/Tween → Interpolate → Composite → Finish → Assembly). Grease Pencil (Blender) stays the rig/animation CORE. New tools are candidates for cleanup / hand-drawn 2D / compositing / rigging experiments — never presented as a core replacement.

| Stage | Tool (version) | Status on this box (verified 2026-11-22) | Job on this short |
|---|---|---|---|
| Draw | Krita 6.0.4 | NOT on disk — not in tools-archive manifest; needs fresh download from krita.org if the lane needs it | Drawing/painting, cleanup |
| Draw | Tahoma2D 1.6.3 | **LIVE + PROVEN 2026-11-22 ~12:19 EST** — re-pulled tarball (328,382,822 B, sha256 `6ca474922bfb86cf601b5c0e484461a5b7122000ced96a107a413abbb9cf1561`) at `~/workspace/tools/tahoma2d/`; `tcomposer -version` → "Tahoma2D v1.6.3"; Ozzie re-render proof (12 drawings on twos, 1280x1280) composited in 1.39s, exit 0, frame own-eyes PASS (sha256 `e346c20c5ad054ce3f9aaf075d29493fbb34e04613c52c7b46bea1b16649b3fe`). Setup fixes recorded in §3 — read them before running it. | Hand-drawn 2D frames + compositing + render via `tcomposer` (ABSOLUTE paths only — relative paths hang forever) |
| Draw | Pencil2D 0.7.2 | On dream-girl Release `production-stack-free-20261120` (AppImage 60,471,800 B, sha verified) — download on demand | Lightweight hand-drawn animation |
| Rig | Blender Grease Pencil v3 (5.2.4) | LIVE — Blender 5.2.4 on disk (`~/workspace/_cape-jones-parking-lot-test/blender/blender-5.2.4-linux-x64/`) | THE CORE — Harmony cutout method lives here |
| Rig | COA Tools 2 (Aodaruma fork v2.3.0) | LIVE — installed in Blender 5.2 user extensions (`~/.config/blender/5.2/extensions/user_default/coa_tools2`); P9 PASS (real sprite import + automesh + bind + pose + render), P17 lizznull mesh-deform PASS | Cutout puppet rig: layered art → auto-mesh → bone rigs + IK, sprite swapping (mouth/eye libraries) |
| Rig | Rigby2D 0.5.1 | On dream-girl Release (AppImage 96,979,448 B, sha OK vs published) — download on demand | Skeletal/mesh/IK/physics editor (live Moho/Spine cover) |
| Rig | AniCraft 0.2.1 | On dream-girl Release (AppImage 19,024,376 B, sha OK vs published) — download on demand | Clean-room Adobe Animate (XFL/FLA/SWF-compatible); FLA-compat test vs a real .fla still owed |
| Rig | SakugaGP (7 add-ons), Grease Pencil Tools 2.3.1 | LIVE — installed in Blender 5.2 user extensions (`grease_pencil_tools` present; SakugaGP kit per catalog P11 QUEUED) | Grease Pencil workflow kit |
| Secondary motion | Wiggle 2 RTX Edition 2.4.0 | LIVE — installed (`wiggle_2` in user extensions); P12 QUEUED, not yet proven | Spring physics on pose bones (cape lag/overshoot/settle) — PROVE on a cape test before relying on it |
| Secondary motion | Wiggle Bones 1.1.2, Jiggle Physics 4.5.3 | LIVE — installed (`wiggle_bones`, `jiggle_physics`); P15 PASS (register-only) | Alternatives if Wiggle 2 RTX fails its proof |
| Manga look | Senga Sketch 1.0.0 | LIVE — installed (`senga_sketch`); P16 QUEUED | Pen-and-ink manga (hatching, screentone) — B&W manga intro frames |
| Manga look | MochiToon 0.3.3, Painterly 2.5D 1.1.1, KiraPaint 0.2.0 | LIVE — installed (`mochitoon`, `painterly_25d`, `kirapaint`); P6a/P6b/P16 QUEUED | NPR looks (toon / hand-painted / sparkly) |
| Lip sync | Rhubarb Lip Sync 1.14.0 (CLI) | Standalone 1.14.0 NOT on disk in searched locations; **bundled 1.13.0 VERIFIED working** with the Tahoma2D re-pull (`~/workspace/tools/tahoma2d/Tahoma2D/rhubarb/rhubarb --version` → "Rhubarb Lip Sync version 1.13.0") | Audio → timed mouth-shape cues — ONLY on the owner's recorded voice, never synthesized |
| Lip sync | Rhubarb Lipsync NG 1.8.2 | LIVE — installed (`rhubarb_lipsync` in user extensions); P10 PASS | Blender add-on wrapping Rhubarb; bakes mouth keys |
| Composite | Natron 2.5.0 | NOT on disk — not in tools-archive manifest; needs fresh download if the lane needs it | Node compositing |
| Finish | Kdenlive 26.08.3, Olive 0.2.0-nightly, ffmpeg 8.1.2 | Kdenlive + Olive on dream-girl Release (AppImages, sha verified) — download on demand; ffmpeg on box (`/usr/bin/ffmpeg`) | Edit + assembly + encode |
| Interpolate | GP Tween 2.4.0 | LIVE — installed (`gp_tween`); **OWNER-GATED** | Interpolates GP strokes between keys — output is NEVER shipped as finished inbetweens until the owner eye-judges a real test frame by frame (owner law: tweening, NOT ghostly AI interpolation) |
| Interpolate | RIFE | DOCS-ONLY — owner law governs; use only where directed | Frame interpolation — same gate as GP Tween |
| Experiment only | AnimLab v0.2.27 | DOCS-ONLY — binary fetch FAILED 2026-11-22 ~07:03–07:10 EST: browser reached the itch download page signed in as Mhvnsnt, but the Download button did nothing (itch download endpoint silently blocked; .deb + AppImage both failed, Alternate Download Mode too, 3-min retry also failed). Current release v0.2.27 (Nov 21, 2026; Linux x86_64 .deb 75 MB, AppImage 197 MB). Download page left open in the browser tab for the owner to tap himself, or he can grab the .deb on his phone and drop it in Drive. | Rigging/compositing EXPERIMENT candidate only — Grease Pencil stays core |
| Video-gen | Wan 2.1 14B I2V (ComfyUI, PR #135 merged 2026-11-09) | Use only where the owner directs | Real-drawn bar + no-interpolation law govern |

## 2. How the short runs through it

1. **Boards (done, 4/7):** `production/2d-parking-lot/boards/` — CJ-PL-02/04/05/06 drawn + own-eyes verified; CJ-PL-01/03/07 NOT drawn (media image tool declined those three on its own safety check; not retried, not routed around — needs a different drawing route or the owner's call). Title: PURPLE LOT. Fan does not appear (Jones + Cape alone).
2. **Poses (done, 8/8 + study sheet):** `production/2d-parking-lot/poses/` — 6 scene poses (idle / raise / press / shift / lower / nod) + 2 cape-as-a-character poses (billow / settle) + the 5-panel cape study sheet the billow was cropped from, all on void-white backgrounds, all own-eyes verified by the lane and re-verified by the coordinator. Continuity notes for the animation pass (not redraw triggers): the remote design varies slightly — gray multi-button remote in pose-02 vs small black remote in pose-03/04/05; the pose-04 remote has a small antenna nub; the cape-02 folded top reads slightly face-like (closed-eye fold) — that fits the cape-as-a-character gag. The pose-05 first pass came back with cartoony pupils and was redrawn and fixed to white eyes.
3. **Rig:** the pose art goes through COA Tools 2 in Blender 5.2.4 — layered pieces → auto-mesh → bones + IK → sprite swap (mouth/eye libraries from sheet 05/06). Cape gets Wiggle 2 RTX only after its cape-test proof passes.
4. **Animate:** Grease Pencil, drawn changes on twos at 24fps (12 drawings/sec), on ones for hits/fast action. Every cut >1s needs an exposure note. The held reaction after the punchline line must be DRAWN (pose change, arms down, cape settling, light shifting) — motion in the stillness, never a freeze.
5. **Light shift:** the dynamic colored lighting is the sincere beat — dim sodium orange → broken-streetlight purple (bible §5A/§8, sheet 03 rim-light rules; suit base stays white, tint on rim/glow only).
6. **Render:** Tahoma2D `tcomposer` (absolute paths only) or Blender Grease Pencil render; composite in Natron where needed; assemble in Kdenlive; encode with ffmpeg.
7. **Voice:** "ah, that's better" is a GAP for the owner's recording. No synthesized voice ever. Rhubarb runs only on his recorded line when it lands.

## 3. Known gaps / recovery notes (honest)

- **Tahoma2D re-pull — VERIFIED 2026-11-22 ~12:19 EST.** The re-pulled 1.6.3 renders end-to-end (Ozzie re-render proof, 1.39s, own-eyes PASS). Five setup fixes were needed on the fresh install — a future lane must do all of them or tcomposer fails silently:
  1. **libOpenGL.so.0:** missing on the system (only libGL.so.1). Fix applied: `libopengl0_1.7.0-1build1_amd64.deb` (Ubuntu 24.04 noble, archive.ubuntu.com) extracted with `dpkg-deb -x` to `~/workspace/tools/tahoma2d/syslibs/usr/lib/x86_64-linux-gnu/`; run with `LD_LIBRARY_PATH` pointed there. (Do not apt-install; apt is broken on this VM.)
  2. **xvfb-run required:** `xvfb-run -a` — the Qt xcb plugin needs a display; `QT_QPA_PLATFORM=offscreen` does NOT work (offscreen plugin is not in this build).
  3. **Stale SystemVar.ini:** `~/.config/Tahoma2D/SystemVar.ini` held `TAHOMA2DROOT` pointing at the dead Nov 20 smoke-test install (`_tool-smoke-tests-20261120/lane-b/...`) — tcomposer aborted on it. Fixed to `/home/hatch/workspace/tools/tahoma2d/Tahoma2D/tahomastuff`. The env var alone does NOT override the ini.
  4. **Fresh installs have NO projects** → "Couldn't find the project" (exit 254). Fix (format from Tahoma2D source `toonz/sources/toonzlib/tproject.cpp`): created `tahomastuff/projects/dreamgirl/tahomaproject.xml` (TOStream, NO `<?xml ?>` header; `<project><version>70 1</version><folders>` with scenes/drawings/outputs/inputs/extras) + `dreamgirl/scenes/scenes.xml` (`<parentProject type="projectFolder">".."</parentProject>` — the `..` MUST be double-quoted; bare dots are not valid TOStream bare tokens and fail silently). Proof scene at `dreamgirl/scenes/ozzie-retest.tnz` (built by `~/workspace/_tahoma2d-wirein-20261112/build_scene.py`); levels in `dreamgirl/drawings/`.
  5. **Absolute paths** for scene + output still the rule (Nov 12). Working render command: `LD_LIBRARY_PATH=~/workspace/tools/tahoma2d/syslibs/usr/lib/x86_64-linux-gnu xvfb-run -a ./Tahoma2D/squashfs-root/usr/bin/tcomposer <abs .tnz> -o <abs out.png> -range 1 1 -step 1` (from `~/workspace/tools/tahoma2d/`).
- **Krita / Natron:** not in the tools-archive release manifest (checked 2026-11-22 — no entries). Fresh downloads from their official sites if needed; do not claim them as on-disk until pulled + verified.
- **Rhubarb standalone 1.14.0:** binary not found on disk in searched locations; bundled 1.13.0 verified working with the re-pull. Rhubarb Lipsync NG add-on is live in Blender.
- **GP Tween / RIFE:** owner-gated, never shipped as finished inbetweens without the owner's frame-by-frame eye-judgment.
- **AnimLab:** docs-only; browser fetch failed 2026-11-22 (see table). Experiment candidate only.
- **Continuity note:** the drawn boards show parked cars in the background; the 3D wide proof shows an empty lot. If the lot must read empty, backgrounds get cleaned in the animation pass — character keys are unaffected. Remote design varies slightly across poses (see §2 step 2) — lock the small black remote in the animation pass.

## 4. Sources

- Stage map: `~/workspace/_free-anim-stack-20261120/PIPELINE.md` · Toolkit: `~/workspace/free-2d-animation-pipeline-toolkit.md` · COA catalog + proofs: `~/workspace/_anime-rig-pullin-20261114/PULLIN-CATALOG.md` (+ `proofs/`) · Tahoma2D wire-in: `~/workspace/_tahoma2d-wirein-20261112/CHECKPOINT.md` (+ `test-project/`, `build_scene.py`, `otmcp-tnz.py`, `otmcp-tnztree.py`) · Dream-girl Release `production-stack-free-20261120` (Rigby2D / AniCraft / Pencil2D / Kdenlive / Olive AppImages, sha-verified).
- Lane workdir: `~/workspace/_cape-jones-parking-lot-2d/` (CHECKPOINT.md authoritative).
