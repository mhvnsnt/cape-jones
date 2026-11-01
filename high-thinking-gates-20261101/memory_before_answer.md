# Conversation gate 3: Memory-before-answer check
Before answering any pick, approval, or "what is done" question:
- [ ] Search MEMORY.md and memory/ for the exact item (pick, approval, version, date)
- [ ] Copy the recorded decision verbatim from memory, do not re-derive it
- [ ] If memory says APPROVED / LOCKED / SUPERSEDED, say that, do not re-ask
- [ ] If memory is silent, say "not recorded" and ask, do not guess
Test: memory_check.py <keyword> — PASS if keyword found in MEMORY.md, else FAIL (not recorded).
