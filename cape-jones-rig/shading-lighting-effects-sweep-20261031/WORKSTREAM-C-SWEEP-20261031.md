# Workstream C — Shading / Lighting / Effects sweep, Mars 100% sweep 2026-10-31

**Folder:** `shading-lighting-effects-sweep-20261031/` — new dated folder only.
No repo push. No deletions. No existing file overwritten, renamed, or recoloured.
No new shading preset was made in this sweep.

## 0. Focus change applied (Mars, 2026-10-31 20:53 CDT, replying to shading preset master contact)

- **Shading preset library is SAVED. Stop making new shading presets right now.**
- The following are **PAUSED, not owed right now — no sweep effort spent there:**
  right-facing cel preset, new shading variants, true SSS, Blender Shader-to-RGB
  node run, true limb segmentation (as new presets).
- Re-prioritisation for the rest of this sweep: **TV PRODUCTION READINESS only** —
  what shading work, if any, is actually needed for shots end-to-end / per-shot
  proofs, versus additives/extras.
- **Shading library approval itself remains 0/1 for Mars, but the library is saved,
  not a production blocker to keep expanding.**
- Rule carried forward from the original brief, unchanged: **shading ≠ lighting.**
  Shading is a separate axis. Lighting levels L0–L5 are never renumbered.
  Light / shadow / bleed live on separate layers; base art is never recoloured.
  Run vs mapping is labelled. Defects are stated plainly.

## 1. Headline counts — with denominators, so percentages mean something

### 1a. Library saved: 100% catalogued, 0% approved (saved ≠ approved)

| Item | Count | % |
|---|---|---|
| Shading Preset Library entries catalogued | 54 / 54 | 100% |
| Library approval (Mars) | 0 / 1 | 0% — saved, not a blocker to expand |
| By tier: ARCHIVE 20, CLEAN 6, STRONG 7, SOFT 5, EXPERIMENTAL 13, REFERENCE 2, TEST_ONLY 1 | 20+6+7+5+13+2+1 = 54 | ARCHIVE 37.0%, CLEAN 11.1%, STRONG 13.0%, SOFT 9.3%, EXPERIMENTAL 24.1%, REFERENCE 3.7%, TEST_ONLY 1.9% |
| By plate: APOSE 51, ARMS_UP 3 | 51 / 54, 3 / 54 | 94.4%, 5.6% |
| Entries with individual PNGs | 34 / 54 | 63.0% |
| Set One entries, contact-sheet only (no individual file exists — stated, not invented) | 20 / 54 | 37.0% |
| Thumbnails in `thumbs/` | 34 | browsing copies only, not new presets |

Sources verified in this sweep (not re-derived from memory):
`shading-preset-library-20261031/shading-preset-catalog-20261031.json`
(counts block matches the 54-entry list; tier and plate counters re-run),
`SHADING-PRESET-INDEX-20261031.md`, `retrieval-proof-20261031.txt`.

### 1b. Shading sets / upgrade — the library's inputs, not new work here

- Shading upgrade (`shading-upgrade-20261031/`): 11 variants V0, V1, V2, V3, V4, V5,
  V6, V7, V8, V10, V9, plus HERO arms-up = 12 measured plates.
  CLEAN first-use: V9 Blender (smooth, edge +27.6, half +0.1), V7 (half +17.4,
  edge +40.1), V10 (half +17.7, edge +29.6). STRONG but faceted on apose:
  V2/V3/V4/V6 and continuation N01/N04/N07 — do NOT ship as clean apose relight.
- Shading sets (`shading-sets-20261031/`): Set One 20 entries (contact only),
  Set Two contact, new-variants 22 PNG files on disk (N01–N10 + X01–X10,
  with ARMS_UP duplicates for X01/X07).
- V9 Blender-vs-PIL gap: V9 Blender edge +27.6 vs PIL V2 +73.9.
  **Reclassified by the focus change: diagnostic additive, not a TV blocker.**
  V9 is already smooth and usable as a CLEAN preset; closing the numerical gap
  does not unblock any shot. It is not a new preset and was not re-run here.

### 1c. Production gap — reported separately, as instructed

This is the TV-production-readiness gap. It is NOT the library gap.
The library being saved does not close it.

| Per-shot axis (30 shots) | Done | % production-ready |
|---|---|---|
| Per-shot shading | 0 / 30 | 0% |
| Per-shot multiplane | 0 / 30 | 0% |
| Per-shot shafts | 0 / 30 | 0% |
| Per-shot effects | 0 / 30 | 0% |
| **All four shot axes combined** | **0 / 120** | **0%** |

**Production gap: 120 / 120 applications still owed = 100% gap on the per-shot axes.**
What is actually needed for shots end-to-end, in priority order:
1. **Per-shot shading application using EXISTING CLEAN presets** (V9/V7/V10 apose;
   HERO/X01-ARMS/X07-ARMS arms-up) — no new preset needed. This is the only
   shading work that is production work. Everything else in §2 is additive.
2. Per-shot multiplane, shafts, and effects applications (0/30 each) — same
   status; they are shot work, not preset-invention work.
3. Gold V6 per-shot application: V6 is 1 shot (arms-up) only; other 29 shots
   0/29 in the V6 report. That application is **blocked on Mars picks** (§4),
   not on inventing a new rim.

### 1d. What counts as 100% production-ready, vs additives/extras

- **Production-ready (the bar):** a shot carries an existing saved preset
  (shading, shafts, effects, gold) applied end-to-end, with a viewed per-shot
  proof, base art untouched, layers separate, and no defect hidden.
  No shot in this workstream meets that bar on the four axes above yet: 0/30 each.
- **Additives / extras — labelled as such, NOT blockers, NOT owed right now:**
  right-facing cel preset; any new shading variant; true SSS (beyond the
  N05 PIL approximation already in the library); Blender Shader-to-RGB node run
  (beyond the N10 PIL ramp equivalent); true limb segmentation (beyond the X08
  y-band proxy); true 3D normal pass (beyond the EDT-estimated normals,
  sigma 2, z-scale 1.5, already documented on every preset); clean facet-free
  apose relight as a *new* build (CLEAN presets already exist for apose use);
  V9-vs-PIL gap investigation; animated glint sparkle in settled crystal V2;
  cape-consumption animation (see §3 — owed only if Mars wants it);
  all-black symbiote variant (FUTURE ONLY, see §3).
- **Paused items are not counted as failures in the production percentage.**
  The 0% above is per-shot application only. Inventing paused presets would
  not raise it.

## 2. Scope (1) — G2 shading sets + Shading Preset Library: AUDITED, SAVED, PAUSED

- Status: **SAVED, approval 0/1.** No new preset made here. No preset renamed,
  re-tiered, or re-filed here.
- Normals warning (carried verbatim, not softened): normals are ESTIMATED from
  silhouette distance transform, NOT a true 3D mesh pass. That is a documented
  limit of the saved library, now classified as an additive (true 3D pass),
  not a reason to keep expanding the library before shots are done.
- Gap that was in the original brief and is now PAUSED — do not chase:
  no right-facing cel preset exists (verified: 0 entries with light=RIGHT and
  finish=CEL in the 54-entry catalog; V3 RIGHT is faceted Lambert, not cel;
  cel presets N04/V4 are LEFT). That absence is recorded, not fixed here,
  because Mars paused it.
- Retrieval: `retrieve.py` — 9 queries in the library's proof: 8 returned
  presets, 1 returned NO MATCH honestly (right cel), 1 refusal proof
  (`--tier TEST_ONLY` refuses for production unless `--allow-test`).
  Retrieval was not re-run as new work; the proof file was read and is cited.
- Viewed proof in this sweep: `sweep-contact-20261031.png` (tile 1 = library
  master contact, existing file, viewed). See §6.

## 3. Scope (2) — Crystallization: AUDITED, NO NEW FORM

### Preset 8 + Crystallization Power — `crystallization-preset8-power-20261031/`

- Approval 0/1 for preset + power pack. No repo push. Base plates untouched.
- 8 variants × 2 plates (apose + arms-up) = 16 plates, each transparent + grey
  copy = 32 P8 files on disk. P8-06 facet-glint = default power-on look.
- Facet-count correction carried forward, not hidden: seed grid 308 facets
  (spacing 48, seed 7); **occupied facets with actual pixels = 208.**
  All percentages in the V2 folder use 208.
- Methods: 16/20 run, 4/20 mapping (labelled in the Preset 8 report).
  Blender gem reference is a MATERIAL REFERENCE ONLY (blue-grey icosphere,
  not Cape, not pink/cyan, not the power).
- Animated glint sparkle in settled V2: 0/1 — **additive, not a TV blocker.**

### Crystal V2 transformations — `crystal-cape-jones-v2-transformation-upgrade-20261031/`

- Naming (Mars, 2026-10-31 20:30 CDT, final): V1 = earlier Crystal Cape Jones.
  V2 = this Preset 8 set, P8-06 default. Transformations #1/#2/#3 are
  animations INTO V2, not new forms. Do not confuse the two numberings.
- #1 = existing transition GIF, feet-up sweep, 6 frames, 0%→100%, horizontal
  y-band (reads like an edit/crop edit — stated in its own report).
- #2 = facet creep from feet, 16 frames, 200 ms, 3.2 s loop. At 50% (frame 8):
  104/208 facets = 50.0% of facets, 184,848 px = 49.4% of mask.
  Front is jagged/branching but still bottom-up overall, by design.
- #3 = vein-first + shard spikes + Gaussian-dot dust, 20 frames, 160 ms, 3.2 s.
  At 50% (frame 10): 104/208 facets = 50.0% of facets, 208,894 px = 55.9% of mask.
  Spikes (10–14 px, cyan) and dust (60 Gaussian dots/frame) fade to 0 at the
  final frame, so settled V2 is clean P8-06. Dust is a PIL proxy of the
  Gaussian Splatting point-field look, NOT a true splat render.
- Per-shot transformation application: 0/30 — **shot work, not preset work.**
- Future all-black symbiote variant: **FUTURE ONLY, NOT V2, NOT canon.**
  Mars said "maybe later". Body (18,18,22), white chest diamond only
  (zone x540–575, y460–545, approximate identification — cowl NOT recoloured
  white). With-cape and no-cape proofs exist; no-lower-cape version removes
  85,752 px (373,846 → 288,094) by zone erase for y≥600 outside x380–720,
  which is a proof, not a finished separation (true cape-piece separation
  would need the sliced cape pieces).
- Cape-consumption animation: **0/1, owed ONLY if Mars wants it animated.**
  It is not a production blocker unless Mars asks for it. Do not build it
  unasked as part of this sweep.

## 4. Scope (3) — Gold split V6: OPTIONS PREPARED, NOTHING DECIDED

- Files: `gold-split-wire100-20261031/` (V5 opaque split source) +
  `gold-split-rim-upgrade-20261031/` (V6 upgrade).
- **Approval discrepancy, flagged plainly — parent must resolve, not this sweep:**
  the V6 report on disk says approval **0/1** for the V6 upgrade set, preset
  filing, and power-candidate filing. The sweep brief from the parent stated
  rim upgrade **APPROVED 1/1**. This sweep does NOT claim approval as landed
  and does NOT overwrite the on-disk 0/1. Treat V6 as **unapproved until Mars
  confirms in writing**; the 1/1 in the brief may refer to a different approval
  (e.g. rim method) than the V6 set filing. Do not present V6 to Mars as
  approved on the basis of this sweep.
- V6 is NOT a level, NOT a V5 variant, replaces nothing. V5 unchanged.
  Old golds remain the preferred main gold look (old L3 V5 gold median
  (174,147,153); old gold-preserved V5 (194,148,158); both pinkish, softer).
  V6 gold is exact (255,180,80), delta 0, but hard — hence power/overlay
  candidate, not main gold look.
- Defect measured (V6 original): rim union 164,692 px; inside silhouette
  93,355 px = 56.7% of the ring; black interior covered 29,246/127,121 =
  **23.01%**, vs old L3 **2.67%** (about 8.6× less). Upgrade fixes this by
  construction: rim = dilate-minus-alpha, **0 px inside the plate, every
  variant**; opaque interior black preserved **100.0%** every variant
  (all interior incl. anti-alias fringe 96.73% — the 3.27% gap is anti-alias
  blending, not rim occlusion, same on all widths because the rim never
  touches the plate).
- Rim width ladder (1100×1500 canvas): thin 6 px = 34,304 rim px
  (gold 18,430 / cyan 15,874); medium 12 px = 59,938 px (31,106 / 28,832);
  heavy 20 px = 93,597 px (47,811 / 45,786).
- **Blocked picks — prepared in `GOLD-V6-OPTIONS-20261031.md`, NOT decided here:**
  1. Seam x550 (original, split through face position — outer-only rim only
     changes head-rim colour there, face interior NOT split) vs x650
     (gold 35,047 / cyan 24,891 px, head rim mostly gold, split in
     right-shoulder gap).
  2. Rim width default: 6 / 12 / 20 px (plus medium+halo variant).
  3. Power candidate, if any: DUAL-CHARGE (thin+halo) vs DUAL-AURA
     (medium+halo) vs SPLIT-OVERLAY (heavy+dark bg 0.55) — plus named-only,
     no-proof candidates SPLIT-DEFENSE, DUAL-FORM, ENERGY-CLASH, OVERLAY-UI.
  4. Rename original file? Original V6 source is
     `gold-split-wire100-20261031/v5-opaque-split-standard-20261031.png`
     (filename still says v5-opaque; V6 original by report naming only).
     It was NOT renamed or moved, to avoid breaking references. Rename is
     a Mars call.
  5. V6 per-shot application: 0/29 other shots (1 shot, arms-up, only).
- Viewed proof in this sweep: `gold-v6-options-contact-20261031.png`
  (thin / medium / heavy / seam-650, existing files, no decision implied
  by tile order).

## 5. Scope (4) — G3 shafts / Environmental Depth and Lighting preset: AUDIT, NOT DUPLICATED

- **The 5+5 improvement agent is running separately. This sweep did NOT
  re-run, re-render, or duplicate its work.** What follows is an audit of
  files found on disk in `shafts-environmental-depth-lighting-upgrade-20261031/`
  and `shafts-volumetric-upgrade-20261031/`, plus a prepared preset doc
  (`SHAFTS-ENV-PRESET-DOC-20261031.md`). If the separate agent updates those
  folders after this sweep, its newer files supersede this audit.
- Preset name: **ENVIRONMENTAL DEPTH AND LIGHTING** (v2-base + v3-improvement).
- **Approval status, stated with the same care as §4:** the preset JSON says
  `status: preset_approved_1_of_1_as_preset_not_production_ready` but also
  `improved_preset_approval: 0_of_1`. The sweep brief stated approval 1/1
  **as preset, NOT production-ready**. This sweep adopts exactly that reading:
  named preset exists, **production-ready = NO**. It does not claim the
  improved v3 set as approved.
- G3 original defect (do not re-present as volumetric): flat PIL rectangles
  blur 0/1/3/6/8 drawn OVER the figure — not real volumetric light.
- Volumetric v2 (Blender 5.2.3 Cycles CPU, 32 samples, ~11 min, 1100×1500):
  lights ABOVE, straight DOWN, through 6 ceiling slats, 5 built gaps
  (-3.0/-1.5/0/1.5/3.0), warm columns BEHIND Cape, figure pasted on top,
  shaft-over-figure max difference 0.0, no-crop PASS (edge alpha 0).
  **Measured: 3/5 columns clear at mid-height = 60%** (x282–379, 494–604,
  721–816; peak 54.8 vs valley 22.9). Top height: only 1 column passes
  (slats block the top row). Outer 2 gaps too dim to pass threshold.
  **Do NOT claim 5 distinct shafts.**
- Defects carried into v3, plainly:
  - Slats dominate top of frame (large black blocks).
  - No ground pools in v2 (floor removed, not fixed).
  - Shafts fade/dim toward the bottom.
  - Glare NOT completed in v2 (Blender 5.2 API, 3 attempts failed, no Glare
    file existed then); Eevee NOT run in v2 (method only).
- What the env folder now contains (audit, not a re-run):
  - 10 planned methods (I1–I5 industry + X1–X5 experimental) but **9/10
    method composites present** in `methods/`: I1, I3, I4, I5, X1, X2, X3, X4, X5.
    **I2 Eevee composite is MISSING** — Eevee scripts exist
    (`build_eevee.py`, `build_eevee_halfres.py`, outputs
    `shafts-eevee-20261031.png` / `shafts-eevee-halfres-20261031.png`
    named in code) but **no Eevee output file was found on disk**.
    Eevee therefore remains NOT evidenced, same as v2.
  - I3 ground pools: now present as a method (warm ellipses at feet_y 1282,
    centres 165/330/550/770/935, blur 18, behind figure) and in the v3-pools
    composite. That closes the v2 "no pools" defect *as a method composite*,
    not as a production-ready shot.
  - I4 Glare: now present as a file (`shafts-glare-blender-20261031.png` +
    `.exr`, Threshold 0.6, Strength 0.5, Size 6, Quality High, 5.2 API fix).
    That closes the v2 "Glare not completed" defect *as a file existing*;
    whether the Glare composite is production-ready is a separate agent's
    call, not claimed here.
  - I5 denoise: v3 used Cycles denoising ON; I5 also includes a PIL
    Gaussian sigma 1.0 proxy on v2 (proxy, labelled).
  - **v3 column measurement still fails the 5-column test:** measured runs
    v3 = [172–232], [298–800], [866–927] — the middle run is 502 px wide,
    i.e. centre columns merged, not 5 distinct columns. Peak 87.2 vs min 37.1
    (valleys much brighter than v2's 12.2). v2 denoised/soft variants keep
    the same 3 runs as v2. **Do NOT claim v3 fixes 5-column separation.**
  - v3 re-render parameters (from preset JSON): narrower slats 0.35, thinner
    0.15, wider volume, outer spots 12000, centre 8000, spot 32°, Sun 5.0,
    samples 24, Cycles denoising ON.
- Preset rules (from preset JSON, carried into the prepared doc):
  shafts ALWAYS behind figure (`shafts × (1 − figure_alpha)`, figure on top
  at full opacity); base art never recoloured; no-crop (edge alpha 0);
  do NOT claim 5 columns unless a measured mid-height run = 5; do NOT claim
  a Glare file unless it exists on disk; do NOT claim Eevee unless the
  Eevee render file exists. On the last two rules as of this audit:
  Glare file now exists; Eevee file does not.
- Per-shot shafts: 0/30 (shot work, separate from preset existence).

## 6. Scope (5) — Effects Sunbeam Preset v1 upgrade: STATUS, NOT A NEW RENDER

- Preset v1: `presets/effects-sunbeam-preset-v1-20261031/` — saved exactly,
  reproducible (Blender 5.2.3 Cycles CPU, 640×480, 32 samples, denoising OFF,
  Glare Fog Glow + Sun Beams compositor stack, orbs at (-0.9,0,1.3) and
  (0.9,0,1.3), radius 0.22, Emission 8.0). Source frame
  `showcase/effects-v2-proof-20261031/effects-v2-proof-blender-20261031.png`.
  Read is energy-orbs only — NOT a Dragon Ball character, no branding shipped.
- Known v1 defects (carried, not hidden): orbs slightly high/wide of fists
  (snap owed in v1 doc); visible Cycles noise at 32 samples (denoise owed);
  volume haze uniform rather than shaft-shaped (shaft masking owed).
- **Sweep-brief status vs on-disk evidence — flagged, not papered over:**
  the brief states "orb snap done" for the v1 upgrade, but **no sunbeam-upgrade
  folder or snapped proof file was found on disk in this sweep** (only the
  v1 preset folder and the v2 proof folder). This sweep therefore records
  orb snap as **stated-done in the brief, unverified on disk** — the parent
  should point to the snapped file before it is presented as done.
  Denoise, shaft masking, and upgrade approval remain **owed** on either
  reading. No new sunbeam render was made here.
- Per-shot effects: 0/30. Per-shot shading/multiplane/shafts/effects are
  0/30 each (see §1c). Effects work for TV is per-shot application of the
  saved v1 preset (plus its upgrade, once verified), not inventing a new
  effects preset.

## 7. Still owed — production work only (paused items removed)

| # | Owed item | Count | Blocker / owner |
|---|---|---|---|
| 1 | Per-shot shading (existing CLEAN presets, end-to-end) | 0/30 | Shot work, unblocked by preset invention |
| 2 | Per-shot multiplane | 0/30 | Shot work |
| 3 | Per-shot shafts (env preset, once separate 5+5 agent lands) | 0/30 | Separate 5+5 agent's preset — do not duplicate |
| 4 | Per-shot effects (sunbeam v1 + upgrade, once verified) | 0/30 | Upgrade verification (snap file) + approval |
| 5 | Gold V6 picks (seam, width, power candidate, rename?) | 0/4 picks | **Mars — blocked, see §4** |
| 6 | Gold V6 per-shot application (other shots) | 0/29 | Blocked on pick #5 |
| 7 | Shading library approval | 0/1 | Mars — saved, not a blocker to expand |
| 8 | Shafts env improved-preset approval | 0/1 (preset JSON) | Mars / separate agent |
| 9 | Crystallization preset+power approval | 0/1 | Mars |
| 10 | Crystal V2 per-shot transformation | 0/30 | Shot work, if wanted per shot |
| 11 | Sunbeam upgrade approval | 0/1 | Mars, after denoise + shaft masking + snap verification |
| 12 | Eevee shafts render file (I2) | 0/1 file found | Separate 5+5 agent (audit only here) |

## 8. PAUSED — not owed right now, not counted as production failures

Right-facing cel preset (0 new builds here) · new shading variants ·
true SSS · Blender Shader-to-RGB node run · true limb segmentation ·
true 3D normal pass (as a new build) · V9-vs-PIL gap investigation ·
animated glint sparkle in settled V2 · cape-consumption animation
(unless Mars asks) · all-black symbiote variant (FUTURE ONLY).

If Mars un-pauses any of these, it returns as a separate, explicitly
approved task — it does not retroactively become a TV blocker.

## 9. Files delivered in this sweep (new folder only)

- `WORKSTREAM-C-SWEEP-20261031.md` — this report
- `GOLD-V6-OPTIONS-20261031.md` — options, no decisions
- `SHAFTS-ENV-PRESET-DOC-20261031.md` — prepared preset doc (audit, not a re-render)
- `sweep-contact-20261031.png` — audit contact, 6 existing tiles, viewed
- `gold-v6-options-contact-20261031.png` — gold options contact, viewed
- `sweep-counts-20261031.json` — machine-readable counts in §1

## 10. Viewed proofs — what was actually viewed in this sweep

- `sweep-contact-20261031.png` and `gold-v6-options-contact-20261031.png`
  (built in this sweep from existing files, then viewed) — see §6 note below.
- Source contacts/files read or measured in this sweep: library master contact,
  shading upgrade contact, V6 power-candidates contact, V6 before-after contact
  (via report), crystal future-symbiote contact, shafts env final + methods
  contacts, shafts v2 measurements JSON, env measurements-methods JSON,
  V6 measurements JSON, library catalog JSON.
- No file was claimed viewed that was not opened or measured. No new preset
  file was created. No base art file was opened for editing.

## 11. What this sweep did NOT do (so the parent does not over-claim)

- Did NOT make a right-facing cel preset, SSS, Shader-to-RGB, limb-segmentation,
  or any new shading variant (paused by Mars 20:53 CDT).
- Did NOT duplicate the separate 5+5 shafts improvement agent (no Cycles/Eevee/
  Glare re-render here).
- Did NOT decide any Gold V6 pick, rename any file, or claim V6 approved.
- Did NOT claim any shot production-ready, any preset landed, or any per-shot
  axis complete. Per-shot axes are 0/30 each.
- Did NOT claim a sunbeam snapped proof on disk (brief says snap done;
  no file found — see §6).
- No browser work was required or claimed. No repo push. No deletions.
