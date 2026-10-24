# Episode 1 — IMMORTAL QOMBAT title card (TRACK C)

Show-ready title card for **Scene 3 — TITLE CARD: IMMORTAL QOMBAT**
(est. 1:30–1:50 in `docs/story/EP01-IMMORTAL-QOMBAT-SHOOTING-SCRIPT.md`).
It plays full-frame on Cape's living-room TV during the channel-flip
sequence, on cue M2 (title sting), as Cape stops flipping and leans in.

## Files

- `immortal-qombat-title-card-4k.png` — still, 3840×2160, drop-in hold frame.
- `immortal-qombat-title-card-anim.mp4` — animated clip, 1920×1080,
  H.264, 30 fps, 6.0 s. The script's 20-second Scene 3 window is the
  scene, not the card's runtime: the 6 s clip covers the card beat and
  can be held/extended on its final frame to fill the scene as the edit
  requires.
- `make-title-card.py` — generator (Pillow + ffmpeg). Re-run to rebuild
  both assets from scratch; no hand-drawn frames.

## Design (matches the script beat)

- Title: **IMMORTAL QOMBAT** — in-universe show name only. The name
  "Western Heart" appears nowhere on the card.
- Kanji underneath: **不死** (fushi — "immortality; eternal life"),
  owner-confirmed 2026-10-24, in red with gold divider rules.
- The stylized **Q** of QOMBAT is red with a tail slash; in the animated
  clip the Q appears first and "opens" into the full word QOMBAT
  (OMBAT fades/slides in from the Q, 0.8–2.2 s), then the kanji fades in
  (2.2–3.2 s), then a hold to 6.0 s.
- Tone: dark and dramatic — near-black background, soft deep-red glow,
  bone-white title, gold IMMORTAL line. No characters depicted.
- No Tekken names appear in these in-universe-facing assets.

## Verification (viewed, not just rendered)

- Full-frame still viewed: title and kanji legible with strong contrast.
- Kanji crop viewed at full resolution: characters confirmed as 不死.
- TV-in-room mock viewed (card composited at TV-screen size on a dark
  wall): IMMORTAL, QOMBAT, and 不死 all still read clearly.
- Animation frames viewed at 1.5 s (Q opening) and 2.2 s (word complete):
  the Q-open reveal reads cleanly with no ghosting/overlap.
- Clip probed: 1920×1080, H.264, 30 fps, 6.000 s.

## Open for the owner

- Final design taste approval (colors, Q treatment, kanji size) — the
  card is show-ready as built, but the owner's eye is the last gate.
- Whether the edit wants the 6 s clip as-is, looped, or held longer
  inside the ~20 s Scene 3 window.
