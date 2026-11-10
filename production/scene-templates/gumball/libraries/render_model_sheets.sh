#!/bin/sh
# render_model_sheets.sh — staged renders for the Gumball libraries.
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

# gb200-puppet-gumball-v008 — Gumball — source: GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-gumball-v008" "$WORK/swfs/GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_008.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-gumball-v008"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-gumball-v008.png (6-9 frames, labeled)

# gb200-puppet-gumball-v006 — Gumball — source: GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_006.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-gumball-v006" "$WORK/swfs/GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_006.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-gumball-v006"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-gumball-v006.png (6-9 frames, labeled)

# gb200-puppet-gumball-v004 — Gumball — source: GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_004.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-gumball-v004" "$WORK/swfs/GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_004.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-gumball-v004"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-gumball-v004.png (6-9 frames, labeled)

# gb200-puppet-gumball-v001-cs3 — Gumball — source: GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_001_CS3.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-gumball-v001-cs3" "$WORK/swfs/GB200_ORIGINAL_PUPPET_GUMBALL_VERSION_001_CS3.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-gumball-v001-cs3"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-gumball-v001-cs3.png (6-9 frames, labeled)

# gb200-puppet-darwin-v002 — Darwin — source: GB200_ORIGINAL_PUPPET_DARWIN_Version002.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-darwin-v002" "$WORK/swfs/GB200_ORIGINAL_PUPPET_DARWIN_Version002.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-darwin-v002"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-darwin-v002.png (6-9 frames, labeled)

# gb200-puppet-darwin-v002-dup9 — Darwin — source: GB200_ORIGINAL_PUPPET_DARWIN_Version002 (9).fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-darwin-v002-dup9" "$WORK/swfs/GB200_ORIGINAL_PUPPET_DARWIN_Version002 (9).swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-darwin-v002-dup9"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-darwin-v002-dup9.png (6-9 frames, labeled)

# gb200-puppet-darwin-v002-cs5 — Darwin — source: GB200_ORIGINAL_PUPPET_DARWIN_Version002_CS5.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-darwin-v002-cs5" "$WORK/swfs/GB200_ORIGINAL_PUPPET_DARWIN_Version002_CS5.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-darwin-v002-cs5"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-darwin-v002-cs5.png (6-9 frames, labeled)

# gb200-puppet-mom-v002 — Nicole (Mom) — source: GB200_ORIGINAL_PUPPET_MOM_VERSION_002.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-mom-v002" "$WORK/swfs/GB200_ORIGINAL_PUPPET_MOM_VERSION_002.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-mom-v002"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-mom-v002.png (6-9 frames, labeled)

# gb200-puppet-mom-v002-dup10 — Nicole (Mom) — source: GB200_ORIGINAL_PUPPET_MOM_VERSION_002 (10).fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-mom-v002-dup10" "$WORK/swfs/GB200_ORIGINAL_PUPPET_MOM_VERSION_002 (10).swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-mom-v002-dup10"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-mom-v002-dup10.png (6-9 frames, labeled)

# gb200-puppet-dad-v004 — Richard (Dad) — source: GB200_ORIGINAL_PUPPET_DAD_VERSION_004.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-dad-v004" "$WORK/swfs/GB200_ORIGINAL_PUPPET_DAD_VERSION_004.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-dad-v004"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-dad-v004.png (6-9 frames, labeled)

# gb200-puppet-dad-v003 — Richard (Dad) — source: GB200_ORIGINAL_PUPPET_DAD_VERSION_003.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-dad-v003" "$WORK/swfs/GB200_ORIGINAL_PUPPET_DAD_VERSION_003.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-dad-v003"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-dad-v003.png (6-9 frames, labeled)

# gb200-puppet-anais-v002 — Anais — source: GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-anais-v002" "$WORK/swfs/GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-anais-v002"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-anais-v002.png (6-9 frames, labeled)

# gb200-puppet-anais-v002-dup8 — Anais — source: GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002 (8).fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-anais-v002-dup8" "$WORK/swfs/GB200_ORIGINAL_PUPPET_ANAIS_VERSION_002 (8).swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-anais-v002-dup8"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-anais-v002-dup8.png (6-9 frames, labeled)

# gb200-puppet-hector-v001-cs3 — Hector — source: GB200_HECTOR_ORIGINAL_PUPPET_V001_CS3.fla
"$FFDEC" -export frame "$WORK/frames_gb200-puppet-hector-v001-cs3" "$WORK/swfs/GB200_HECTOR_ORIGINAL_PUPPET_V001_CS3.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): gb200-puppet-hector-v001-cs3"
# then: montage the exported frames into $OUT/sheet-gb200-puppet-hector-v001-cs3.png (6-9 frames, labeled)

# rig-carrie-ghost — Carrie — source: Carrie_Ghost.fla
"$FFDEC" -export frame "$WORK/frames_rig-carrie-ghost" "$WORK/swfs/Carrie_Ghost.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): rig-carrie-ghost"
# then: montage the exported frames into $OUT/sheet-rig-carrie-ghost.png (6-9 frames, labeled)

# rig-ocho-spider — Ocho — source: Ocho_Spider.fla
"$FFDEC" -export frame "$WORK/frames_rig-ocho-spider" "$WORK/swfs/Ocho_Spider.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): rig-ocho-spider"
# then: montage the exported frames into $OUT/sheet-rig-ocho-spider.png (6-9 frames, labeled)

# rig-penny-peanutantlers — Penny — source: Penny_PeanutAntlers.fla
"$FFDEC" -export frame "$WORK/frames_rig-penny-peanutantlers" "$WORK/swfs/Penny_PeanutAntlers.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): rig-penny-peanutantlers"
# then: montage the exported frames into $OUT/sheet-rig-penny-peanutantlers.png (6-9 frames, labeled)

# rig-tobias-sportypuff — Tobias — source: Tobias_SportyPuff.fla
"$FFDEC" -export frame "$WORK/frames_rig-tobias-sportypuff" "$WORK/swfs/Tobias_SportyPuff.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): rig-tobias-sportypuff"
# then: montage the exported frames into $OUT/sheet-rig-tobias-sportypuff.png (6-9 frames, labeled)

# fosters-turn-madam-foster — Madame Foster — source: Madam_Foster_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-madam-foster" "$WORK/swfs/Madam_Foster_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-madam-foster"
# then: montage the exported frames into $OUT/sheet-fosters-turn-madam-foster.png (6-9 frames, labeled)

# fosters-turn-goo — Goo — source: Goo_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-goo" "$WORK/swfs/Goo_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-goo"
# then: montage the exported frames into $OUT/sheet-fosters-turn-goo.png (6-9 frames, labeled)

# fosters-goo-hair — Goo (hair only) — source: Goo_Hair.fla
"$FFDEC" -export frame "$WORK/frames_fosters-goo-hair" "$WORK/swfs/Goo_Hair.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-goo-hair"
# then: montage the exported frames into $OUT/sheet-fosters-goo-hair.png (6-9 frames, labeled)

# fosters-turn-duchess — Duchess — source: Duchess_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-duchess" "$WORK/swfs/Duchess_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-duchess"
# then: montage the exported frames into $OUT/sheet-fosters-turn-duchess.png (6-9 frames, labeled)

# fosters-turn-ed — Ed (Eduardo) — source: Ed_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-ed" "$WORK/swfs/Ed_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-ed"
# then: montage the exported frames into $OUT/sheet-fosters-turn-ed.png (6-9 frames, labeled)

# fosters-turn-cheese — Cheese — source: Cheese_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-cheese" "$WORK/swfs/Cheese_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-cheese"
# then: montage the exported frames into $OUT/sheet-fosters-turn-cheese.png (6-9 frames, labeled)

# fosters-turn-frankie — Frankie — source: Frankie_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-frankie" "$WORK/swfs/Frankie_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-frankie"
# then: montage the exported frames into $OUT/sheet-fosters-turn-frankie.png (6-9 frames, labeled)

# fosters-turn-terrence — Terrence — source: Terrence_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-terrence" "$WORK/swfs/Terrence_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-terrence"
# then: montage the exported frames into $OUT/sheet-fosters-turn-terrence.png (6-9 frames, labeled)

# fosters-turn-coco — Coco — source: Coco_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-coco" "$WORK/swfs/Coco_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-coco"
# then: montage the exported frames into $OUT/sheet-fosters-turn-coco.png (6-9 frames, labeled)

# fosters-turn-wilt — Wilt — source: Wilt_Turnaround.fla
"$FFDEC" -export frame "$WORK/frames_fosters-turn-wilt" "$WORK/swfs/Wilt_Turnaround.swf" 2>/dev/null || echo "STAGED-ONLY (no companion SWF / guard): fosters-turn-wilt"
# then: montage the exported frames into $OUT/sheet-fosters-turn-wilt.png (6-9 frames, labeled)

