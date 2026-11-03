# Memory backup — mirrored agent memory

**What this is.** A mirrored copy of the agent's live standing files, kept in two GitHub repos so the memory can never be lost again:

| Live file (agent VM) | Mirror copy (this folder) |
|---|---|
| `~/MEMORY.md` | `memory-backup/MEMORY.md` |
| `~/AGENTS.md` | `memory-backup/AGENTS.md` |
| `~/SOUL.md` | `memory-backup/SOUL.md` |

**Where the mirrors live (both hold identical copies):**
- `mhvnsnt/agent-memory` → `memory-backup/` (private — the canonical restore source)
- `mhvnsnt/cape-jones` → `memory-backup/` (second mirror)

**Why.** On 2026-11-02 at 05:38 CST, `~/MEMORY.md` was found truncated to 0 bytes. It was rebuilt the same day from the memory search index, verbatim fragments, and the daily logs. The owner (Real) then ordered the memory mirrored into these repos permanently (2026-11-02), so a wipe can never take it again.

**How it stays current.** `~/workspace/agent-ops/memory-backup-sync/sync-memory-backup.sh` hashes the three live files; when any hash changes it lands the new copies in both repos (agent-memory: direct commit to `main`; cape-jones: branch → PR → merge, additions/updates to `memory-backup/` only). It runs daily via the cron job **`memory-backup-sync-daily`** ("Memory backup sync (daily)") and can be run by hand any time. Each sync refreshes `memory-backup/SYNC-STATE.md` with the source md5s and the sync time. Sync state and logs: `~/workspace/agent-ops/memory-backup-sync/state.env` and `sync.log`. A copy of the script also lives in `mhvnsnt/agent-memory` at `tools/sync-memory-backup.sh`.

**Restore procedure — if the local memory is ever lost or zeroed:**
1. Get the mirror: `gh repo clone mhvnsnt/agent-memory` (or use the identical copy in `mhvnsnt/cape-jones` under `memory-backup/`).
2. Copy `memory-backup/MEMORY.md` → `~/MEMORY.md`, `memory-backup/AGENTS.md` → `~/AGENTS.md`, `memory-backup/SOUL.md` → `~/SOUL.md`.
3. Verify: `md5sum ~/MEMORY.md ~/AGENTS.md ~/SOUL.md` must match the md5s recorded in `memory-backup/SYNC-STATE.md`.
4. Run `bash ~/workspace/agent-ops/memory-backup-sync/sync-memory-backup.sh` — it should report no change, confirming the restore is exact.
