# Workstream E — Blender 5.2.3 production render + ACES + compositing — report 2026-10-31

## Counts (task gates)

- Blender 5.2.3 render viewed: **1/1** (was 0/1)
- ACES/OCIO test in Blender: **1/1** (was 0/1)
- End-to-end proof shot, Cape Jones ALONE (universal-pipeline gate): **1/1** (was 0/1)
- All three are the same Blender pipeline (one script, one node tree, two view
  transforms). The Standard render is BOTH the Blender-render proof AND the
  proof shot — one artefact, counted once per gate, not two separate shots.
  The ACES render is a separate file (same node tree, different view).

## What was rendered (all Blender, CPU, no PIL image presented as a render)

Engine: Blender **5.2.3 LTS** (`blender-5.2.3-linux-x64/blender`, NOT 4.5.3),
**BLENDER_EEVEE, CPU only** — local VM has no GPU. Kaggle GPU render is
OUT OF SCOPE for this subagent (no browser) and is **pending for the parent**;
no GPU/Kaggle render is claimed anywhere here.

Plate (all three renders): approved clean fighting pose
`reposes-v7c-clean/fighting-pose-forward-bicep-curl-gauntlet-out-fixed-v7c-clean.png`
(1100x1500). Label gate passed three ways: driver PIL/numpy pure-red
(255,0,0) count = **0**; Blender pixel-scan pure-red count = **0** (limit 100);
final outputs pure-red count = **0** each. No labels in any final.
Base art: `Character_untouched` image node is never modified in place;
grade/rim/bleed/shadow are separate nodes layered over it.

| File | Resolution | Blender RenderTime* | Script total† | Nodes / Links |
|---|---|---|---|---|
| `proof-shot-cape-jones-alone-level2-v2-standard-20261031.png` (+ `.blend`) | 660x900 | 00:05.40 | 8.9 s | 34 / 43 |
| `aces-test-cape-jones-level2-v2-aces20-rec1886-20261031.png` (+ `.blend`) | 660x900 | 00:03.65 | 6.9 s | 34 / 43 |
| `grey-key-mask-fighting-pose-20261031.png` (+ `.blend`, diagnostic) | 660x900 | 00:01.97 | 4.8 s | 20 / 22 |

\* RenderTime from the PNG metadata (pure render). † Script total includes the
label-gate pixel scan + tree build + render. Resolution is 60% of the plate
(compositor Scale 0.6); all compositing math runs at full 1100x1500 first,
so rim 3 px / bleed band 3–8 px are full-res spec values.
`.blend1` files in this folder are Blender save backups from the re-runs,
not deliverables.

Script: `blender-proof-render-20261031.py` — modes `proof | mask | shadow`.
It REFUSES plates with >100 pure-red pixels (SystemExit, no render), in
Blender as well as in the driver pre-check.

## Proof shot — viewed by the agent (Standard file, final, not a try)

`proof-shot-cape-jones-alone-level2-v2-standard-20261031.png` — viewed:
Cape Jones ALONE, approved fighting pose (fists up, gauntlet-out-fixed),
full body in frame, **clean grey background** (the "clean background" branch
of the proof spec — NOT the room at 2.5x; room was not used here),
Level 2 v2 grade, no labels, no recoloured base art.
Visible: warm cream suit (graded white), purple cowl intact, warm amber rim
around the whole outer silhouette, orange bleed halo, soft blue-violet
ground shadow under/behind the feet. No god rays (Level 2 never has them),
no bloom/Glare (Level 3). **PROOF SHOT ONLY — NOT Mars-approved.**
Final Standard pixels are identical to the viewed try4 (max pixel diff 0).

Measured samples, Standard final (sRGB):
- Background corner: (129,129,129) — grey 128 preserved, ungraded control.
- Suit torso sample: (255,225,173) — warm cream (PIL v2 sRGB gain would give
  white → (255,242,179); Blender linear gain gives a slightly deeper warm —
  hue family R>G>B matches, numbers differ, see "honest differences").
- Shadow zone: try4-vs-no-shadow pixel diff = 17,020 pixels, all in
  y 687–803 (feet region), x 193–468 — zero elsewhere. No waist/head shadow.

## ACES test — viewed by the agent (ACES file, final)

View transform: **ACES 2.0**, display device: **Rec.1886**
(Blender 5.2.3 built-in OCIO config; views available on sRGB display:
Standard, ACES 1.3, ACES 2.0, AgX, False Color, Raw — Filmic is gone in 5.2).
Same node tree and pose as Standard; ONLY the view/display changed, so the
difference is purely the OCIO view transform. Colour-managed in Blender,
not flat PIL.

**Verdict: DIFFERED from the L5 Rec.709 gamma 2.4 finishing spec — honestly.**
- The display EOTF family matches (Rec.1886 ≈ BT.1886 ~2.4 gamma), but the
  ACES view transform is NOT plain Rec.709 gamma 2.4: ACES applies its own
  RRT tone mapping on top of the display EOTF.
- Measured, Standard → ACES 2.0: background grey (129,129,129) → (107,107,107);
  suit highlight (255,225,173) → (192,172,150). Mean absolute pixel
  difference 24.0, max 73. Viewed: ACES image is visibly darker and greyer,
  warm cream becomes grey-beige, rim warmth is muted, cowl stays purple.
- Consequence: for a STRICT L5 delivery (Rec.709 gamma 2.4 finish), use the
  Standard view, not ACES 2.0. ACES 2.0 is a creative look, not the L5 finish.
  ACES 1.3 was NOT tested in this run (owed if Mars wants a version
  comparison); only ACES 2.0 is claimed here.

## Level 2 v2 stack in Blender (translation, not a PIL copy)

- Grade: gain (1.10, 0.95, 0.70), character layer only; grey background
  left ungraded as a control. (DIFFERS from PIL v2, which graded the whole
  plate including background.)
- Rim: outer-only, Dilate 3 px minus original mask, ADD, warm amber
  sRGB (255,180,80) stored as a linear socket colour.
- Bleed: band Dilate 8 px minus Dilate 3 px, SCREEN, orange sRGB (255,120,0)
  × 0.20, edge band only, never whole-suit tint.
- Shadow: full-size squashed (Scale Y 0.22) + blurred (20 px) ground shadow,
  blue-violet sRGB (40,40,90) × 0.35, translated to the feet.
- NOT in this build: `.cube` LUT node (none exists in Blender 5.2's
  compositor — the LUT file is recorded in the .blend text block, NOT
  claimed as applied); god rays; Glare/bloom; internal line light; lit-side
  rim/bleed fade. See "owed".

## Honest differences from PIL v2 (not hidden)

1. Linear vs sRGB math: Blender compositing runs scene-linear, PIL v2 runs
   sRGB. Same hue family, different measured RGB (see samples above).
   No pixel-match to PIL v2 is claimed.
2. Grey-key centre correction (found by a failed mask run): Blender's
   `image.pixels` API reads sRGB (grey 128 = 0.502), but compositor nodes
   run scene-linear, where grey 128 = **0.216** (tolerance 0.044). Using
   0.502 keyed the background as foreground (first mask came out inverted:
   background white). Corrected mask is a solid white silhouette on black
   (final mask pixel-identical to the viewed corrected mask, max diff 0).
3. Rim/bleed are UNIFORM in Blender v1 — PIL v2's lit-side fade
   (left 1.0 → right 0.3) is owed in the Blender stack.
4. Internal line light (PIL v2 dark-line tint toward rim colour) is NOT in
   this build — owed.
5. Shadow geometry differs: Blender ground blob (squashed + blurred
   silhouette) vs PIL v2 ellipse + two foot pads — pads geometry is owed.
   The Crop bottom-band pads approach was tried and FAILED in this
   compositor (try1: strip centred at waist, 2,687 diff pixels in waist
   band y 358–418; try2/try3: zero pixels contributed, verified by
   try2-vs-try3 pixel diff 0.0). Full-size Scale/Translate behaviour was
   then proven by diagnostic (Scale anchors at canvas centre; Translate
   Y negative moves DOWN — measured against the true plate bbox
   x 182–499 / y 152–776 output) before the working shadow was built.
6. Relative render paths fail in Blender background mode (Render error:
   No such file or directory — caught on the first finals run). The script
   now forces absolute output paths; finals were re-rendered with
   absolute paths and verified on disk.

## Still owed (not claimed as done)

- PIL ellipse + two-foot-pads shadow geometry in Blender (Blender has a
  working ground shadow; pads geometry is the refinement).
- Internal line light in Blender; lit-side rim/bleed fade in Blender.
- ACES 1.3 comparison (only ACES 2.0 tested).
- Room-at-2.5x version of this shot (this proof uses the clean-background
  branch; room compositing in Blender is a separate shot).
- Kaggle GPU render (pending for the parent — this subagent has no browser).
- Mars approval of the proof shot itself (it is a proof, not an approval).
- Prior compositor-stack note: the old 18-node/22-link file stack used the
  labelled v6 plate and is DEBUG ONLY — superseded for finals by this
  34-node/43-link clean-plate stack. The old file was not modified.

## Compliance

No push, no delete, no subagents spawned. No PIL image is presented as a
Blender render — every PNG here carries Blender RenderTime metadata and a
matching `.blend`. No file Mars has seen was overwritten; all files in this
folder are new and dated 20261031.
