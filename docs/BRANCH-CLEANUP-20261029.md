# Branch cleanup — 2026-10-29

Follow-up sweep after the 2026-10-24 cleanup (docs/BRANCH-CLEANUP-20261024.md). The EP01 / studio-speed / wired-tools / fullstack work landed via PRs #249–#262; every head branch was verified fully merged (GitHub compare ahead_by = 0) before deletion. All 17 non-main branches were deleted on 2026-10-29 after their tip SHAs were recorded below. Restore any branch with: gh api -X POST repos/mhvnsnt/cape-jones/git/refs -f ref=refs/heads/<name> -f sha=<recorded sha>.

Format: branch | tip sha at deletion | audit class

```
ep01-arena-recreation-preserved-20261024 | 7b871b801010ae4931c7b1455c29fa4cc6bf4303 | tip-ancestor-of-main
ep1-m4-cue-sheet | 9c4fcdfe9c04bb88a8d3c0f6baf501597210dcd7 | tip-ancestor-of-main
ep1-nosferatu-audio | c0f4411a9931af525c849e35592c0a698d6de7dc | tip-ancestor-of-main
ep1-nosferatu-score-id | 8d415b8b827fcb4f523461b8921db0dc24cfd5ab | tip-ancestor-of-main
ep1-pantera-voice | ed615d1c42a29e3ccfcd2c6559ccf8ec872f4d21 | tip-ancestor-of-main
ep1-render-pipeline | 328da6e8521294cb6c7a3fdd5cc7fd58756d3f83 | tip-ancestor-of-main
ep01-script-header-approved-20261024 | ebe3b18b6816bc320d4207df2757260210fe268e | tip-ancestor-of-main
ep1-script-pantera-voice-correction | eaca3c6cf2ac4d020eb522a83ac5e52512fbef35 | tip-ancestor-of-main
ep1-stack-research | 5f51753bb925c1eaf3d71b02df54374cdb8fc318 | tip-ancestor-of-main
ep01-stance-proof-20261024 | ba3777df0cb35f5c25e99fd60cc288d084b34e04 | tip-ancestor-of-main
ep1-title-card | fbfb49f3ce7e11cc65746c8f106ae709b59ce6f2 | tip-ancestor-of-main
fullstack-20261028 | 2627b681fd51f13e89f68047dde18c018b658132 | tip-ancestor-of-main
king-voice-acquisition-20261024 | 40f4f48baf23a67d3c7bef10cf328e4d44d40f24 | tip-ancestor-of-main
land/blend-guard-20261029 | 3cdef469c85f3ab115b5d6883d7df6bb32a01b01 | tip-ancestor-of-main
land/fullstack-sit-20261029 | 84745541893fd7385322baa8f0a3d3c2e47293ce | tip-ancestor-of-main
studio-speed-20261024 | 763ad1f49128b990a80217807183d8ca0020fbc2 | tip-ancestor-of-main
wired-tools-20261028 | 9973de482af81599c6ae0f0c256b74ffa0c18bff | tip-ancestor-of-main
```
