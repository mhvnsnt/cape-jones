# AI Watermark Removal — LaMa Inpainting Pipeline (Cape Jones)

**Status: PRODUCTION — used for EP01 final (2026-10-21). Owner-approved result.**
This is THE way watermark removal is done on Cape Jones. Never blur boxes, never
black rectangles, never cover-up patches — AI inpainting that rebuilds the
background, or nothing.

## The method (what worked)

1. **Ground truth first.** Work only from the owner's actual source version.
   Version files downstream of our own editing passes contain OUR additions —
   never assume an artifact (e.g. a blur box) is in the owner's source just
   because it is in a v3/v4 file. (Learned the hard way on EP01: the blur box
   we spent days "removing" was one we had added ourselves.)

2. **Detect by glyphs, not by template matching.** Template correlation fails
   whenever the background color changes (LED color grades!). Instead:
   - Build a *glyph mask* from a clean template crop: pixels brighter than a
     Gaussian-blurred copy of the template (left thresh 60, right thresh 40).
   - Per frame, score = fraction of glyph-mask pixels that are watermark-white
     (min(R,G,B) > 170 and max−min < 45).
   - **PRESENT iff glyph_score > 0.55 AND whole-box white fraction < 0.4**
     (the second clause kills false positives like the white suit crossing
     the box — verified: 50s suit frame scores 0.748 glyph but 0.689 white
     fraction and is correctly rejected).
   - See `detect_watermarks.py`. Validated scores: present 0.59–0.95 (right),
     0.82–0.91 (left); absent ≤ 0.35.

3. **Inpaint with LaMa** (big-lama torch.jit model, Kaggle T4 GPU):
   `https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt`
   (205,721,600 bytes). Direct `torch.jit.load` — do NOT use the
   `simple-lama-inpainting` pip package (broken on Kaggle's Python 3.13).
   - Context patch: box + 110px context on all sides, mask = the box only.
   - **Boxes must cover the watermark's soft glow**, not just the glyphs.
     EP01 final boxes (1080×1920 frame):
     - LEFT inpaint `(0,920)-(330,1040)`, detect box `(15,935)` 300×90
     - RIGHT inpaint `(705,1340)-(1075,1460)`, detect box `(720,1355)` 300×90
     - The earlier narrower right box (to x=1030) left a faint pink ghost —
       the glow extends past the glyphs. Widening fixed it completely.
   - **Feather the paste**: 6px alpha ramp on the pasted region's edges so the
     fill fades into the background (owner requirement: "make it actually
     fade into the background... it should do that automatically").
   - Full episode (5009 frames) runs ≈ 12 min on Kaggle T4.
   - Notebook: `cape-jones-wm-lama.ipynb` (generator: `build_notebook.py`).
     It renders 4 test stills FIRST (right 45s, left 89s, clean-corner 10s
     passthrough, magenta 83.1s) — always eyeball them in the output before
     trusting the video.

4. **Verify with your own eyes before delivery** (standing law): freeze the
   known watermark spots (EP01: right 41–64s, 74–90s, 95s, 110s, 137–141.5s,
   151.5–157.5s; left 68–74s, 86.3–92s, 145–151s), the corners, and any
   heavy grade-change moments. A worker's "verified" is a claim, not a fact.

## Known limitation — color changes (owner-noted 2026-10-21)

When the scene's LED color grade shifts hard, a watermark can show through in
individual frames the detector scored below threshold (the glyphs take on the
grade's color and stop reading as "watermark-white"). Good enough for EP01's
release. Improvement paths, in order:
1. Per-scene/per-grade glyph thresholds — score against the *local* expected
   watermark color under the active grade instead of global white.
2. Track detections temporally: the watermark is fixed-position, so a strong
   detection at t−1/t+1 should force inpainting at t even on a weak score.
3. Multi-template masks captured under each major grade (blue/magenta/amber).

## Rebuild recipe that produced the EP01 master (v5)

- `cape-jones-episode-v3.mp4` (1080×1920, pre-blur, owner-verified same edit
  as his upload) = picture base.
- Magenta extension re-applied by lifting the 15 frames 83.0–83.5s from v4
  (where the extension already existed) with the baked blur corner replaced
  by v3's genuine corner, color-matched via a per-channel affine fit from
  the paired frames at 83.1/83.2s (`magenta_fit.py`, `build_v5_source.py`).
  The lift gate was data-driven: only frames where v4's R−G exceeded v3's
  by > 15 were lifted — exactly 15 frames.
- Audio: v3 and v4 measured identical loudness (−20.32 LUFS) — same stream,
  no mux needed.
- LaMa pass on the result → `cape-jones-v5-clean.mp4` (167s master).

## Kaggle operational notes (hard-won)

- `kaggle kernels push` with `dataset_sources` in kernel-metadata.json DID
  propagate for this kernel (v3/v4 runs). If a run ever can't find inputs,
  attach via the browser Input tab and verify before Save & Run All.
- **Never Quick Save** — it captures 0 output files.
- `kaggle kernels output` downloads can sit at 0 bytes for 10+ minutes then
  complete; use `--file-pattern` to skip `big-lama.pt` (197MB, just the model
  the notebook fetched at runtime).
- Check status: `python3 -m kaggle kernels status marsfmmg/cape-jones-wm-v3`

## Files

- `cape-jones-wm-lama.ipynb` — the Kaggle notebook (production run)
- `build_notebook.py` — notebook generator (edit this, rebuild, re-push)
- `detect_watermarks.py` — glyph detection, validated standalone
- `build_v5_source.py` / `magenta_fit.py` — the v5 master rebuild
- `wm_template_left.png` / `wm_template_right.png` — glyph template crops

---

## V6 ADDENDUM — the suit-overlap failure (found by QC scan 2026-10-21, fixed 2026-10-22)

The v5 clean master passed every spot-check and still shipped leftovers: a full-video
QC glyph scan (every 0.5s, both boxes) flagged sustained high scores, and own-eyes
review confirmed the watermark **fully visible wherever it overlaps the white suit**:

- right: ~101.5–103s, ~106.5–108.5s, ~127.5–129.5s, ~135–136s
- left: across his torso through stretches of ~35–57.5s

**Root cause:** the detection rule's white-fraction guard (`frac < 0.4`, added to reject
a supposed suit false positive at 50s) rejected exactly the frames where the watermark
sits on bright costume. That "false positive" was itself a real watermark over the suit.

**The fix (v6, verified):** presence = glyph_score > 0.55, NO white-fraction guard.
An independent relaxed scan of the source mapped 1307 left / 2495 right frames; the v6
run's fill counts matched exactly. Own-eyes re-checks at 102s (cape/suit edge) and 37s
(torso/belt line art) show the watermark gone and the artwork intact.

**Standing rules added:**
1. After ANY removal pass, run the full-video QC glyph scan on the result — spot-checks
   alone missed this. Sustained glyph scores > 0.45 anywhere = inspect with eyes.
2. Never add a guard that can veto detection on bright subjects; the glyph shape is the
   discriminator, not the box's overall brightness.
