# Delivery Protocol — surviving chat message loss (Mars, 2026-10-31 22:54/22:57/22:58 CDT)

**Plain limit, first:** this does NOT fix the Muse app/client disappearing
messages itself. That is a client/runtime issue outside this work. What this
does is make delivery SURVIVE it: repo log + resend by topic + short
single-item messages, so a dropped chat message never means lost work.

**How any agent picks this up (read this, then do it):**
1. Read PROGRESS-STATUS-20261031.md. That is the current state. Do not use
   chat memory alone.
2. Deliver ONE item per short message, visual first, then 2-3 lines of
   numbers, then approval 0/1. Never a big batch in one message.
3. Give every delivery a topic ID (DELIVERY-001, -002, ...) and log it in
   PROGRESS-STATUS append-only log, with folder path + file version.
4. If Mars says "resend X", "that message disappeared", or names a topic,
   resend ONLY that topic, same file version, no rebuild, unless he ordered
   a new version. That resend is idempotent — same ID, same file, no duplicate
   approval counted twice.
5. If Mars approves or corrects via ANY channel (chat, repo status file edit,
   or an external AI showing him the repo and relaying his words), APPEND
   that approval/correction to PROGRESS-STATUS with date, time, channel, and
   verbatim words. An external AI cannot write to this repo on its own
   unless Mars gives it repo access — in that case it opens a PR, or Mars
   relays the words into chat. Do NOT claim an external AI auto-writes here.
6. Never claim landed, approved, or fixed until the evidence is in the repo
   (PR + merge SHA + size+SHA on main) or Mars said the approval words.

## 5 industry-standard methods — RUN, with proof

| # | Method (actual standard, not a buzzword) | How it runs here | Proof |
|---|---|---|---|
| I1 | Append-only event log / Write-Ahead Log (WAL) — database/event-sourcing practice: new facts append, old facts never edited | PROGRESS-STATUS append-only log section, new entries at bottom only | This file + PROGRESS-STATUS log entries dated 2026-10-31 22:54/22:57/22:58 CDT |
| I2 | Repo as source of truth / GitOps — the repo, not chat, is the deployable state | Status file + per-folder reports + builders landed in mhvnsnt/cape-jones, PR-only, verified on main | PRs #290-#295 merged; batch G report appended on merge (see LANDING-REPORT-20261031.md) |
| I3 | Idempotent resend / idempotency keys — at-least-once delivery, same key = same result, no double-count (payments/APIs use this) | Every delivery has a topic ID (DELIVERY-001...). Resend = same ID + same file version. Approvals counted once per ID | DELIVERY-003 (serve right5 no-crop fix) was resent as one item, not rebuilt, same 314,481 centre |
| I4 | Single-item chunking / short-message chunking — SMS/push chunking: one item per message, visual first | Protocol rule 2 above; parent chat practice since 2026-10-31 21:04 CDT: work first, short text | This protocol doc itself is one item; status file is the long record, chat messages stay short |
| I5 | ACK/NACK delivery receipts — TCP ACK / read-receipt practice: receiver ACKs, sender resends on NACK or silence | Mars replying "stayed", "approved", "resend X", or a correction = ACK/NACK. Agent logs it in PROGRESS-STATUS. Silence after a delivery = not an approval, it is an open ACK | Approval log in PROGRESS-STATUS: PAH GO cleaned APPROVED 100% 2026-10-31 22:24 CDT, logged as ACK |

## 5 experimental methods — RUN where stated, MAPPING where stated

| # | Method | Status | Proof / exact reason if mapping |
|---|---|---|---|
| X1 | Multi-channel fallback — chat + repo status + external-AI repo reading, any channel can carry the same delivery | RUN (channels documented + status file in repo) | Chat channel: this protocol. Repo channel: PROGRESS-STATUS on main after batch G merges. External-AI channel: README-EXTERNAL-AI-20261031.md tells an external reader exactly where to look. Write-back from external AI is MAPPING: it needs Mars-granted repo access or Mars relaying words into chat |
| X2 | Numbered sequence + gap detection — message sequence numbers, a missing number = a gap to resend (transport-layer sequencing) | RUN (in the status log) | Deliveries numbered DELIVERY-001... in PROGRESS-STATUS. A gap (e.g. a delivery Mars never saw) is found by comparing his ACKs to the numbered list, then resent by number |
| X3 | Visual-first + text-fallback — visual carries the work, text carries the numbers, if one drops the other path still exists in repo | RUN (partial) | Every delivery folder holds both the visual (GIF/PNG) AND a text report/JSON with numbers. If chat drops the visual, the repo path in PROGRESS-STATUS still points to the same visual. Full text-fallback for a dropped visual in chat alone is MAPPING: chat cannot re-show a visual Mars never received except by resending it |
| X4 | Status-file polling / heartbeat — receiver polls a known status URL/file for new sequence numbers | RUN as file, MAPPING as polling | File exists and updates with each delivery (heartbeat = new log entry). Automated polling by an external AI is MAPPING: no cron/poller for an external AI is set up here; Mars or his external AI checks the repo manually until he orders a poller |
| X5 | Redundant duplicate delivery with dedup — send the same item on two paths, receiver dedups by ID (redundancy + dedup, like dual-path networking) | RUN | Same delivery exists on two paths with the same ID: chat message AND repo folder + status entry. Receiver dedups by DELIVERY-ID, so a duplicate resend is not counted as a new approval or a new version |

## Multi-channel feedback — how it lands

- Chat -> status file: agent appends Mars's chat approval/correction, verbatim, dated.
- Repo status file -> chat: agent reads PROGRESS-STATUS before every delivery,
  so a correction already in the file is never re-asked or re-built wrong.
- External AI (ChatGPT or similar) -> Mars -> status file: external AI reads
  README-EXTERNAL-AI-20261031.md + PROGRESS-STATUS + per-folder reports,
  shows Mars what is done/approved/running/owed, Mars approves/corrects,
  agent (or Mars, via PR) appends that to PROGRESS-STATUS. No channel is
  chat-only. No approval lives only in chat memory.

## What NOT to do

- Do NOT send a big batch message and hope it stays up. One item, short.
- Do NOT claim the app bug is fixed. It is not. Delivery survives it; the
  app bug itself is outside this protocol.
- Do NOT count a resend as a new approval. Same ID = same delivery.
- Do NOT rewrite PROGRESS-STATUS history. Append only.
- Do NOT push a verbatim chat transcript to a public repo without Mars's
  explicit yes (private details risk) — status summaries, not transcripts.
