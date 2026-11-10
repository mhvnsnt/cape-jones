# The Watch — Sc076: two-shot crying escalation — both boys end up bawling on the floor

**Episode:** GB219 "The Watch" (Season 2) · **Scene:** Sc076 · **Frames:** 209 @ 25fps · **Source:** GB219WATCH_Sc076_Clean_V012_KR.fla / .swf

## Story / beat
A locked living-room two-shot that is one long grief crescendo. Gumball starts teary and wobbling (f1), breaks into an open-mouthed wail (f27), collapses to his knees sobbing (f131) and stays down. Darwin starts flat, answers late — mouth open at f53, tear streaks at f79, his own collapse at f183 — until the final frame (f209) has both boys on the floor, bawling at full stretch.

## Cast
- **Gumball** — GB200_GUMBALL_PUPPET_001 (553 + 256 kf entries) on the GB scene layer. Leads every beat.
- **Darwin** — GB200_DRW_ORIGINAL_PUPPET_v001 (696 kf) on the DARWIN scene layer. Answers every beat ~25–50 frames late.

## Construction
- One locked background: GB219_WATCH_SC076_LO_BG.jpg (bitmap plate, frames 0–209) — a tighter living-room framing than Sc075 (plaid couch left, door behind Darwin).
- Minimal stack: GB and DARWIN puppet layers over background, plus audio, framecounter, fieldguide and the 'layout mov' reference layer. No props, no camera moves — the scene is two puppets and time.
- The collapses are body-position changes on the same stock puppets (standing → kneeling → slumped sitting); no 'crying' puppet variants exist in the file.

## Techniques (tags + evidence)
- **dialogue-two-shot** — two characters held in one locked shot for 209 frames on separate scene layers (GB / DARWIN) over a single shared background, carried by alternating face-comp performances (manual, layers + sheet).
- **face-comp-driven** — face comps 4,699 kf vs body puppets 1,505 kf; GB_HEADCOMP alone holds 1,190 kf, the largest symbol in the file (auto).
- **layout-mov-reference** — scene carries a 'layout mov' reference-video layer (auto).
- Tears are face-comp elements: white tear streaks appear on the head comps from f79 and grow with the performance (sheet).

## What Cape Jones steals from this scene
- The escalation duet: two characters, one beat shape, offset clocks. Leader breaks first, foil resists, foil breaks harder — a complete emotional arc with two puppets and one background.
- Collapse by position, not by asset: dropping the same puppet to its knees sells the peak without any new drawings.
- A 209-frame scene with essentially five drawings' worth of staging: budget goes to face comps (4,699 kf), not sets.

## Media status
- Contact sheet: done (209 frames). Video: done, production audio muxed from the SWF sound asset. Frames rendered: 209/209.
- Render history: the first render process died silently at 147 frames; the relaunch needed three FFDec attempts under cross-batch contention (cached 147 → 185 → 204) before an attempt completed the full 209.

## Gaps / honesty
- None in the final media: full 209/209 frames rendered and verified. The render history above is kept because the contention pattern affects the whole batch.
