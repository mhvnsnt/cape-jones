# Professional 2D Animation Inbetweening — Deep Research

**Date:** 2026-10-15
**Question:** How do professional studios handle inbetweening for hand-drawn animation? Is there production-grade software better than RIFE/ffmpeg for cartoon interpolation?

---

## THE CORE INSIGHT

**All professional auto-inbetweening works on VECTORS, not raster pixels.**

RIFE, ffmpeg minterpolate, DAIN — these all operate on raster pixel data. They try to track motion by looking at pixel patterns. On flat cartoon colors (white suit, purple cape, black background), there are no pixel patterns to track, so they default to blending = ghosting.

Professional tools (Cacani, OpenToonz, Toon Boom Harmony) convert drawings to **vector stroke data** first, then interpolate the **strokes themselves** — moving lines from position A to position B. No pixel blending, no ghosting. This is the fundamental difference.

---

## 1. CACANI — The Professional Standard

**What:** Commercial 2D animation software from Nanyang Technological University (Singapore), developed by Dr. Hock Soon Seah's team.

**How it works (technical):**
- Vector-based drawing system (not raster)
- Auto-inbetweening detects **stroke chains** — connected sequences of line segments that form parts of a character's outline
- Matches stroke chains between keyframe A and keyframe B using correspondence algorithms
- Interpolates each stroke chain independently along animation paths
- Timing adjustable down to individual strokes
- Smart auto-painting: paint one frame, color propagates to inbetweens

**Key features:**
- Automatic inbetween frame generation from key drawings
- Stroke occlusion handling (hides parts behind other shapes)
- Stroke end tapering (natural-looking line ends across frames)
- Multi-layer support
- Exports to After Effects-compatible sequences

**Pricing/Availability:**
- Commercial software (cacani.sg)
- Has been used by Japanese anime studios and Singaporean companies
- No open-source version exists

**Why it doesn't ghost:** It never blends pixels. It moves vector strokes mathematically from one position to another.

**Relevance to Cape Jones:** This is the gold standard. If we vectorize the FlipaClip drawings first, we could theoretically do Cacani-style inbetweening.

---

## 2. OPENTOONZ / TAHOMA2D — What We Already Have

**Vector inbetweening:** OpenToonz documentation confirms: "Automatic creation of inbetween frames is available for **vector shapes**."

**Raster-to-vector converter:** OpenToonz has a built-in bitmap-to-vector conversion tool that:
- Works in both centerline mode (for line art) and outline mode
- Converts black & white AND color art
- Works on **multiple drawings for animations** (batch conversion)
- Can export results as SVG
- Includes bitmap cleanup tools for pre-processing sketches

**We have Tahoma2D** (OpenToonz fork) at `~/workspace/tools/Tahoma2D/` — extracted and ready.

**The workflow this enables:**
1. User draws keyframes on FlipaClip (raster)
2. Import frames into Tahoma2D
3. Convert raster → vector using built-in tool
4. Use vector inbetweening to generate tween frames
5. Export

**Limitation:** Requires GUI interaction. No confirmed headless/batch API for the vectorization + inbetweening pipeline. Needs testing.

---

## 3. TOON BOOM HARMONY — Industry Standard

**How studios use it for inbetweening:**
- **Morphing tools:** Select two vector drawings, Harmony generates inbetweens by morphing one shape into another
- **Rig-based:** Build character rigs with bones/IK, pose at keyframes, Harmony interpolates (CTRL+K)
- **Traditional:** Draw keys, use onion skin, draw breakdowns manually

**Known issues (from professional animators):**
- Morphing creates straight-line motion instead of natural arcs — requires manual correction
- "Pancaking": when flipping poses, the rig flattens unnaturally between frames
- Auto-inbetweens are starting points, not finished frames — always need cleanup

**Key quote from working animator:** "Harmony can make these frames itself! By pressing CTRL K, Harmony can move the rig from the quickest path between two points... Harmony is obviously not a flawless program, so it's bound to make mistakes that need to be corrected later on."

**Pricing:** Commercial, expensive. Not an option for this pipeline.

---

## 4. JAPANESE ANIME PIPELINE (RETAS and Real Workflows)

**How anime actually does inbetweening:**

The pipeline uses distinct roles:
- **Genga (原画):** Key animators draw the important poses
- **Dōga (動画):** Inbetweeners fill in the gaps — **by hand**
- **Shiage (仕上げ):** Digital painters add color

**Software used:** RETAS STYLOS, Toon Boom Harmony, Clip Studio Paint EX, Adobe Animate, Photoshop

**Critical insight:** Anime uses **"limited animation"** — typically 8 or 12 fps, NOT 24fps. They deliberately don't try for smooth motion. Instead they compensate with:
- Dramatic camera movements
- Intense lighting effects
- High-detail backgrounds
- Strong posing and timing

**This means:** The anime industry's answer to "how do we inbetween efficiently" is largely **"we don't — we use fewer frames and make each one count."** The 12fps FlipaClip output is already at anime standard.

**Implication for Cape Jones:** We may not need 24fps at all. 12fps with strong poses IS the anime look.

---

## 5. THE HYBRID APPROACH: Combining Tools

### Can we combine ffmpeg's motion estimation with RIFE's quality?

**ffmpeg motion vectors:**
- ffmpeg can export motion vectors via `-flags2 +export_mvs` with `codecview` filter
- These are **macroblock-level** vectors from video compression (16x16 pixel blocks)
- They show general motion direction but are too coarse for frame interpolation
- Not directly compatible with RIFE's dense optical flow approach

**Verdict:** Not a clean combination. The motion vector formats are incompatible.

### Better hybrid: RIFE + De-ghosting + Scene Awareness

**Proposed pipeline:**
1. **Scene detection:** Split video at hard cuts/black frames (don't interpolate across them)
2. **RIFE interpolation:** Generate inbetween frames within each scene
3. **De-ghosting post-process:** Detect semi-transparent blended regions, snap them toward the nearest sharp keyframe
4. **Selective application:** Only interpolate where motion is detected; hold static frames as-is

This combines the best of each approach without requiring incompatible data formats.

### The Vector Path (Best Long-Term)

**Proposed pipeline:**
1. FlipaClip drawings (raster) → Tahoma2D
2. Raster → Vector conversion (built-in OpenToonz tool)
3. Vector inbetweening (built-in OpenToonz feature)
4. Export as image sequence or video

This is how Cacani and professional studios do it. No ghosting because no pixel blending.

**Needs testing:** Can Tahoma2D do this headlessly? What's the quality of auto-vectorization on FlipaClip line art?

---

## 6. OPEN-SOURCE PROJECTS FOR CARTOON INTERPOLATION

| Project | Approach | Status |
|---------|----------|--------|
| **AnimeInterp** (CVPR21) | Specifically for line drawing inbetweening | Code available, weights gone (Dropbox 404) |
| **FLAVR** | Flow-free, doesn't use optical flow | Code cloned at `~/workspace/tools/flavr/`, not set up |
| **GMFSS Fortuna** | Anime-specific | Working but 15+ min/frame on CPU |
| **ECCV2022-RIFE** | General video | Working, ghosts on flat colors |
| **DAIN** | Depth-aware | Older than RIFE, generally worse |
| **EMA-VFI** | Enhanced motion-aware | RIFE beats it on benchmarks |
| **Timestep-conditioned diffusion** (CMU 2025) | AI learns animation motion | Research project, not production-ready |

**Bottom line:** No open-source tool is specifically designed and trained for cartoon inbetweening with available weights. AnimeInterp was the closest, but weights are lost.

---

## 7. WHAT PROFESSIONAL STUDIOS ACTUALLY DO

**For hand-drawn raster animation, the answer is: human inbetweeners.**

From Animation Magazine: "Traditionally, lead animators draw key character poses and inbetweeners fill in the gaps by drawing each intervening frame by hand. The labor-intensive process is one of the main reasons animation goes overseas."

**The software assists, but doesn't replace:**
- Cacani: vector inbetweening with manual correction
- Harmony: morphing with manual cleanup of arcs and pancaking
- OpenToonz: vector tweening for simple motions

**No studio has fully automated raster inbetweening.** The technology doesn't exist at production quality. This is why the user is right to push — we're trying to do something the industry hasn't solved.

---

## RECOMMENDATIONS FOR CAPE JONES

### Immediate (this week):
1. **Wire up de-ghosting** as RIFE post-process — reduces the worst artifacts
2. **Scene-aware splitting** — don't interpolate across black frames/cuts
3. **Test Tahoma2D vectorization** on FlipaClip frames — if it works, this is the real solution

### Medium-term:
4. **Set up FLAVR** — flow-free approach might handle flat colors better
5. **Embrace 12fps** — anime standard. May not need 24fps at all.

### Long-term:
6. **Vector-first workflow:** Draw keys → vectorize → vector inbetween → render. This is the professional method.
7. **Hunt for AnimeInterp weights** through academic channels or alternative mirrors.

### The honest truth:
There is no perfect open-source raster inbetweening for cartoons. The professional answer is vector-based. Our best path is to move toward the vector workflow that Cacani/OpenToonz/Harmony use, not to keep pushing raster interpolation harder.

---

## SOURCES

- Cacani official site: https://cacani.sg
- OpenToonz documentation: https://opentoonz.github.io/e/
- Toon Boom Harmony morphing: professional animator workflows
- Anime pipeline: RETAS, Genga/Douga roles, limited animation technique
- AnimeInterp paper: CVPR 2021, "Computational Inbetweening for Line Drawings"
- Animation Magazine: "Automatic Inbetweens?" (2003)
