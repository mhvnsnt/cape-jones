# Episode 1 "Immortal Qombat" — fight choreography (Track B)

Locked decisions (owner, 2026-10-24): stage = Jungle Outpost (Tekken 7).
Fight outcome = PANTERA WINS, comeback (down to one hit from death),
then his chain grapple (King-style chain-throw sequence; in-universe
simply Pantera's chain grapple) finishes Cape. Cape's Scene 6 line =
"I don't even want to be here." (owner verbatim). In-universe show name
is IMMORTAL QOMBAT, never "Western Heart". Fighters fly INTO the TV,
never out of it.

## Paired timeline (30fps, scene frames; proof camera: side view, +X)

| Scene frames | Cape | Pantera | Beat |
| --- | --- | --- | --- |
| 0-59 | stance (108f clip trimmed to 0-59) | stance loop (0-74, 75-149, 150-160 partial) | Square off |
| 60-81 | strike_light spin (22f) — ends turned 180 deg AWAY | stance loop | Cape strikes first, spins, ends with his back turned |
| 82-134 | stance recovery (still turned away, vulnerable) | stance loop + approach: object location +0.60 m toward Cape, f110-135 | Pantera closes while Cape is turned away |
| 135-155 | hit (stagger, 21f) | arrived; blow implied by approach + Cape stagger (Pantera has no strike clip — see gaps) | Pantera's answer lands; Cape reels |
| 156-160 | stance (reeling recovery) | stance | Beat before the finish |
| 161-195 | — | grab (35f): crouch-in, lift (hips ~1.46 m, ~1 m forward), slam, ends on the ground | The chain grapple |
| 170-184 | hit_launch frames 0-14 ONLY + follow offset keys (see below) | (grab in progress) | Cape is carried through the lift |
| 186-225 | ko (40f) | — | Cape down |
| 196-235 | (ko continues) | stance frames 30-69 (STANDING guard — NOT frame 0, which is a deep crouch) as win stand-in | Pantera standing over Cape |

## Contact and sync notes (measured, not assumed)

- Pantera's grab root motion (measured stood-up): crouch (hips z -0.09),
  lift to z 1.46 at grab f12-17 with ~1 m +Y travel, slam to z ~0.15-0.20
  at f24, ends on the ground ~1 m forward. The grab travels TOWARD Cape
  (Pantera faces +Y, Cape is at +Y) and carries Pantera INTO and PAST
  Cape's starting position.
- Cape's launch clip does NOT follow the grab on its own: its root stays
  near its start point, pops up slightly, and frames 15+ drive the
  pelvis below ground (measured: pelvis z -0.30 at launch f24). The
  choreography therefore (a) uses launch frames 0-14 only, and (b) adds
  scene-level Cape armature location keys during the grab (f169: base;
  f178: +0.30 m toward Pantera, +0.25 m up — tracks the lift; f186:
  +0.45 m, -0.05 m — the slam point; held through f235). These offsets
  are documented choreography aids, NOT source-motion edits.
- Spacing at grab start: ~0.5 m (Cape y +0.55, Pantera y +0.05 after the
  approach), i.e. grappling range. Cape's heavy strike root travel
  (scaled ~0.36 m) + arm reach visually connects at the exchange; the
  spin strike is deliberately the beat BEFORE the grab (Cape ends turned
  away, which is why Pantera can grab him).
- v1 failure (fixed in v2, kept here so it is not repeated): v1 ran
  Cape's full launch (0-24) with no follow offset. Mid-throw (scene
  f175) the two bodies tumbled separately with no contact, the launch
  tail drove Cape through the floor, and the win cut (f196) showed a
  tangled heap (Pantera stance frame 0 = deep crouch + Cape ko frame 0
  overlapping). v2 fixes all three: trimmed launch, follow offsets,
  win strip from standing stance frames 30-69.

## What the clips do NOT show (gaps, not hidden)

- Pantera has no strike clip: his blow at f135-155 is implied by the
  approach + Cape's stagger reaction. A real Pantera strike clip is on
  the T7 swap list.
- Pantera has no win-pose clip: the f196-235 stance is a stand-in
  (standing guard over the downed Cape), not a victory pose.
- Pantera has no hit-reaction/stagger clip: the comeback ("one hit from
  death") is conveyed by ORDER (Cape strikes first and Pantera keeps
  standing), not by a stagger animation.
- The grab ends with Pantera on the ground (suplex follow-through), not
  standing as winner. The edit bridges grab-end -> win stance; the grab
  clip alone must not be described as ending with Pantera standing.
- Fingers stay open during grabs (no finger channels in T3 sources).
- The full multi-stage chain (King-style chain sequence) is NOT in hand:
  only the single T3 grab is. The full chain is on the T7 swap list.
- Arena backdrop: the delivered Jungle Outpost GLB is 140 m wide, so at
  fight-camera distance (4.5 m) its dressing falls outside the frame
  and reads as void in Workbench. The paired proof therefore adds a
  neutral ground plane at arena ground level so foot/ground contact
  reads. An arena-composited beauty proof (arena dressing legible
  behind the fighters) is PENDING on the arena track's fight-scale
  framing pass — it is not faked here.
