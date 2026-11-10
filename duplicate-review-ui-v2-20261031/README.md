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

## V2 — 10 new features (20261031, improved version, v1 folder untouched)

Industry, all wired in index.html JS (node --check PASS):
- I1 Keyboard shortcuts — / focuses search, j/k scroll groups, K keep / D delete candidate / U undecided on focused tile, Ctrl+Z undo, ? help, Esc closes modal.
- I2 Bulk select & actions — tile checkboxes, per-group select-all, bulk KEEP / DELETE CANDIDATE / UNDECIDED / apply suggested labels; bulk bar appears only when something is selected.
- I3 Undo — 50-step history covering single, bulk, keep-first, label and import actions.
- I4 Indexed search — token index over group id, source, folder and label; search is instant and ANDs tokens.
- I5 Export validation — runs BEFORE download (not after); lists groups with >1 KEEP, groups with DELETEs but no KEEP, and all-undecided groups; export anyway requires confirm.

Experimental, all wired in index.html JS:
- X1 Near-duplicate preview — per tile, other groups sharing the same stripped stem (e.g. same sheet id under another pack name). Stem-based, NOT a pixel-perceptual hash — that distinction is stated in code.
- X2 Auto-label suggestions — rule-based from path (dance pack, jojo pack, jojo pack 2, lounge clean 3quarter, lounge pack, reference tpose); per-tile "Use suggestion" + bulk apply.
- X3 Confidence scoring — per-tile badge "Confidence 100% — exact MD5 match" (these 24 groups are exact byte-identical).
- X4 Pixel-diff compare — pick two tiles, Compare runs a canvas RGBA compare and reports differing pixels / %. Honest limit: canvas comparison requires same-origin serving (e.g. GitHub Pages); under file:// it may report tainted-canvas fallback instead of a number.
- X5 Progress persistence — progress bar (% decided), scroll-position restore on reload, import of a previously exported decision JSON.

Regeneration: index.template.html is now the v2 template (DATA placeholder). Running `python3 build_data.py` regenerates data/duplicate-groups.json + index.html as v2. `patch_v2.py` is the original v1->v2 patch, kept for provenance; it is not needed for regeneration.

Status: approval 0/1 for the improved UI separately. Landing ≠ approval. NO deletions — this UI only records keep/delete candidates.
