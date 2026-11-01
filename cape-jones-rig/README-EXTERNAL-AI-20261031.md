# Cape Jones — read me first (for an external AI showing Mars his work)

You are reading this repo with ONLY repo access. You do not have chat memory.
You can still show Mars exactly what is done, approved, running, and owed,
by reading these three files in order:

1. `PROGRESS-STATUS-20261031.md` — the source of truth. Approvals with
   dates, completed-not-yet-seen items with folder paths, running items,
   counted percentages, still-owed list, landing state.
2. `DELIVERY-PROTOCOL-20261031.md` — how deliveries survive chat loss:
   one item per short message, resend by topic ID, append-only log.
3. `FOLDER-INDEX-20261031.md` — every new folder, one line each, with
   approval status. Then open the per-folder report in any folder you show.

## Rules for showing work to Mars

- Show ONE item at a time, visual first (GIF/PNG in the folder), then 2-3
  lines of numbers, then approval status (approved / 0/1 / saved-good).
- Never call a file "approved" unless PROGRESS-STATUS says Mars approved it,
  with a date. Existence in the repo is NOT approval. Landing in the repo is
  NOT content approval.
- Never call a file "landed" unless LANDING-REPORT-20261031.md lists its
  PR number + merge SHA + size+SHA verification on main.
- If Mars approves or corrects something you show him, tell him to relay
  those exact words into chat, or open a PR appending them to
  PROGRESS-STATUS-20261031.md. You cannot write to this repo unless he
  gives you access, and you must not claim you did.
- Percentages always come with counts (e.g. 21/30 = 70%). Never a bare %.
- The app/client disappearing chat messages is a client issue, NOT fixed by
  this repo. This repo is the workaround: a persistent record he can check
  even when chat drops.

## Quick answers (full counts in PROGRESS-STATUS)

- Mars-approved finished shots: 0/30 = 0%. Storyboard poses: 21/30 = 70%.
- TV production core-blocker average: ~23%, counted estimate, not verified.
- Room scale lock: 3.0x ONLY. Space Ghost workflow: episodes first, then
  Mars fills dialogue, then audio pass + QC on dialogue.
- Latest approved: PAH GO cleaned movement APPROVED 100% (2026-10-31 22:24 CDT).
- Latest saved: Ghoul Shuffle V1 official, V2 saved-good (hands too far down,
  not enough up — next version in progress).
- Latest fix in progress at status-file time: serve hand up2 (314,479),
  no-crop fixed base, no erase, no notch.
