# Animation / movement examples — Mars, 2026-10-31
Logged as STUDY, not as assets to copy. Influence only: Johnny Bravo,
Gumball, Scooby-Doo / Scooby gang, Space Ghost (via Cape Jones canon).
Cape Jones stays his own character, white suit + purple cape, his own
canon. No show frames, GIFs, or character art from those shows are
copied into this doc or into any repo. The repo version of this log
will contain descriptions and timing only, never the show files.

## What was actually received — check this first
20 examples, files 10001790xx_4 through _23, all SINGLE-FRAME stills
(JPEG, despite .gif names), 162x200 to 736x848, 7–94 KB each.
0 animated frames to measure. So no FPS can be read off these files.
File 1000179069_33_9jye.jpg is a byte-identical duplicate of _13
(Scooby dance, 50,558 bytes, 736x848) — counted once, not twice.
Files _24 through _32 were also present on disc at 10:46 but were NOT
in the messages for this log — not logged here yet, awaiting Mars.

## Frames per second / drawings per second — the rule to use
TV cartoons in this style are made at 24 fps.
- Normal movement: animated on 2s = 12 drawings per second, each drawing
  held 2 frames. Walk, lounge, talk, dance groove, flex pose holds.
- Fast action: animated on 1s = 24 drawings per second. Punch snap,
  dance hit, jump, head snap, cape whip.
- Holds: a pose drawing held 6–24 frames (0.25–1.0 sec) for a joke beat,
  a flex, a "HEEEEY" beat, or a reaction.
For Cape Jones puppet animation, that means: do NOT make a new drawing
for every frame. Reuse locked v8 pieces, move/rotate them on 2s for
normal motion, on 1s only for snaps, and hold poses. A 2-second dance
groove = 48 frames, ~24 unique piece positions on 2s, not 48 new drawings.

## Examples, movement only, mapped to Cape Jones rig

1. _4 — Standing confident, arms at sides, chest out, feet apart.
   Cape Jones: v8 T-pose with arms down at sides (A-pose variant), no new pieces.
2. _5 — Close-up head, lying / leaning back, smug.
   Cape Jones: Head_Front + Mouth_Smile/Closed, head tilt back. Needs: head tilt angle (rotate head piece, no new art yet).
3. _6 — Dance flex, fists up at chest, knees bent, bouncing.
   Cape Jones: cut-limb arms bent at elbow, fists (Pack1), knees bent (cut legs), torso bounce up/down 10–20px on 2s. Needs: bent-elbow arm assembly (cut limbs exist).
4. _7 — Lean forward, arms reaching forward/down, knees bent, stepping.
   Cape Jones: torso lean forward (rotate torso), arms forward (foreshortened hand, Pack1), legs stepping (cut legs). Needs: foreshortened forearm piece (Pack1 hand exists, forearm foreshorten is missing).
5. _8 — Lounging on couch, legs crossed, watching, relaxed.
   Cape Jones: reclined torso + crossed legs. Missing: reclined torso piece, crossed-leg pose (cut legs can approximate, not a true cross).
6. _9 — Lounging, one arm up holding a remote, other hand on chin, legs up.
   Cape Jones: arm up (rotate upper arm), grip hand (Pack1 Grip), head on hand. Missing: remote prop (new prop, not a body piece), reclined torso as in _8.
7. _10 — Gumball standing excited, arms slightly out, mouth open, big eyes.
   Cape Jones: arms out, Mouth_Open, eyes wide. Missing: wide eye strip (Pack4 eye strips, pending), excited mouth (Mouth_Open exists).
8. _11 — Group dance, 4 characters stepping, arms up/swinging, in sync.
   Cape Jones (solo first): step legs alternating, arms swinging opposite, torso bounce. Group version needs other characters, not in this rig.
9. _12 — Solo dance, arms swinging across body, legs bent, tail/body twist.
   Cape Jones: arms swinging (rotate at shoulder), legs bent, torso twist. Missing: torso twist / 3/4 torso piece (front torso only right now).
10. _13 — Solo dance pose, arms crossed forward, legs in a wide stance, grinning.
    Cape Jones: arms forward across chest, legs wide (v8 legs wider apart), Mouth_Smile/Teeth. Missing: arms-crossed assembly (cut limbs can do it, needs a test).
11. _14 — Pose in briefs / flex, hands on hips or flexing, chest out.
    Cape Jones: replicate POSE only, not costume. Hands on hips, chest out. Missing: hands-on-hips hand angle (Pack1 relaxed/grip can approximate).
12. _15 — Beach flex, one arm flexed, other down, legs apart, showing off.
    Cape Jones: flex arm (cut limb bent), other arm down, legs apart. No new pieces.
13. _16 — Lab flex / dance, fists up, legs apart, bouncing.
    Cape Jones: same as _6, fists up, bounce on 2s. No new pieces.
14. _17 — Karate stance, arms up in guard, legs in a wide stance.
    Cape Jones: replicate STANCE only, not the gi costume. Guard arms (cut limbs), wide legs. No new pieces.
15. _18 — Pixel-art arms forward, fists out, leaning in.
    Cape Jones: arms forward, fists (Pack1), torso lean. Missing: foreshortened fists (Pack1 foreshortened reaching hand exists).
16. _19 — Standing flex, one bicep flexed, other hand on hip.
    Cape Jones: flex arm + hip hand, as _11/_14. No new pieces.
17. _20 — Lying on floor, chin in hands, legs kicked up behind.
    Cape Jones: lying torso + legs up. Missing: lying torso piece, legs-up pose (cut legs can approximate).
18. _21 — Shirtless flex, hands on hips, chest out, "HEEEEY" beat.
    Cape Jones: replicate POSE/beat only, not shirtless. Hands on hips, chest out, hold 12–24 frames. No new pieces.
19. _22 — Looking in a mirror, one hand holding mirror up, head turned to profile.
    Cape Jones: Head_Profile exists, grip hand, mirror prop (new prop). Missing: mirror prop only.
20. _23 — Dance punch, one arm punching forward, other back, legs stepping.
    Cape Jones: punch arm forward on 1s (fast snap), other arm back, step legs. Missing: foreshortened punch forearm, as _7.

## Missing pieces list, from these 20 examples (counted)
- Cape states: draped, lying flat, swinging left/right, billowing — 0/4 done, Pack5 pending. Current cape: back-main + collar only.
- Torso angles: 3/4, side, reclined, twisted, lying — 0/5 done, front only.
- Leg poses: seated, crossed, lying-up, stepping — cut limbs can approximate 2/4, true seated/crossed/lying are missing.
- Arm foreshorten: reaching forward, punch forward — 1/2 done (Pack1 foreshortened hand, forearm foreshorten missing).
- Heads: 3/4, back, scowl — 0/3 done in Pack4, front + profile only.
- Eyes/mouths: wide, scowl, etc. — Pack4 pending (8 eye strips, 14 visemes).
- Props: remote, mirror — 0/2 done, both are simple props, not body pieces.
- Costumes: gi, beach, shirtless — NOT to be made. Replicate pose, keep Cape Jones white suit + purple cape.

## Next step, in order
1. Finish v8 repo lock (already uploading, separate from this log).
2. Push this log to the cape-jones repo in a SEPARATE animation PR, descriptions only, no show files.
3. Build repose tests from v8 pieces first: A-pose (arms down), flex, dance groove, lounge, punch — using cut limbs + Pack1 hands, on 2s, holds as above.
4. Then generate/make only the missing pieces listed above, one pack at a time, clean-cut sliced, shown to Mars before the next pack.

## Batch 2 — pose sheets, 2026-10-31 10:47 CDT (files _24 to _32, + duplicate _33)
All single-frame stills again, JPEG/PNG, no animated frames to measure.
Pose sheets, so one file = many poses. Do NOT copy these sheets into
any repo — descriptions only, same rule as Batch 1.

- _24 (570x570): Johnny Bravo pose sheet, labelled "20 DESIGN / 80 FILES" —
  ~20 small poses: flex, dance, lean, arms crossed, pointing, tuxedo,
  karate, fall, etc. For Cape Jones: a pose library, not one movement.
  Most poses map to flex / dance / lean / arms-crossed already listed.
  New: tuxedo pose (costume only, ignore), fall pose (needs lying/fall torso).
- _25 (605x507): Johnny Bravo pose sheet, ~20 poses: flex, dance, point,
  Santa hat, motorcycle, "I'M AWESOME" hold, etc. Same mapping as _24.
  New: motorcycle ride pose (needs seated legs + handlebar grip — prop,
  not a body piece to copy).
- _26 (2028x1628, largest file): Johnny Bravo "19 Designs" sheet, ~19
  large poses: arms crossed, dance with finger snap, comb hair, karate
  kick, motorcycle, arms out, flex, fall into ground, etc. New for
  Cape Jones: comb-hair hand (Pack1 hand + comb prop), karate kick
  (leg kick pose — cut legs, leg raised), fall-into-ground (lying torso).
- _27 (390x580): Johnny Bravo pose sheet, 9 poses: flex, dance, point,
  arms crossed, fall, etc. Same mapping, no new body parts.
- _28 (921x2048, phone screenshot): Johnny Bravo pose poster, single
  pose: arms up, hands open, chest out. Ignore the phone UI / eBay text.
  Cape Jones: arms up (rotate arms up), hands open (Pack1 Open).
- _29 (588x330): Gumball + Darwin dancing together, arms up, legs
  stepping, mouths open. Cape Jones solo first: dance step + arms up.
  Group version needs a second character rig, not in this batch.
- _30 (1280x720): Gumball shouting / reacting at a table, Darwin beside.
  Cape Jones: shout mouth (Mouth_Shout exists), wide eyes (Pack4 pending),
  arms out. No new body pieces.
- _31 (1220x673): Gumball jumping, arms up, legs bent/tucked, mouth open.
  Cape Jones: jump pose — legs tucked (cut legs bent), arms up, torso
  bounce. Needs: jump leg tuck assembly (cut limbs can do it).
- _32 (498x285): Richard (pink, Gumball's dad) dancing on a couch,
  arms up, legs apart. Cape Jones: dance on a couch = seated/standing
  dance, same as _29/_31, no new pieces.
- _33: duplicate of _13, counted once in Batch 1, not again.

Batch 2 totals: 9 new files, ~70+ individual poses across the sheets.
Combined with Batch 1: 29 unique files, 20 single poses + ~70 sheet
poses = ~90 poses to study, all as movement/pose descriptions only.

## What I will NOT pull in, plainly
- No CN / Nickelodeon / Disney show files, rigs, or character art
  copied into the Cape Jones repo, and no "Giga leak" leaked material
  pulled in. I have not verified any such leak repo in this workspace,
  and a leak would not make a show's character art ours to ship.
- No Toon Boom show rigs copied. Toon Boom as a tool is a different
  thing from a show's rig file — if we use a tool, it will be on
  Cape Jones's own pieces, not on a show's character.
- No "250–300 tools" claim until inventoried. The tools I can verify
  here and will use first are the ones already in this workspace:
  slice_clean.py (clean cuts), Pack1 + cut limbs, assemble_tpose_default.py,
  and the locked v8 pieces. If a tool is needed beyond that, it will
  be named, checked, and added as its own step, not counted by guess.
- Blair Witch / other repos: not verified as Cape Jones sources in
  this turn, not pulled in on a name alone. If Mars names a specific
  file in a specific repo that is his own work, that file can be
  checked then.

## What I WILL do, in order, from these examples
1. Finish v8 repo lock first (uploading now, separate branch).
2. Push this log (descriptions only) in a separate animation PR.
3. Repose tests from v8 pieces only: A-pose, flex, dance groove,
   lounge, punch, jump, arms-crossed, arms-up — on 2s, holds as in
   Batch 1, using cut limbs + Pack1 hands.
4. Make only the missing pieces the poses actually need, one pack at
   a time, clean-cut sliced, shown to Mars before the next pack:
   cape swing/drape states, torso 3/4 + reclined + lying, foreshortened
   forearm, seated/crossed/lying legs, Pack4 eyes/visemes, and simple
   props (remote, mirror, comb) — all as Cape Jones originals.
