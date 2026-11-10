# Choice-First Gate — Gate 3 of 5: High-Thinking Gates (Cape Jones, 2026-11-01)

## Rule
Unknown piece = show options, STOP, do NOT build a guessed version.

If a part is ambiguous — two or more candidate sources, an unclear label, a
missing file, a part Mars has not approved — the agent does NOT pick one
silently, does NOT build a guessed version and then defend it, and does NOT
bury the ambiguity in a long report. It shows the options and waits.

This is the standing CLEAN-REPLY rule applied at build time: unknown piece
= show options and ask, never build guessed version + long defense.

## Procedure
1. STOP the build before that piece is assembled.
2. Present the options table below (one row per candidate), in chat, short.
3. Ask at most 1 question: which candidate (or "none — I will supply it").
4. Record Mars's choice verbatim in the reasoning log; only then resume.
5. If Mars supplies no choice, the piece stays OWED — it is never filled
   with a guess to keep the build moving.

## Template options table
| Part | Candidates | Source (file / version / repo path) | Why ambiguous |
|------|------------|--------------------------------------|---------------|
| e.g. neck | A: neck v4 (127x82, top 340) | rig-34 locked pose, APPROVED 2026-11-01 | — |
| e.g. neck | B: neck v2 (width ~126, top 350) | superseded by v4, kept for reference | v2 vs v4 width/top differ; v4 is official but the build spec named v2 |
| (add rows) | | | |

Columns:
- **Part**: the exact part name (neck, collar, Arm 2, etc.).
- **Candidates**: each candidate version, with its distinguishing numbers
  (size, position, colour) — numbers, not vibes.
- **Source**: file path / version / approval record for each candidate.
  A candidate with no source is not a candidate — it is a guess; drop it
  and say so.
- **Why ambiguous**: the exact conflict (two approvals, superseded vs
  current, missing file, unclear label, cropped vs whole).

## Banned moves
- Building all candidates and presenting them as if one were approved.
- Building one candidate, calling it "the" version, and asking Mars to
  correct it afterwards.
- Renaming a guessed build with an official version number (v-numbers
  only go up, and only for approved edits — see version-lock rule).
- Filling a missing piece with a hand-drawn stand-in "for now".
