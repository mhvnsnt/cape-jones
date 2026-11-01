# 12 Principles of Animation — Cape Jones checklist (wired 2026-10-31)

Source, public industry standard: the 12 principles from Disney's *The Illusion of Life*
(Frank Thomas & Ollie Johnston). Listed here as methods only — no character art, names,
dialogue, or logos from any show are copied. Each principle has one concrete Cape Jones
example and one gate. Checklist status: wired as a checklist 12/12 = 100%.
Per-shot application: 0/30 shots checked against this list — that is a separate pass,
not claimed here.

| # | Principle | Cape Jones example | Gate for a shot |
|---|---|---|---|
| 1 | Squash & stretch | Punch impact: torso compresses on impact, then stretches on follow-through; flex biceps bulge on the tighten frame, relax on the anticipation frame | Impact frame shows a clear squash OR stretch vs the hold frame; volume (area) stays roughly constant |
| 2 | Anticipation | Flex anticipation frame (fists outward, before tightening) — the before-flex in-between, built 2026-10-31, is the anticipation for the final flex | Every big move has a readable anticipation frame before it; no move starts from rest with no wind-up |
| 3 | Staging | Punch Impact locked (-110 across-up): Arm 2 across the chest reads clearly against the torso, Arm 1 punching out reads against grey — one idea per shot | The action reads in silhouette at thumbnail size; if it does not, re-stage, do not add effects |
| 4 | Straight-ahead vs pose-to-pose | Pose-to-pose is the Cape Jones default (v7c joint-locked key poses: apose, punch, flex, dance, jump, seated); straight-ahead is used for secondary elements (cape sway, background life) | Key poses locked first, then breakdowns, then in-betweens — never the reverse |
| 5 | Follow-through & overlapping action | Cape keeps moving after the body stops (cape states: swinging, billowing); gauntlet/fist settle after the forearm stops | Cape and secondary pieces lag the body by 1–2 frames and settle after it, not with it |
| 6 | Slow in & slow out | Darwin dance retarget spec: keyframes on twos at a ~14-frame beat grid, with eased spacing into and out of the twist (32 keyframes, frames 43–97) | Spacing eases at both ends of a move; no linear spacing on a held-to-move transition |
| 7 | Arcs | Punch Arm 2 across the chest follows an arc, not a straight line; dance stride → groove → kick → split stance follows an arc through the body | Fist/foot paths are arcs in the exposure sheet; a straight path is flagged and re-timed |
| 8 | Secondary action | Space Jones idle loops (tapping foot, humming, sketching, swaying — Mochiichao-combine idle library, spec only) support the main action without stealing it | Secondary action is readable but never louder than the main action; if it competes, cut it |
| 9 | Timing | Punch impact: fast in (2–3 frames), hold on impact (flex-clip.json frame 7 hold 24 at 24fps is the precedent); dance beat grid ~14f @ 25fps (~107 BPM) | Timing is written on the exposure sheet in frames before any in-between is drawn |
| 10 | Exaggeration | Flex: elbows out wide, fists above head height, biceps at full bulge — pushed past realism, but the pose still reads as a double-bicep flex | Exaggeration serves the idea (strength, impact); a pushed pose that breaks the rig's joint lock is rejected |
| 11 | Solid drawing | v7c joint-locked rig: pivot = ball centre, parent trimmed at ball, child = whole-limb crop, single circular cap — volume and joint placement stay consistent across poses | A pose that breaks volume (detached fist, floating gauntlet) fails QC — see the 2026-10-31 flex wrist-seam failure, which was NOT shipped |
| 12 | Appeal | Clean plate rule: no red debug labels in final shots, rim follows key/LUT hue family, base palette is canon | Final shot has no debug labels, no hue-mismatched rim, and the character reads as Cape Jones, not as a reference |

## How to use this checklist
1. Pick the principle(s) the shot is ABOUT (usually 1–3, never all 12 at once).
2. Write them on the shot spec (see color-shot-spec-template.json / PIPELINE-TEMPLATE-20261031.md).
3. Check the gate after the key poses are built, before clean-up.
4. Log the check in TOOL-PASS-LOG.md with the shot's tool list.
