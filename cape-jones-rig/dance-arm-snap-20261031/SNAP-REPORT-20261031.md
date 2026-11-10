# ARM-FRONT-SNAP — Corrected Dance Rebuild (Mars, 2026-10-31 17:58 CDT)

## What was built
Corrected dance (63 frames) rebuilt with the ARM-FRONT-SNAP rule from
../ARM-FRONT-SNAP-RULE.md. Old correction folder untouched; all new
work in dance-arm-snap-20261031/.

## Diagnosis (measured, not guessed)
Old builder order: upper arms BEFORE torso, forearms AFTER torso.
So on a crossed frame the forearm was already in front, but the upper
arm segment shoulder->elbow was hidden BEHIND the chest. The arm read
as a forearm floating at the pec line with its shoulder connection
eaten. The eaten piece was the UPPER arm. Snapping only the forearm
would change nothing; the whole chain (upper + lower + elbow cap)
moves above the torso on snapped frames, and the head stays above
the arm (chest < arm < head).

## Snap gate (measured per frame, per side)
Forearm alpha vs torso alpha overlap at 1100x1500, threshold >1000 px.
Out-to-side frames measure 0-268 px; crossed frames 1538-8969 px.
Upper-arm overlap is NOT the test (always 4000+ px at the shoulder
attachment, crossed or not).

## Counts — 63/63 frames rebuilt
- Frames with at least one snapped side: **21/63 = 33%**
  11, 13, 15, 17, 62, 64, 66, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91,
  93, 99, 101, 103
- Frames unchanged (no snap): **42/63 = 67%**
- Side-snaps total: **30** — L 10 frames (11, 13, 15, 17, 62, 64, 66,
  99, 101, 103), R 20 frames (11, 13, 15, 17, 64, 66, 73, 75, 77, 79,
  81, 83, 85, 87, 89, 91, 93, 99, 101, 103)
- Keyframes: f015 snapped both sides (L 7963 px, R 7416 px);
  f028 unchanged control (0/0 px, arms out to the side);
  f083 snapped R only (2145 px).
- Note on Mars's frame numbering: he described top-row frames 1-2 as
  out and frame 3 as in front. In the contact sheet the crossed
  keyframe is the SECOND (f015, Stride B) and the third (f028, Groove
  A) is out to the side. The rule as built follows the MEASURED
  crossing (f015 snapped, f028 not), which matches his intent — arms
  in front snap, arms out do not — even if his numbering was off by
  one. If he meant a different frame, the audit CSV names every
  frame, so the exact frame can be re-checked, not re-guessed.

## Honest trade-off, not hidden
The snapped upper-arm pieces are BULKY. At f015 the snapped upper
arms cover a large part of the pecs; at f083 the snapped R upper arm
covers the right pec edge. The arm chain is now continuous (that was
the ask), but pec coverage is the price: a front arm, drawn whole,
necessarily covers the chest it crosses. Mars is the judge of whether
that read is "arm in front, correct" or "too much pec covered." If he
rejects the bulk, the next variant to try is NOT a return to the old
order — it is a narrower upper-arm piece or a clipped snap (upper arm
only where it overlaps the forearm's path), and that variant is owed
only if he asks for it, not built silently here.

## Files (new dated folder, old correction untouched)
- frames/dance-arm-snap-f001..f109.png (63 frames)
- dance-arm-snap-20261031.gif (63 frames, 80 ms, 275x375)
- dance-arm-snap-contact-20261031.png (keyframes 1,15,28,42,56,69,83,97)
- dance-arm-snap-before-after-20261031.png (top corrected, bottom
  snapped; columns f015 snapped, f028 unchanged, f083 snapped R)
- dance-arm-snap-chest-crops-f015/f083-20261031.png (left corrected,
  right snapped, chest zone enlarged)
- arm-snap-audit-20261031.csv (all 63 frames, side, overlap px, snap)
- per-frame-audit-20261031.csv (knee-feet rule, unchanged logic)
- build_arm_snap.py (snap-aware builder, gate in its header)
- SNAP-REPORT-20261031.md (this file)

## Still owed
- Mars approval of the snapped dance: 0/1.
- No repo push made here (parent PR route).
- The rule itself is logged as standing in ../ARM-FRONT-SNAP-RULE.md
  and applies going forward to every pose/clip/shot, not just dance.
