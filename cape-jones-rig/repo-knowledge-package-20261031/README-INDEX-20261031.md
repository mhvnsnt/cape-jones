# CAPE JONES — REPO KNOWLEDGE PACKAGE (2026-10-31)

**Purpose, in Mars's words (2026-10-31 ~18:43 CDT):** get all of that logged
and remembered, document all of this in the repo so anyone who works on it
will know, and so it can help going forward. Pull in industry-standard
stuff for all of this, keep wiring stuff up — anything not 100% wired,
get it 100% wired; anything not pulled in and wired, pull it in and wire
it 100%; make sure it lands.

**This package is push-ready, NOT pushed.** Landing is a separate step:
PR-only, additions only, 0 deletions, no force-push, merge gate, verify
on main by size + SHA after merge. Landing is NOT approval — see
`APPROVALS-LEDGER-20261031.md` for what Mars actually approved, and
`GAPS-OWED-20261031.md` for what is still 0/1.

**How to use this package (onboarding, 5 minutes):**
1. Read `MEMORY-NOTE-20261031.md` first — the durable facts, rules, and
   Mars-only decisions a future session must not re-ask or re-decide.
2. Read `CONSOLIDATED-RULES-20261031.md` before building ANY pose, shot,
   or effect — it is the standing rulebook, with original doc paths.
3. Check `APPROVALS-LEDGER-20261031.md` before re-showing or re-asking
   anything — approved items are shown as approved, never re-asked.
4. Check `GAPS-OWED-20261031.md` before claiming anything done — it
   carries counts + percentages, per Mars's percentage rule.
5. Run the pipeline gates in `WIRE100-SWEEP-20261031.md` before delivery:
   snap gate, knee-feet per-frame gate, gauntlet regression, arm
   alignment QC, colour tracking (input + on-screen + cause).

**Package contents:**
- `README-INDEX-20261031.md` — this index.
- `CONSOLIDATED-RULES-20261031.md` — 22 standing rules, consolidated
  without changing meaning, each with its original doc path.
- `APPROVALS-LEDGER-20261031.md` — 34 Mars approvals, each with date,
  file, and scope limit.
- `METHODS-INDEX-20261031.md` — 30 industry-standard methods pulled in,
  with source, wiring, and proof.
- `GAPS-OWED-20261031.md` — everything still 0/1, with counts +
  percentages.
- `MEMORY-NOTE-20261031.md` — concise memory update for a future session
  (a file in this package, NOT an edit to ~/MEMORY.md — the parent
  handles memory).
- `WIRE100-SWEEP-20261031.md` — wire-100 audit: what was newly wired in
  this sweep, what is still unwired, and why.
- `ADR-20261031.md` — architecture decision records (ADR method, see
  Methods Index #30) for the 8 biggest decisions, so a future worker
  knows WHY, not just what.
- `check_package.py` + `check_package_proof.json` — the package's own
  verification script and its run proof (true-final-flex md5 still
  03d282c8b1c56adf3fb43bb2dfe30b9a).
- `PUSH-HANDOFF-20261031.md` — exact folders/files for the landing
  agent, in order.

**Repo + workspace facts (verified 2026-10-31):**
- Cape Jones repo target: `mhvnsnt/cape-jones`. Canonical game repo
  (separate): `mhvnsnt/Mochiichao-Diamond-Version-2d-fresh-start`
  (PRIVATE, standalone since 2026-10-28). Old `...-public-fork` is
  reference/archive only, NEVER a push target. Proprietary
  Pokemon/Sonic material goes only to the private mirror
  `mhvnsnt/Mochiichao-Diamond-Version-2d--mirror`; ROMs/dumps go in NO
  repo; a dump Mars uploads stays private/local only.
- Rig root: `~/workspace/cape-jones-rig/` — 70 root-level .md docs,
  6,057 media files (png/jpg/gif/mp4), ~1.9 GB, counted 2026-10-31.
  Study clone `~/workspace/cape-jones-flying/` is READ-ONLY.
- Last verified main head at last landing check: cape-jones PR #289,
  merge 70acb397d52b6f3f8483bd35aaa08e08f606dedb. Re-verify head
  before pushing — do not trust a stale head.
- Production default: Blender 5.2.3 LTS
  (`~/workspace/tools-industry/blender-5.2.3-linux-x64/blender`).
  Blender 4.5.3 on disk is NOT the standard. Free stack:
  Tahoma2D 1.6.3, Krita 5.2.2, Pencil2D 0.6.6, Synfig 1.5.1, FFmpeg 8.1.2.

**Standing meta-rules (Mars, never override silently):**
- Percentage rule: every unfinished list gets a percentage + the count.
- Push-then-clean / disc-to-repo: verify on main by size+SHA after
  merge before any cleanup; never delete our work; checkpoint files
  never deleted; uncertain status = keep it and report it.
- Checkpoint / version-lock: every version its own dated file, never
  overwrite a version Mars saw; newest approved edit is current.
- Image-cache rule: a new version of an image always gets a new
  dated/versioned filename, never the same filename re-shown.
- Chat-viewable rule: non-viewable files (blend, json, md, html,
  scripts, docs, folders) go in the repo / plain text only, NEVER as
  chat file links; visuals embedded in chat; audio as links only.
  Muse remote-storage links are download links, not viewable links.
- Do-not-lie rule: never claim generated when a piece is vector-drawn
  / code-drawn / pulled / desaturated — call it exactly what it is.
  "Less hand-tooled" is banned — NOT hand-tooled AT ALL, except
  necessary fit / colour match.
- Likeness rule: NEVER put a character's name in a generation prompt.
  Reference image first, then visible attributes only.
- Show-building method: reference + transformation, not theft.
  Barred only: exact likeness shipped as-is, character literally,
  character name, script dialogue literally, brand image/logo.
  Character images are TRANSFORM-ONLY production reference.
- Free-way-around rule: if a roadblock appears, find a FREE way around
  it or reverse-engineer the METHOD and rebuild it free — never just
  present a roadblock. Methods only: not cracking, not bypassing a
  subscription/license, not copying proprietary code.
- Wire-it-up rule: installation alone is NOT wiring. A tool, preset,
  or gap item is wired only when it has a real viewed Cape Jones
  output (or a file verified by re-parse where the output is a file).

**Mars approval of this knowledge package: 0/1 — do NOT claim approved.**
