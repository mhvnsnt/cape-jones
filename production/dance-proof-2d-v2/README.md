# Cape Jones dance proof — 2D v2

**Status: LABELED FALLBACK delivered; the Wan/VACE render is staged but
blocked at Kaggle authentication (see "VACE status" — the unblock is one
browser step, spelled out there).** Nothing in this PR is the VACE product,
and nothing here calls itself that.

Deliverables (in `~/workspace/your_files/cape-jones-dance-proof/`):
- `cj-dance-proof-2d-v2-fallback.mp4` — 1920x1080, 24 fps, 75.79 s, the
  cutout-guide composite (this folder's `assemble_v2.py --fallback`),
  upscaled from the 832x480 guide clips.
- `cj-dance-proof-2d-v2-sheet.png` — one frame per lighting state.
- Audio: `song/song-full-v2-jp.mp3` (the song lane's fixed Japanese mix,
  PR #268), full length; the 7-state lighting cycle is stretched across
  the song (about 10.8 s per state) instead of looping the 21 s v1 cycle.

## Character source (owner correction #5) — the 01 turnaround is banned

v1 was extracted from `characters/sheets/01-tpose-turnaround.jpg`, the 3D
rig's T-pose turnaround; its cape splits became v1's cape holes. Every
sheet was viewed for this build. Verdicts:

- `characters/design-sheet.png` — drawn 2D production art (vintage Space
  Ghost cel art + model pages, assembled as the design donor sheet). Its
  hero figure wears Space Ghost's colours, so it is a design reference,
  not the Cape Jones likeness source.
- `characters/sheets/04-action-flight-vfx-reference.jpg` — **drawn 2D**,
  full Cape Jones poses. The standing "HOVERING" figure is the character
  source for the guide puppet (`extract_figure2.py`).
- `characters/sheets/07-character-parts-expressions.jpg` — **drawn 2D**
  parts (heads, hands, capes, legs). Source of the VACE head reference.
- `characters/sheets/08-body-parts-limbs-capes.jpg` — **drawn 2D** ink
  model sheet (body angles, solid one-piece capes, legs/stances).
- `characters/sheets/09-hero-shot-black.png` — **drawn 2D** full-body
  hero; used as a VACE likeness reference.
- `characters/sheets/10-hero-in-space.jpg` — the same drawn figure as 09
  composited over a painted space background; the character is drawn art.
- `characters/sheets/01-tpose-turnaround.jpg` — the 3D rig's turnaround.
  **Banned as an animation/likeness source by owner ruling; not used
  anywhere in this build.**

The result reads obviously 2D next to the 3D version: a flat drawn
character with bold outlines, no modelling, no shading rig.

## How the picture was fixed

- **Cape is one solid piece.** The drawn cape has no 3D splits. Layer
  ownership is exclusive (head > torso > arms > legs geometrically, cape
  takes the dark/purple pixels no part claimed, limb layers keep only
  components touching the joint core, sheet-coloured see-through pixels
  belong to no part), and every posed drawing gets a hole-fill underlay
  from its own dilated silhouette in cape-dark, so no sky shows through
  the body. Zoom-checked at the owner's named spots (both shoulders,
  cape hem, between the legs) on the step and twist poses: no through-
  hole, no detached shard, no hem slivers, no between-legs slit in the
  cape. (v1's right-shoulder sky hole is gone.)
- **The legs work.** The dance is a 48-frame (2 s) loop of 10 key poses
  with eased in-betweens every frame: step left/right with weight dips, a
  twist with cape swing and head look-off, a ta-da hop, a landing crouch,
  and a two-step shuffle. Measured with PR #269's section-5 method on the
  day-section loop of the delivered fallback: **foot-band travel 21.0% of
  body width, torso-band travel 15.9%, ratio 1.32** (spec: ratio >= 0.5,
  torso >= ~10%). v1 measured foot 4.0% / torso 16.7% / ratio 0.24.
- **Backgrounds are PAINTED HERE — labeled honestly.** Searched first:
  cape-jones `docs/environments/` holds design docs only, no plates;
  `mystery-coast-ghosted`'s Scooby-Doo model pack holds 16 real painted
  production plates, but all are establishing/interior compositions (no
  character-scale yard stage) and carry WB slates; the cn-gigaleak EPS
  route does not rasterize on this box (15-minute cap respected, per the
  brief). So the plates in `render_v2.py` are painted in code with
  texture, shading, strata, and layered far/mid/near/foreground depth per
  `docs/environments/MIXED-MEDIA-GUIDE.md`. The mesa plate is still the
  flattest of the three and is named as a shortfall below.

## VACE status — exactly where it stopped

Built and staged, in this PR under `production/assets/dance-proof-v2/`:
7 driving clips + masks (832x480, 49 frames, one dance loop each,
loop-closed), 3 drawn-art references, `batch.json` (30 steps, cfg 5 —
the quality/baseline class from the owner's speed-test verdict, not the
rejected fast setup), and the kernel (`kaggle/cj_dance_vace_kernel.py`,
Wan2.1-VACE-1.3B, text encoder split to the second GPU, per-section
likeness metrics and a manifest that never writes a clip it did not
render).

The run did not happen. Kaggle's installed CLI (2.2.4) dropped legacy
API-key auth; the accel lane's venv CLI (kaggle 1.6.14, rebuilt at
`~/venvs/kaggle`) was made to reach Kaggle from this box — that took
`KAGGLE_PROXY` plus `KAGGLE_SSL_CA_CERT=/etc/ssl/certs/ca-certificates.crt`
(the egress proxy's CA is only in the system bundle) with
`KAGGLE_USERNAME`/`KAGGLE_KEY` passed as env so the config-file read
doesn't discard the proxy — and the API then answered **401 Unauthorized**
on both dataset create and kernel push: the stored legacy key itself is
dead. Unblock (browser, owner's blanket-approved Google sign-in):
generate a new Kaggle API token at kaggle.com/settings/api (or run
`kaggle auth login` in the 2.2.4 CLI), then:

```
~/venvs/kaggle/bin/kaggle datasets create -p <dataset folder>   # env recipe above
~/venvs/kaggle/bin/kaggle kernels push -p <kernel folder>
~/venvs/kaggle/bin/kaggle kernels status marsfmmg/cj-dance-vace
~/venvs/kaggle/bin/kaggle kernels output marsfmmg/cj-dance-vace -p vace_out
python3 assemble_v2.py        # tiles the VACE clips to the song, muxes, measures
```

A Colab run of the same kernel (the PR #108 pattern) is the other route.
Note the accel README's earlier warning: this account hit its 30 h
weekly GPU quota on 2026-10-29; quota state at unblock time is unknown.

## Known shortfalls of the fallback (honest)

- It is a cutout guide, not drawn animation: at zoom, a raised arm's
  shoulder bridge stretches, and the cape's shoulder drape can read as a
  dark block behind a raised arm. That is the class VACE exists to
  replace; the fallback does not hide it, it is labeled for it.
- No blink/settle secondary layer (PR #269 gap G5); holds are carried by
  the pose changes and the cape's offset swing only.
- Mesa plate still reads flatter than the yard/evening plates.
- The guide's feet come from a hovering pose (pointed toes); steps read
  through travel and weight dips rather than flat-foot plants.

## Files

- `production/dance-proof-2d-v2/` — this README + all build scripts
  (`extract_figure2.py`, `build_dance_v2.py` dance keys/sampler,
  `build_dance_v3.py` drawn-art puppet, `render_v2.py` painted plates,
  `render_v3.py` song-length render + VACE batch, `assemble_v2.py`
  assembly + spec measurement + zoom checks) + the Kaggle kernel and
  batch metadata.
- `production/assets/dance-proof-v2/` — the VACE batch: 7 driving clips,
  7 masks, 3 drawn-art reference images.
