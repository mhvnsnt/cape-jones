# Learning log — duplicate pipeline, incremental, log-only

## Entry 2026-10-31 — TRUE vs NEAR upgrade (Mars, 23:50 CDT)
- Input: Mars's picks DG-01 + DG-23 (deleted on branch only, PR #296, NOT main).
  Both were exact-MD5 groups. Feedback applied: exact-MD5 weight UP.
- Input: Mars's defect report: same row / pattern row, actually two different
  items with slight differences. Feedback applied: row-name weight = 0
  (old D7 flawed for pieces), silhouette weight DOWN (outline alone is not identity).
- Change vs previous 498-group strict list:
  - Old similar count: 498 groups, 1,420 members (unchanged as a similarity count)
  - New TRUE count: 474 subgroups, 975 files (68.7% of old members)
  - New NEAR count: 440 files (31.0%)
  - New OTHER count: 5 files (0.4%)
  - Groups fully true: 295/498; groups with near: 201/498; groups with other: 3/498
- Rule learned: TRUE needs pixel identity, not pattern identity.
  Edge IoU is the discriminator that caught the near example
  (silhouette 0.995, edge 0.512).
- Next learning step (when Mars makes new picks): append the pick here,
  re-score only changed files, and update weights again. No deletion is
  triggered by any log entry. Deletions are STOPPED at Mars's order.
- Deletions in this job: 0.
