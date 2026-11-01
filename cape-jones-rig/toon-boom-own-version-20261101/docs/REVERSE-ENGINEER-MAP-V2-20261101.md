# Reverse-Engineer Map v2 — Toon Boom Harmony 27, for OUR OWN version

Mars, 2026-11-01 01:33 CST: reverse engineer Toon Boom, make our own version
while we use it, and keep trying to get it installed on the browser.

Legal method, stated first, so it is never mistaken for a crack:
- Sources: public Harmony docs, our own usage, and read-only inspection
  of the owned installer name/size only. No Toon Boom code copied, no
  binary redistributed, no key extracted, no activation bypassed.
- Reverse engineering here = observing a tool we own, documenting its
  public interfaces, and writing interoperable code for OUR original art.
- This map is v2: it supersedes the v1 map in toon-boom-wire100 only
  by adding the own-version implementation column. V1 docs stay untouched.

## 1. Interfaces reverse-engineered (behaviour, not code)

| # | Harmony interface | Observed behaviour | Own-version implementation |
|---|---|---|---|
| R01 | Node View / Drawing + Peg | Drawing holds art; Peg holds x, y, rotation, pivot. Z-order = draw order. | cjtoon.py: node + peg per piece, DEFS-stable z sort, pivot (ox,oy) |
| R02 | Peg pivot | Rotation about peg pivot, not piece centre. Top-centre (0.5,0) for torso/arms/thighs/shins; forearmL (0.39,0.11), forearmR (0.63,0.11); centre for knees/caps/hands. Cape/pelvis/head centre = ASSUMED, verify in-app. | pivot_xy() in cjtoon.py; assumed pivots flagged, not claimed confirmed |
| R03 | In-place rotate bug (our lesson, not Harmony's) | PIL in-place rotate clipped 25.7% of Arm 2 bicep, 48.0% of forearmR. | Own version rotates about pivot in rig math; image side must use large-temp rotate, never in-place |
| R04 | Drawing substitution | Swap whole drawing at a key (hand, mouth, eye). Whole-piece swap only. | Substitution rule in scene JSON; no crop/erase in code |
| R05 | Deformers (Bone/Curve/Envelope) | Bone chain drives a drawing; envelope follows a shape. | FK chains in CHAINS: arm1/arm2/leg1/leg2/spine/cape |
| R06 | Kinematic Output | Output node under a deformer, e.g. hand follows arm deformer. | handL/handR are chain ends, wrist-anchored at forearm end |
| R07 | Master Controller | One dial drives many nodes (pose dial). | Future: pose dial = named key set; NOT built yet, see checklist |
| R08 | Onion skin + Xsheet | Previous/next frames ghosted; Xsheet holds keys, not blends. | onion_weights(): nearest keys at 0.35; inbetween() smoothstep |
| R09 | Inbetweening | Real intermediates between keys, with easing. Crossfade is NOT inbetweening. | smoothstep(3t^2-2t^3), tested: mid = 0.5 exactly at frame 12/24 |
| R10 | Camera / multiplane | Camera plane + depth layers; ground line is a stage rule, not a render trick. | Stage 1400x1600, ground y=1475, reported, never shifted to fake planting |
| R11 | Effects (L0-L5, rim, shadows, crystal, dream) | Effect stack on top of drawings, in order. | Effect order carried in scene rules; effect rendering itself is NOT in own version yet |
| R12 | Lip-sync / Storyboard Pro | Phoneme chart drives mouth substitution at 107 BPM, 14/14 chart. | Chart carried as data; mouth substitution via R04, not yet wired to audio |
| R13 | Batch render / Control Center | Render a scene to video from a script, headless-ish. | Own version exports keys as JSON; video render from keys is a next job, NOT claimed here |
| R14 | Templates (.tpl) + Libraries | A rig saved as a template, reused. | Own template = scene.cjstage.json; .tpl must still be exported from Harmony after activation |

## 2. File formats (public-doc level, not byte-exact)

- .xstage: a scene FOLDER, not a self-contained blob. Do not treat it as one file.
- .vbd: compact scene file, v25+. Own version default: non-compact, inspectable JSON.
- .tvg: vector drawing format. Own version does NOT convert bitmap pieces to .tvg silently; bitmaps stay bitmaps, whole.
- .pal/.plt: palette. Own version ships CSV (7 colours, measured). A byte-exact .plt must be exported from Harmony after import — CSV is NOT a fabricated .plt.
- .tpl: template. Own version ships .cjstage.json; .tpl must be exported from Harmony after activation.
- QtScript (.js, ECMAScript): public pattern node.getAttr("Top/Drawing-P", 1, "position.x").doubleValue(). Own version generates a READ-ONLY check script with that pattern; it does not write Harmony internals.

## 3. What our version does NOT need Harmony installed to do

Load 19 nodes, validate 6 FK chains, smoothstep-inbetween keys, onion-skin
weights, palette load, .cjstage export/import round-trip, Harmony check-script
generation. All tested exit 0, numbers only, no PNGs.

## 4. What still needs Harmony activation (Windows/Mac only)

Run harmony_check.js in-app, verify cape/pelvis/head pivots, save .tpl,
export verified .plt, render one frame in Harmony, log menu paths and
attribute names, and confirm edition/subscription/start/end in-app.
