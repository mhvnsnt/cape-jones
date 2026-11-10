#!/bin/sh
# render_contact_sheets.sh — staged renders for the Gumball partials.
# Blocked at staging time (2026-11-02) by the sandbox write guard on rendered binaries;
# run when it lifts. Requires: JPEXS FFDec (ffdec) on PATH or $FFDEC, and the CN-Leaks-001
# SWFs staged in $WORK/swfs (range-fetch from the release asset; see dance-choreo tooling).
# Step 0 for binary FLAs with no companion SWF: open the FLA in Adobe Animate, publish SWF,
# then run the same export against the published SWF.
set -eu
WORK=${WORK:-$HOME/workspace/_gumball_templates_work}
OUT=${OUT:-$HOME/workspace/your_files/scene-templates}
FFDEC=${FFDEC:-ffdec}
mkdir -p "$OUT"

# gb209-banana-crashed-topshot — Gumball, Darwin — source: GB209_GB+DRW_CRASHED_TOP_SHOT_V002.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-crashed-topshot" "$WORK/swfs/GB209_GB+DRW_CRASHED_TOP_SHOT_V002.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-crashed-topshot"
# then: montage the exported frames into $OUT/sheet-gb209-banana-crashed-topshot.png (6-9 frames, labeled)

# gb209-banana-bilboquet-sc162 — Gumball, Darwin — source: GB209_BANANA_GB+D_BILBOQUET_SC162_FINAL.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-bilboquet-sc162" "$WORK/swfs/GB209_BANANA_GB+D_BILBOQUET_SC162_FINAL.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-bilboquet-sc162"
# then: montage the exported frames into $OUT/sheet-gb209-banana-bilboquet-sc162.png (6-9 frames, labeled)

# gb209-banana-gumball-hurt-facekick-sc155 — Gumball — source: GB200_GUMBALL_HURT_FACEKICK_SC155_FINAL.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-gumball-hurt-facekick-sc155" "$WORK/swfs/GB200_GUMBALL_HURT_FACEKICK_SC155_FINAL.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-gumball-hurt-facekick-sc155"
# then: montage the exported frames into $OUT/sheet-gb209-banana-gumball-hurt-facekick-sc155.png (6-9 frames, labeled)

# gb209-banana-gumball-hurt-floor-sc160 — Gumball — source: GB200_GUMBALL_HURT_FLOOR_SC160_FINAL.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-gumball-hurt-floor-sc160" "$WORK/swfs/GB200_GUMBALL_HURT_FLOOR_SC160_FINAL.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-gumball-hurt-floor-sc160"
# then: montage the exported frames into $OUT/sheet-gb209-banana-gumball-hurt-floor-sc160.png (6-9 frames, labeled)

# gb209-banana-gumball-hurt-himself-sc158 — Gumball — source: GB200_GUMBALL_HURT_HIMSELF_SC158_FINAL.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-gumball-hurt-himself-sc158" "$WORK/swfs/GB200_GUMBALL_HURT_HIMSELF_SC158_FINAL.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-gumball-hurt-himself-sc158"
# then: montage the exported frames into $OUT/sheet-gb209-banana-gumball-hurt-himself-sc158.png (6-9 frames, labeled)

# gb209-banana-darwin-hurt-backkick-sc159 — Darwin — source: GB200_DARWIN_HURT_BACK_KICK_SC159_FINAL.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-darwin-hurt-backkick-sc159" "$WORK/swfs/GB200_DARWIN_HURT_BACK_KICK_SC159_FINAL.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-darwin-hurt-backkick-sc159"
# then: montage the exported frames into $OUT/sheet-gb209-banana-darwin-hurt-backkick-sc159.png (6-9 frames, labeled)

# gb209-banana-darwin-hurt-himself-sc161 — Darwin — source: GB200_DARWIN_HURT_HIMSELF_SC161_FINAL.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-darwin-hurt-himself-sc161" "$WORK/swfs/GB200_DARWIN_HURT_HIMSELF_SC161_FINAL.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-darwin-hurt-himself-sc161"
# then: montage the exported frames into $OUT/sheet-gb209-banana-darwin-hurt-himself-sc161.png (6-9 frames, labeled)

# gb209-banana-destroyed-face-gumball — Gumball — source: GB209_DESTROYED_FACE_GUMBALL_V002.fla
"$FFDEC" -export frame "$WORK/frames_gb209-banana-destroyed-face-gumball" "$WORK/swfs/GB209_DESTROYED_FACE_GUMBALL_V002.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb209-banana-destroyed-face-gumball"
# then: montage the exported frames into $OUT/sheet-gb209-banana-destroyed-face-gumball.png (6-9 frames, labeled)

# gb202-remote-sc160-recover — Gumball, Darwin, Nicole, Richard — source: RECOVER_GB202REMOTE_Sc160_CLean_V003_jf.fla
"$FFDEC" -export frame "$WORK/frames_gb202-remote-sc160-recover" "$WORK/swfs/RECOVER_GB202REMOTE_Sc160_CLean_V003_jf.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb202-remote-sc160-recover"
# then: montage the exported frames into $OUT/sheet-gb202-remote-sc160-recover.png (6-9 frames, labeled)

# gb214-words-sc060-sfx — Gumball, Darwin (fragments) — source: GB214WORDS_Sc060_V003_SFX_AC.fla
"$FFDEC" -export frame "$WORK/frames_gb214-words-sc060-sfx" "$WORK/swfs/GB214WORDS_Sc060_V003_SFX_AC.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb214-words-sc060-sfx"
# then: montage the exported frames into $OUT/sheet-gb214-words-sc060-sfx.png (6-9 frames, labeled)

# gb2215-apology-test-export — Gumball — source: GB2215APOLOGY_TEST_EXPORT.fla
"$FFDEC" -export frame "$WORK/frames_gb2215-apology-test-export" "$WORK/swfs/GB2215APOLOGY_TEST_EXPORT.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb2215-apology-test-export"
# then: montage the exported frames into $OUT/sheet-gb2215-apology-test-export.png (6-9 frames, labeled)

