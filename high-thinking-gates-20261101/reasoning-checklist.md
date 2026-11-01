# Reasoning Checklist — Gate 1 of 5: High-Thinking Gates (Cape Jones, 2026-11-01)

Run BEFORE any rig build. No build starts until every box below is checked
and the JSON log exists. If any check fails, STOP — do not build a guessed
version (see choice-first-gate.md).

## 1. Inventory source pieces
- [ ] List every source piece the build needs (part name, source file, path).
- [ ] Every piece comes from an approved source: a Mars-approved version,
      a locked version, or a file already landed in the repo.
- [ ] No piece is listed from memory, from a description alone, or from a
      filename that has not been opened and inspected.

## 2. Verify source exists
- [ ] Each listed source file exists on disc (or on main, by path) at the
      moment of the check — not "existed yesterday".
- [ ] Each source file opens and is the expected type (image / rig / spec).
- [ ] Record file size (bytes) and SHA-256 for each source in the JSON log.

## 3. No-crop check (whole piece only)
- [ ] Every piece is used WHOLE — no square/rectangular crop, no trimming
      of arms, hands, biceps, or any body part to force a fit.
- [ ] Any resize keeps the whole piece intact; a piece that does not fit
      whole is flagged, not cropped.
- [ ] Cropping versions previously rejected by Mars (pipeline-auto literal /
      real-rig fist-split, hand resize, Arm 2 bicep crop) are never reused
      as a base.

## 4. No hand-draw check
- [ ] No piece is hand-drawn, redrawn, or traced from scratch for this build.
- [ ] Any piece that would need hand-drawing is flagged `hand_drawn: true`
      and the build stops (script exits non-zero).

## 5. No guessed label check
- [ ] Every piece label matches its source (part name, version, side).
- [ ] Labels are debug-only (see LABELS-ARE-DEBUG-ONLY): a label never
      becomes part of the shipped art.
- [ ] Any label that is guessed, inferred, or unverified is flagged
      `guessed: true` and the build stops.

## 6. Record the decision
- [ ] Run `check_reasoning.py` with a manifest; it writes a JSON log
      (`reasoning-log-<date>.json`) with: build name, date, each piece,
      source path, size, SHA-256, flags, and PASS/FAIL.
- [ ] A FAIL log blocks the build. A PASS log is kept with the build
      artifacts and referenced in the landing PR.
- [ ] Never overwrite a prior log: new date/time in the filename, append
      only (checkpoint rule).

## Manifest format (input to check_reasoning.py)
```json
{
  "build": "sit-idle-v7",
  "pieces": [
    {"part": "neck", "source": "path/to/neck-v4.png",
     "hand_drawn": false, "guessed": false}
  ]
}
```

## Fail = stop
Missing source, hand-drawn flag, or guessed flag → script exits non-zero,
build does not start, Mars is asked (choice-first gate) instead of being
shown a guessed build.
