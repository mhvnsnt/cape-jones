# 1. Status Honesty — State Machine (not free text)
States, in order, no skipping:
  STARTED -> RUNNING -> RECEIVED_NOT_VERIFIED -> VERIFIED -> CLOSED
  (any state may go to FAILED or BLOCKED, with reason recorded)
- A delegated subagent being spawned = STARTED, not done.
- A browser task being accepted = STARTED, not done.
- A PR being opened = STARTED for landing; landing is CLOSED only after
  merge SHA + size+SHA verified on main.
- A reply that only acknowledges = no state change at all.
Transition rule: moving to VERIFIED requires naming the evidence
(tool output id, file + bytes, or repo blob SHA + merge SHA).
