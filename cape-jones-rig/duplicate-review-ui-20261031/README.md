# Duplicate Review UI — Cape Jones sheets

**NOTHING IS DELETED HERE.** This UI only records choices.
Nothing is deleted, moved, or renamed by this page. Deletion happens
ONLY later, after Mars approves the exact keep/delete list exported
from here, in a separate job.

## What it is

A single static HTML page (`index.html`) that lets Mars actually use
the duplicate/organization work:

- Go through duplicate groups, same art side by side
- Search (by source name), filter (folder, group size, decision state),
  sort (group number, size, first source name)
- Label each item (free-text label per item)
- Mark each item KEEP, DELETE CANDIDATE, or UNDECIDED
- Per-group helper: "Keep first, mark rest DELETE CANDIDATE"
  (with a confirm dialog; still only records candidates)
- Click a tile to enlarge it (modal preview)
- Export decisions as JSON or CSV (download buttons + live preview)
- Decisions auto-save in the browser (localStorage) so a refresh
  does not lose work; "Reset all decisions" clears them (confirm dialog)

## Data — real, never invented

Loaded from the verified manifests, embedded in `index.html` by
`build_data.py` (the page works as one static file, no server needed):

- `honest-defects-10-methods-20261031/measurements-10-methods-20261031.json`,
  M7_duplicates: **24 exact-MD5 groups, 59 items, 35 extra copies**,
  173 unique hashes / 208 plates checked.
- `transparent-plates-grok-full-sweep-20261031/conversion-manifest.json`
  (245 entries): alpha_frac / quality shown on each tile.
- Totals only from `sliced-68-unsliced-20261031/SLICING-MANIFEST-20261031.json`:
  3,818 sliced pieces (1,908 named, 1,910 MIXED).

Tile images are the real transparent plates, loaded by relative path
(`../transparent-plates-grok-full-sweep-20261031/plates/...`), so the
UI must land in the repo alongside that folder, at the same level.
All 59/59 plate files were verified to exist before delivery.

### Swapping in a newer data source

1. Replace `data/duplicate-groups.json` with the new export, same shape:
   `groups[]` with `group_id, method, size, suggested_canonical`,
   `items[]` with `source, plate, decision, label`.
2. Re-run `python3 build_data.py`. It re-embeds the JSON into `index.html`.
3. Never hand-edit group membership in the HTML.

The sibling duplicate-finding job (`duplicates-organize-20261031/`,
still running at UI build time) is the intended next data source.
Its folder was not touched by this job.

## Honest limits

- These 24 groups are **exact byte-identical files only** (MD5).
  Near-duplicates that are not byte-identical are NOT in this set.
  That is a separate, still-owed pass — not a claim that no
  near-duplicates exist.
- The walkthrough decisions shown in `contacts/` are EXAMPLES only.
  No real keep/delete decision has been recorded by Mars yet.
- The UI was verified by static checks + data checks in this session
  (placeholder replaced, all 24 groups / 59 items / 59 plates present,
  export shape checked). No browser screenshot tool was available in
  this VM session, so the contacts are layout proofs built from the
  same data and plate images the HTML loads — labelled as such on
  the images — not browser screenshots. Click-through in a browser
  is still owed before this is called browser-tested.
- The 4 full-frame props (FULL-FRAME-TEXTURE, not cut objects) and
  the 37 backgrounds are not duplicate groups and are not in this UI.

## Decision export format

JSON: `{version, exported_from, note, groups: [{group_id, method,
suggested_canonical, items: [{source, plate, decision, label}]}]}`

CSV: `group_id, method, suggested_canonical, source, plate, decision, label`
(one row per item).

A later landing/deletion job may act ONLY on a list Mars approves
exactly, in this shape. This UI alone authorises no deletion.

## Walkthrough — one group end to end (DG-01)

1. Open the page, search `2e9kj` — only DG-01 remains.
2. Three tiles side by side, visibly the same sheet:
   `fla-packs/dance-packs/dance-2e9kj.jpg`,
   `fla-packs/jojo-packs/recent-2e9kj.jpg`,
   `fla-packs/jojo-packs-2/recent-2e9kj.jpg`.
   This is the Grok drift pattern: the same sheet staged under three
   pack names.
3. Label each tile (e.g. "dance pack", "jojo pack", "jojo pack 2").
4. Mark one KEEP, the other two DELETE CANDIDATE (or use
   "Keep first, mark rest DELETE CANDIDATE").
5. Export JSON/CSV. That file is the candidate list Mars approves
   before any deletion job runs.

## Files

- `index.html` — the UI (static, single file)
- `index.template.html` — the UI template (`__DUPLICATE_GROUPS_JSON__`
  is replaced by `build_data.py`)
- `build_data.py` — regenerates `data/duplicate-groups.json` + `index.html`
- `data/duplicate-groups.json` — the swappable data source
- `contacts/walkthrough-group-DG-01-20261031.png` — DG-01 walkthrough
- `contacts/walkthrough-group-DG-23-20261031.png` — DG-23 (tpose-front-alt pair) walkthrough
- `contacts/ui-layout-proof-20261031.png` — UI layout proof (labelled, not a browser screenshot)

## Status

Approval 0/1 for the UI separately. No original touched, no deletions
executed, no repo push by this job.
