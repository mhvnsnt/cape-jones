# PICKS STILL OWED — 2026-10-31
Mars ordered 2026-10-31 23:54 CDT: show all picks still owed, explain them if not visual.
No pick is silently made here. Every pick below is approval 0/1 separately. No repo push by this job.
Approved items are NOT re-asked. See the end for items already resolved / waiting, not picks.

## HOW TO ANSWER
Say the pick number + the option letter, e.g. "Pick 1: B2", "Pick 3: 2.8x". One pick at a time is fine — you do not have to answer all 13 at once.

---

## PICK 1 — TEMPO: picture vs song (NOT visual — listen, then pick)
Song in repo: C major, 152 BPM. Picture visuals: ~107 BPM.
Final mixes exist at BOTH tempos, both −14.0 LUFS PASS (107 BPM 17.94s, true peak −2.29; 152 BPM 12.63s, true peak −2.89). Both are synthesised originals, NOT the repo song, NOT recorded voice. Dialogue stems are silence placeholders by design.

- **A — Picture follows song (152):** Re-time the visuals to ~9–10 frame beats. What changes: visual timing, cuts and movement pacing change to match the song. Song untouched.
- **B1 — Song follows picture by time-stretch (152 → 107):** Stretch the song to 107 BPM. What changes: song timing, with artefacts likely at 1.42× stretch. Needs your explicit approval, and you must hear it first — no silent stretching.
- **B2 — Song follows picture by re-perform (at 107):** Re-perform the song at 107 BPM. What changes: cleanest sound, costs a new performance. No stretch artefacts.
- **C — Neither moves:** Decouple. Song becomes a non-synced bed under the picture. What changes: the sync claim is dropped — picture and song no longer claim to be in sync.
Until you pick: no side is silently stretched. This is POST-EPISODE, not an episode blocker.
Approval 0/1.

## PICK 2 — QC RULING + CJ-26 RIM CORRECTION (NOT visual — a rule pick)
QC now: 27/30 PASS, 3/30 FAIL — CJ-05, CJ-06, CJ-26.
Key finding, plain: all three failures are UNVERIFIABLE, not measured hue mismatches. Spec hue = None for key and rim in all three, the rim rule has no achromatic (white/grey) case, and the dual-light exception applies to NONE of them.

- **R1 — Pass all 3 by a new achromatic clause → 30/30.** What changes: the rule gains a white/grey case. Does NOT make CJ-26 canon or final — DEMO-ONLY / SPEC-ONLY stands for CJ-26.
- **R2 — Pass CJ-05 + CJ-06, HOLD CJ-26 → 29/30.** What changes: two shots pass, CJ-26 stays held for a separate decision.
- **R3 — Fail stands, all 3 → 27/30.** What changes: nothing passes that is currently failing; the three stay flagged.
Under ANY ruling, one correction is still owed: CJ-26 rim field 255,255,255 vs notes 240,240,240 — that mismatch must be corrected to one value.
Approval 0/1 (ruling) + 0/1 (CJ-26 correction value, once you say which number is right).

## PICK 3 — SEATED SCALE: 2.8x vs 2.3x (VISUAL)

![Seated 2.8x vs 2.3x](sandbox://workspace/cape-jones-rig/picks-still-owed-20261031/contacts/pick-seated-2p8-vs-2p3-20261031.png)
Left: 2.8x lock-consistent. Right: 2.3x absolute. Source proofs: roomscale-eyes-20261031/room-proofs/seated-2p8-lock-consistent-portrait-20261031.png and seated-2p3-absolute-portrait-20261031.png.

- **2.8x — lock-consistent (3.0 − 0.2):** bbox height 1186. What changes: seated figure stays in the same scale family as the 3.0x standing room scale, so standing and seated figures in the same room read as the same size character. Taller in frame.
- **2.3x — absolute:** height 974. What changes: seated figure is smaller in frame, closer to its raw plate size. Breaks lock-consistency with 3.0x standing.
Both: feet anchor 1700, rug 0.624 PASS. CJ-23 is a lotus plate with no chair prop — a finished lounge-chair composite is still owed either way.
Approval 0/1.

## PICK 4 — ROOM SCALE 3.0x GENERAL CONFIRMATION (VISUAL, already locked FOR ROOM USE)
Room scale is ALREADY locked at 3.0x FOR ROOM USE (Mars, 20:56 CDT: "That's the only scale to use him in that room. Never any other scale."). 2.5x is superseded FOR ROOM USE. Standing 1140px, seated 1034px derived at room scale in the coordinator table.
What this pick actually asks: confirm 3.0x generally, beyond room shots, or keep the lock room-only and let other shots use their spec scale (~0.35 layout for non-room shots).
- **Confirm 3.0x generally:** 3.0x becomes the default everywhere it fits.
- **Keep room-only:** room shots stay 3.0x, other shots keep their own spec scales.
Approval 0/1 (general confirmation only — room-use lock is not re-asked).

## PICK 5 — JUMP-TO-SHIMMY: RE-KEY OR DROP (NOT visual — a build pick, the ONLY blocker to 9/9)
Rig successors: 8/9 built = 89%. The missing one is jump-to-shimmy.
Why it is blocked, plain: its v1 land key is a rendered clip frame with no builder config. Re-keying it changes the sequence — it is not a copy-paste fix.
- **Re-key:** You state the key sequence you want (what keys, in what order). What changes: a new jump-to-shimmy sequence is built from those keys, successors go to 9/9.
- **Drop:** The successor is dropped from the set. What changes: successors stay 8/9, the set is complete without it, no further work on that transition.
Approval 0/1 (re-key with your sequence, or drop).

## PICK 6 — GOLD V6: SEAM, RIM WIDTH, POWER NAME, RENAME? (VISUAL)
V6 is a STANDALONE opaque gold/cyan split. It replaces nothing. V5 stays V5, V6 is NOT a lighting level.

Seam:
![V6 seam 550 vs 650](sandbox://workspace/cape-jones-rig/picks-still-owed-20261031/contacts/pick-v6-seam-550-vs-650-20261031.png)
- **Seam x550:** split line at x=550 on the figure.
- **Seam x650:** split line at x=650, further to the viewer's right. What changes: how much of the figure reads gold (left) vs cyan (right).

Rim width (outer-only rim, interior black preserved 100%):
![V6 rim 6 vs 12 vs 20](sandbox://workspace/cape-jones-rig/picks-still-owed-20261031/contacts/pick-v6-rim-6-12-20-20261031.png)
- **Thin 6px / Medium 12px / Heavy 20px.** What changes: thickness of the outer rim only. Default width pick sets the V6 default; the other widths stay available as variants.

Power candidate (no canon power is named yet — the name is the pick):
- **DUAL-CHARGE / DUAL-AURA / SPLIT-OVERLAY.** What changes: only the name attached to V6 as a power, until a power is actually named in canon. No power is active by default.
- Power candidate contact: gold-split-rim-upgrade-20261031/v6-power-candidates-contact-20261031.png

Rename:
- **Rename the original file to the V6 filename? YES / NO.** YES: the original filename becomes the V6 file (old name gone, V6 is the file). NO: V6 stays a separate file, original stays as-is.
Approval 0/1 per sub-pick (seam, width, power name, rename) separately.

## PICK 7 — HERO-BLACK BETTER METHOD: YES / NO (VISUAL — you said you must see it first)
Sheet: 09-hero-shot-black. Black hero on a black background, so the cut edge shows blue/pink fringe at zoom. Shape is kept, background gone, usable, not perfect.
Trials (original sweep plate untouched, variants in honest-defects-10-methods-20261031/variants/):

![Hero M1 vs M2](sandbox://workspace/cape-jones-rig/picks-still-owed-20261031/contacts/pick-hero-M1-vs-M2-20261031.png)
Left: M1 decontaminate. Right: M2 erode 1px.

- **M1 — colour decontamination / spill suppression:** fringe_edge 275 (−77% from baseline 1,190), fringe_all 7,005, alpha UNCHANGED 520,910. Best clean trial. Honest note: at contact scale M1 looks near-identical to baseline — the reduction is numeric (saturated edge pixels), not a dramatic visible redraw.
- **M2 — alpha erosion 1px (matte choke):** fringe_edge 250 (−79%), fringe_all 6,807, alpha 511,199 (−9,711, figure shrinks 1px). Best number, costs size.
- **M3 feather — REJECTED** (fringe +302%, worse). **M4 closing+fill — no change.** **M5 decon+erode — fringe 419, worse than M2 alone.**
- **NO — do not apply a better method:** keep the original sweep plate as-is, fringe and all.
Hero-black is NOT claimed fixed until you see it and say so — this pick is that yes/no. Approval 0/1 (M1 / M2 / NO).

## PICK 8 — DUPLICATE KEEP / DELETE, PER GROUP (VISUAL LIST — LOG ONLY, NO DELETIONS NOW)
Mars order 23:50 CDT: NO MORE DELETIONS at the moment. Duplicates stay LOGGED only. The 3 files already deleted (DG-01 ×2, DG-23 ×1, PR #296, branch only, NOT on main) are done — nothing else is deleted.
Organized list, upgraded (duplicates-upgrade-true-vs-near-20261031):
- Old strict groups: 498 groups, 1,420 members.
- Upgraded TRUE: 474 subgroups, 975 files (68.7%). NEAR-DUPLICATES (similar row/pattern, different detail): 440 files (31.0%). OTHER (old merge wrong, split out): 5 files (0.4%).
- Groups fully true: 295/498 (59.2%). Groups containing near files: 201/498 (40.4%).
- Do NOT quote 1,420 as true duplicates — 1,420 is the old "similar" count only.
- Keep/delete suggestions in the index are SUGGESTIONS ONLY (keep = highest resolution, then largest bytes per group). You pick per group, in the duplicate-review UI (v2 landed, PR #297, verified 10/10 on main; tiles broken on main until G1 merges).

![Largest duplicate groups](sandbox://workspace/cape-jones-rig/duplicates-organize-20261031/contacts/duplicate-groups-largest-20261031.png)
![True vs near](sandbox://workspace/cape-jones-rig/duplicates-upgrade-true-vs-near-20261031/contacts/true-vs-near-contact-20261031.png)
![Cross-category groups](sandbox://workspace/cape-jones-rig/duplicates-organize-20261031/contacts/duplicate-groups-cross-category-20261031.png)

What a keep/delete pick changes: which copy of the same art stays canonical, which copies are candidates for a LATER deletion job — only after you approve the exact list. This pick does not delete anything by itself.
Approval 0/1 per group (in the UI), not one blanket approval.

## PICK 9 — JOJO DREAM, DUAL-LIGHT, DEVICE SCALE, PARTS EXCEPTIONS (VISUAL + LIST)

### 9a. JoJo DREAM: A white vs B gold (VISUAL)
![DREAM A/B + dual-light V3/V4](sandbox://workspace/cape-jones-rig/picks-still-owed-20261031/contacts/pick-dream-dual-20261031.png)
Top left: DREAM A. Top right: DREAM B. Bottom: dual-light V3 / V4.
- **A — suit WHITE:** cape FULL magenta-pink (255,60,180), helm turquoise, suit white.
- **B — suit GOLD:** cape FULL magenta-pink (255,60,180), helm turquoise, suit gold.
What changes: suit colour in the DREAM shift only. Cape and helm are the same in both.
Approval 0/1.

### 9b. Dual-light: V3 vs V4 (VISUAL, difference is subtle)
Same contact, bottom row.
- **V3 — gold inner, cyan outer:** gold rim on the inside edge, cyan on the outside.
- **V4 — cyan inner, gold outer:** swapped. What changes: which colour reads as the inner rim vs the outer rim in a dual-light shot.
Honest note: at thumbnail scale the two look near-identical; the swap is in the rim layers, clearest at full resolution on the figure edge.
Approval 0/1.

### 9c. Device scale: 148×65 vs ~100 wide (NOT visual as a pair — a size pick)
The handheld gag device (always in pocket in canon) in final shots.
- **Keep 148×65:** larger, reads clearer on screen.
- **~100 wide:** smaller, sits more naturally in hand/pocket, less dominant in frame.
What changes: on-screen size of the device only, not the device design. Source: device-prop-v2-20261031/device-in-final-shot-v2-20261031.png.
Approval 0/1.

### 9d. Parts exceptions, 6 (LIST — explain, not visual as a pair)
- **1A Eye_White_R:** keep + rename "shadow eye" vs discard. What changes: whether that eye piece stays in the library under a new name, or is dropped.
- **1B CLEAN legs spares:** keep spares vs drop. What changes: whether spare clean leg pieces stay available, or are removed from the set.
- **1C Hand sides:** largely superseded by the per-hand flip approvals (7/7 approved) — confirm whether anything is still owed here, or close it as superseded.
- **1D Face_Angry:** combined vs split. What changes: whether the angry face stays as one combined piece, or is split into separate pieces.
- **1E Thin pieces:** accept vs redraw. What changes: whether thin pieces are accepted as-is, or redrawn thicker.
- **1F Forearm:** build Arm2 forearm vs Arm1-only. What changes: whether a second-arm forearm piece is built, or the set stays Arm1-only.
Approval 0/1 per exception (1A–1F separately).

## PICK 10 — DIALOGUE FILL, POST-EPISODE (NOT a pick to force now — explanation)
Space Ghost workflow: episodes FIRST, fully built; then Mars fills dialogue where needed; then audio pass + QC on dialogue. Dialogue / song-tempo / dialogue-QC are NOT episode blockers.
- Lines filled: 0/30 by design. Dialogue slots templated 30/30, lines filled 0/30.
- First: CJ-26 / CJ-27.
- After you fill: audio pass to −14 LUFS, then post-episode QC on the dialogue.
What changes when you fill: the episode gets its spoken lines, then the audio pass and QC can run on real dialogue instead of silence placeholders. No pick is needed now — this is waiting on your fill step, in your own time.
Approval: N/A until filled; then 0/1 for the filled dialogue pass.

## RESOLVED / WAITING — NOT PICKS, DO NOT RE-ASK
- **11. Bonyu vs Ginyu — RESOLVED by Mars 23:54 CDT: he meant GINYU.** Recorded. Ginyu Force core team is five; Bonyu is the documented 6th/former member, not the team Mars meant. Do not ask again.
- **12. Canonical room pictures — WAITING ON MARS, he said 23:54 CDT he will get them to us.** Batch-KKGuh is NOT canonical, placeholder only. Do not chase, do not guess a room. When the pictures arrive, re-measure and re-lock.
- **13. Toon Boom install — ON OUR SIDE, per Mars 23:54 CDT: do it on Muse's browser / Windows / Mac install, NOT on Mars's PC.** A separate install job is the route; Mars is not asked to install. Trial start is still NOT confirmed on pages alone, Windows install still owed, reminders armed day-11 Wed 2026-11-11 09:07 CST and day-13 Fri 2026-11-13 09:07 CST (end date NOT confirmed).
- **Messenger — SAVED, NOT SENT, per Mars 23:54 CDT.** Logged in repo at cape-jones-rig/MESSENGER-SEND-FUTURE-20261031.md: send on Facebook Messenger, to Real M Heavensent — spelled H-E-A-V-E-N-S-E-N-T (NOT "Heavenson", NOT "heaven son"). 9 JoJo v3 items in order: tension, power, uncertainty, dream, dread, resolve, atmosphere, opposition, overview. Rule before sending: preview the 9 to Mars first, then explicit confirmation, then send in order. Never show raw FBIDs. Do NOT send now.

## SHOTS NOT APPROVED — FOR REFERENCE (part of the parent's 23:54 order, shown here so the picks pack is complete)
Shots Mars-approved: 0/30 = 0%. Proof-built: 30/30. Per-shot axes approved: 0/120, built 120/120.
Existing finals contact: shots-endtoend-20261031/contact-finals-20261031.png (finals in shots-endtoend-20261031/finals/, CJ-01–CJ-30). Grounded 25/30, airborne 5/30 (CJ-12 hover 120, CJ-13 soar 170, CJ-14 dive 150, CJ-15 forward 140, CJ-21 takeoff 100). These shots are NOT approved by this picks pack — each shot needs its own 0/1 when Mars sees it.

## SOURCES USED FOR THE VISUALS IN THIS PACK
- Seated: roomscale-eyes-20261031/room-proofs/
- V6: gold-split-rim-upgrade-20261031/
- DREAM: jojo-shift-variation-20261031/ — DREAM A white, DREAM B gold, helm turquoise, cape full magenta-pink (255,60,180)
- Dual-light: dual-light-variants-20261031/ — V3 gold-inner/cyan-outer, V4 cyan-inner/gold-outer
- Hero-black: honest-defects-10-methods-20261031/variants/ + contacts/
- Duplicates: duplicates-organize-20261031/contacts/ + duplicates-upgrade-true-vs-near-20261031/contacts/
- Shots: shots-endtoend-20261031/contact-finals-20261031.png
- Tempo/QC: recorded-audio-qc-options-20261031/ + shots-endtoend production record
