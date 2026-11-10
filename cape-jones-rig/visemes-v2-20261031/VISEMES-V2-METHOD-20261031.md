# Visemes v2 — mask-first swap library (Mars, 2026-10-31)

## Why v1 looked hand-tooled
V1 pasted a mouth drawing on top of the existing head. The head's own
mouth line, cheek lines, and little mouth line stayed visible underneath
and around the new shape — most obviously on OH / OO / W, where a
circle sat on top of the old horizontal mouth line and the vertical
cheek lines poked out beside it. That is a paste-over, not a mouth swap.

## Industry-standard method used in v2 (methods only, no code copied)
- **Toon Boom Harmony mouth chart + drawing substitution**
  (docs.toonboom.com, Harmony 20 Essentials: Manual Lip-syncing /
  How to Import Sound and Add Lip-Sync): lip sync is a standard
  mouth chart — A (m,b,p), B (s,d,j,i,k,t), C (e,a), D (A,E), E (o),
  F (u,oo), G (f,ph), X (silence) — and the mouth drawing on a frame
  is *swapped* for another drawing in the library via Drawing
  Substitution. The mouth lives on its own layer/symbol.
- **Toon Boom lip-sync setup rule:** the character head that mouths
  go onto should be a character *without a mouth area that will show
  behind the mouth shapes* — i.e. the base head must not carry a mouth
  that can bleed through. V2 follows this literally: the base is a
  clean head with the mouth zone blanked.
- **Adobe Character Animator viseme set** (adobe.com, Creating mouth
  shapes): 14 shapes in a Mouth group (Neutral, Smile, Surprised +
  Ah, D, Ee, F, O, M, Oh, R, S, Uh, W-Ow). For each viseme, the inner
  mouth mask is matched to the area between the lips, and the upper
  teeth do not move. V2 keeps the same 14-shape list as v1 (so lip-sync
  timing does not change), but each shape is now a complete drawing
  on a masked base, with the mask matched to the lip area.

## Layer order (v2, every viseme)
1. Head base (`sliced/Head_Front.png`, upscaled 4x for smooth lines)
2. SKIN MASK — gradient inpaint of the mouth zone, sampled per row
   from the head's own skin (left/right averages, smoothed over
   21 rows to kill banding), applied through a *feathered elliptical*
   mask centred on the mouth (weight 1 at centre, smoothstep feather
   to 0 at the ellipse edge). This covers the old mouth line AND the
   cheek lines where the new mouth sits, with no hard rectangle edge.
   First attempt used a hard rectangle and showed a visible patch
   edge + row banding on viewing; it was replaced by the elliptical
   feathered mask before reporting.
3. New mouth shape (complete drawing: lips, teeth, tongue, interior)
4. Outline

Mouth zone (fractions of head): x 0.235–0.825, y 0.595–0.815,
centre (0.5, 0.715). Chin tick below y 0.85 is preserved (it is not
part of the mouth). Cheek lines *outside* the mouth ellipse remain
faint at the face sides — that is the face's own linework, not a
mouth line showing through the new mouth.

## OH / OO / W fix (Mars's specific ask)
- OH: tall oval, dark interior + tongue, on masked skin.
- OO: TRUE circle (diameter 92px at 4x), dark interior.
- W: TRUE circle, smaller and tighter than OO (diameter 72px at 4x,
  heavier outline) — pursed, distinct from OO.
- In all three, the previous mouth line and the cheek lines in the
  mouth zone are covered by the skin mask *before* the circle draws.
  Proof: `proof-before-after-oo-w-20261031.png` (original head /
  v1-method paste on unmasked head / v2 masked head, for both OO and W).

## Reuse for eyes and expressions
Same method applies: eye strips and expression swaps go on a masked
eye zone (mask the old eye line first, then the new eye drawing),
never pasted over the old eyes. That is the next application of this
doc, not a new invention per eye.

## Files
- `clean-head-base-20261031.png` — masked head, no mouth (the base layer)
- `head-v2-NN-<key>-20261031.png` — full-head composites, 14/14
- `patch-v2-NN-<key>-20261031.png` — mouth-zone swap pieces (crop of
  the mask zone from each composite; paste at the manifest box)
- `visemes-v2-manifest-20261031.json` — keys, Toon Boom chart
  letters, patch boxes, layer order
- `build_visemes_v2.py` — builder (mask + shapes + proof)
- `proof-visemes-v2-on-head-20261031.png` — 14-head proof sheet
- `proof-before-after-oo-w-20261031.png` — OO/W before/after

## Status
V2 visemes 14/14 built and viewed. OO/W covered-lines fix verified
by viewing (mouth line gone, cheek lines covered in the mouth zone).
Mars approval: NOT claimed — he approves. Nothing pushed to any repo
in this task; the v1 hand-tooled method is NOT pushed anywhere here,
and the Goodville repo name was NOT guessed — it needs Mars to name
the exact repo before any push there.
