# Mars-eye labelling workflow — plain words, step by step
## For Mars: you look, you name, you never touch code. For the agent: exact commands.

### What this is
The tools propose a label for every little piece. Most proposals are
GUESSES (in the 60-piece batch, only 2/60 were high-confidence). Your
eye is the deciding vote. This workflow makes your eye pass fast:
look at a contact sheet, correct the names in a plain-text file, hand
it back, and the corrections land.

### The rules that never change
- Labels live on the CONTACT SHEET ONLY. They are never baked into a
  clean scene piece (labels-are-debug-only rule).
- No file you have seen is ever overwritten. Corrections make NEW files.
- A tool proposal is never treated as a final label until you say
  "good" or you rename it yourself.

### Step 1 — Agent runs a batch (agent does this, not Mars)
```
cd ~/workspace/cape-jones-rig/fla-piece-labelling-top5-20261031
venv/bin/python label_pieces.py <piece1.png> <piece2.png> ... --out batch-<N>-20261031
```
This writes, in the batch folder:
- `proposals.json` — every proposal, with both tools' answers, confidence, band
- `contact-sheet-01-20261031.png`, `-02-...` — the sheets you look at
- `mars_corrections.txt` — the form you edit (see Step 2)

### Step 2 — Mars looks at the contact sheets (Mars does this)
Open the contact sheets in chat (they are embedded images, 1600px wide,
grey background, 8 pieces per sheet). For each piece, look at the
picture, NOT just the proposed name. The proposal line under each piece
reads: `piece_id -> proposed canonical name | BAND conf X agree=True/False`.
- If the name is right: leave that line alone, or change `keep` to `good`
  (good = you verified it — that counts as Mars-verified).
- If the name is wrong: change the name to the right one and change
  `keep` to `rename`.
- If the piece is junk / not a rig piece: change `keep` to `reject`.

### Step 3 — Mars edits the corrections file (plain text, no code)
Open `mars_corrections.txt`. It looks like this:
```
# lines starting with # are ignored. Do not edit the piece_id.
fla-front/Row1_1.png = capejones_cape_collar_front | keep
fla-front/Row1_20.png = capejones_belt_front | keep
```
Edit ONLY the right-hand side. Examples of correct edits:
```
fla-front/Row1_1.png = capejones_leg1_foot_front | rename
fla-front/Row1_20.png = capejones_belt_front | good
fla-front/Row1_16.png = capejones_unknown | reject
```
That is the whole format. One line per piece. `keep` = no change.
`rename` = use my new name. `reject` = throw it out. `good` = I checked
it and the proposal is right.

### Step 4 — Agent applies your corrections (agent does this)
```
venv/bin/python apply_corrections.py batch-<N>-20261031/proposals.json \
  batch-<N>-20261031/mars_corrections.txt batch-<N>-20261031/corrected.json
```
This prints a change report: what changed, from what to what, and
which piece_ids were unknown (skipped, never guessed). The corrected
labels live in `corrected.json`. The original `proposals.json` is
untouched, so your corrections are always auditable against the
original proposals.

### Step 5 — Next batch
Repeat Steps 1-4 on the next folder of unlabelled pieces. Your
corrections from earlier batches are NOT re-applied automatically to
new pieces (a new piece gets a fresh proposal) — but the canonical
names you chose become the vocabulary the tools propose from, because
Tool #3's schema is the same list.

### The current batch, ready for Mars's eye
Batch 60: `batch-60-20261031/` — 8 contact sheets, 60 pieces,
2 HIGH, 58 NEEDS-MARS-EYE, 0 reject. The `mars_corrections.txt` in
that folder is blank (all `keep`) and waiting for Mars's edits.
No correction has been applied to this batch yet — the test corrections
in this task's proof run were applied to a /tmp copy only, never to
the real batch file.
