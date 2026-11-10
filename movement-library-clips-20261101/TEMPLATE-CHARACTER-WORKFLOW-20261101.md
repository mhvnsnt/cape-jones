# Template Character Workflow — NEXT PHASE, NOT STARTED HERE
Mars, 2026-11-01 11:14 CST update: soon we will start getting other
characters from those shows over as TEMPLATES, verify they stand in
our show and move around in the world cleanly, then change them over
to a custom original character of Mars's own.

Standing method (SHOW-BUILDING-METHOD): placeholder/test character
→ kitbash + reskin → redesign → completely different original
character. Art style may stay similar (style != character identity).
Barred ONLY: exact likeness shipped as-is, character literally,
name, script dialogue, logo. Character images only as transform-only
production reference (parody / wholly different character before
release, never ship as-is).

## This task: DO NOT start importing show characters yet
This folder's clips are Cape Jones ONLY. No show character was
imported, reskinned, or shipped here. This file is the workflow,
ready for the next phase, so that phase does not start by guessing.

## Phase 0 — placeholder check (before any reskin)
For each candidate template, in order, with a gate per step:
1. STANDS CLEANLY: placeholder stands on the ground plane, feet
   planted, no floating, no clipping through floor, bbox bottom =
   ground line every frame, proportions readable at 1920×1080 and
   at chat size (700×800). Gate: ground check PASS, no edge clipping.
2. MOVES CLEANLY: placeholder walks / steps / gestures on the
   movement library timing (24 fps, on 2s normal, on 1s snaps,
   holds 6-24f), with wrist gate (wrist end to forearm end, wrist
   nearer than fingertip) and knee-feet gate (knees+feet same
   direction) PASS, and flash gate PASS (no >3 flashes/sec, no
   black/white forearm flip, no red flash).
3. WORLD CHECK: placeholder in a clean painted background (no debug
   dots, no second hero in the plate), lighting level named, cape/
   clothing layers in correct order (back layer behind torso, collar
   top layer at shoulder/neck), no layer popping frame-to-frame.
4. If ANY gate fails, fix the timing/layer/ground — do NOT ship the
   placeholder as a character, and do NOT fix it by copying donor art.

## Phase 1 — kitbash + reskin
- Swap palette, suit, cape, head shape, hands, feet to Cape Jones
  show language (white suit + purple cape family, or Mars's chosen
  palette for that new character), keeping ONLY movement timing,
  pose structure, and layer order from the template.
- Record every swap in a manifest: template movement → new piece →
  source (Cape Jones pack / new clean-cut piece, never donor art).
- Re-run all gates (ground, wrist, knee-feet, flash, layer order).

## Phase 2 — redesign
- Change silhouette, proportions, face, and distinguishing features
  until the character reads as a different character at a glance,
  not as the template with a new colour. Mars approval is the gate:
  0/1 until he sees it and says so. No approval is assumed from a
  description.
- Remove any remaining template-specific silhouette, accessory, or
  pose that is the template's signature — or, if Mars wants that
  pose, keep the POSE (movement is pullable) with a wholly different
  body, not the template body.

## Phase 3 — completely different original
- New name (Mars's, never a show name), new backstory slot in Cape
  Jones canon (not the donor show's story), new voice/dialogue
  slot (never donor dialogue), no logo.
- Only then may the character appear in an episode cut. Before that,
  it stays labelled TEMPLATE / PLACEHOLDER in every file name and
  report, never in a final.
- Landing: template work lands in its own dated folder, PR-only,
  verified size+SHA on main, 0 deletions unless Mars approves that
  exact deletion. Placeholder files that still look like a donor
  character are NOT landed as final episode assets.

## What to bring to Mars at the start of that phase
- One placeholder clip per candidate, with gates PASS/FAIL listed,
  ground + movement + world checks shown, and the reskin plan
  (which pieces change, which timing stays).
- A plain list of candidates that FAILED the stand/move cleanly
  check, with the reason, so Mars does not have to re-approve a
  broken template.
