# Dance scene revisit — test, 2026-11-01
## Song — FOUND, verified on main, not invented
- Title: ケープ・ジョーンズ・ダンス — Cape Jones Dance, anime-intro song for the Cape Jones dance scene.
- Canon (lyrics.md, verified by reading the file): deadpan caped hero dances in ONE spot; world and lighting change around him; dance never changes.
- Repo: mhvnsnt/cape-jones, production/vocal-stack/song/, verified via GitHub Contents API on main, 25 files.
- Structure: C major, 152 BPM, 48 bars, 75.8s; intro → verse A → chorus A → verse B → bridge → chorus B → outro.
- v2 full mixes, both 1,820,674 bytes, DIFFERENT md5 (distinct mixes, not duplicates):
  - song-full-v2-jp.mp3, md5 2c8d06a1ca4de88db1afce2c30e42255, duration 75.789s
  - song-full-v2-en.mp3, md5 1761698d6e2cd0555b12aca957433ac8, duration 75.789s
- Also on main: song-vocal-stem-v2-jp.wav / -en.wav (13,369,364 bytes each), song-instrumental-v2.mp3, lyrics.md (JP + romaji + EN translation).
- Local copy: fetched into the sparse clone ~/workspace/cape-jones-flying/production/vocal-stack/song/ for this test only.
  That clone is READ-ONLY for pushing and was NOT committed from (sparse-checkout anti-clobber law) — no commit made here.
- Vocal honesty (README.md): NOT a real VOCALOID5/Avanna voicebank; espeak-ng JP guide + Rubber Band pitch placement + Avanna-bus chain. v2 locked -14 LUFS / -1 dBTP per prior memory; song-list approval 0/1.
## Old dance scenes — list, approvals, cuts, song attached?
- dance-improved-20261031: 63 keys, f001..f109 on twos, 24fps ~107 BPM, beat starts 1,15,28,42,56,69,83,97,110. BUILT+VIEWED, NOT approved 0/1. Song attached: NO (silent, beep noted only). Defects: kick f042 weak/tangled, twist stand-in, JoJo pink on twist frames.
- dance-kneefeet-fix-20261031: 63f. SUPERSEDED — block-range FootIn wrong both directions. Song: NO.
- dance-kneefeet-fix-correction-20261031: 63f. APPROVED 100% PERFECT by Mars 2026-10-31 17:50-17:51 CDT. Per-frame rule FootIn ONLY IF leg_upper L>0 AND R<0. Song: NO (GIF only; MP4 attempts failed/0-byte, deleted).
- dance-arm-snap-20261031: 63 keys f001..f109, knee-feet correction + arm-front-snap (21/63 snapped). Built+viewed, approval 0/1. Song: NO.
- dance-recreation-20261031 MAIN (A): 217f @48fps, 4.52s, from arm-snap keys + image-interpolation inbetweens (NOT rig re-pose). Approval 0/1. Song: NO — SILENT by design, EN/JP audio slot documented, same visual cut for both languages (track swap, not re-edit).
- dance-recreation-20261031 COMBINE (B): 215f @48fps, 4.48s, from mochiichao-combine 108f. Approval 0/1. Song: NO, same slot.
- mochiichao-combine-build-20261031 dance-clip-combined: 108f f000..f107 @24fps. Approval 0/4 for combine as whole. Song: NO. Background-life loops separate (room/street/forest).
- Ghoul Shuffle = SQUAT SQUAT SHUFFLE OOGA BOOGA THREE QUARTER TURN AND THEN FORWARD FACE:
  - V1 ghoul-shuffle-lastframe-handswap-20261031: 37f @12fps, OFFICIAL V1, md5 f80a3d403b195fbe809080f3413f360b, untouched.
  - V2 ghoul-shuffle-v2-free-hands-20261031: 74 frames in folder, SAVED AS GOOD (not "rejected").
  - V3 ghoul-shuffle-v3-hand-mobility-20261031: 74 frames, approval 0/1 for dance version (saved, not approved, not rejected).
- Shimmy Number One, shimmy-step-fix-20261101: 97f @24fps, 4.04s, stepped (alternating feet, never both up). APPROVED PERFECT 1/1 per prior summary (stepped version); old successor-shimmy NOT approved. Song: NO.
- "Old rejected": NO dance clip was found labelled rejected as a whole. The rejected items are: v1 knee-feet block fix (superseded), old successor-shimmy (not approved), v1 vocal mix (different project, Mochiichao title, not this song). Do NOT label Ghoul V2/V3 or the recreations as "rejected" — they are saved-good / 0/1, respectively.
- Cuts/setup: all dance cuts are one visual cut, beat-grid cuts at beat starts (24fps grid above, doubled at 48fps). Language versions are track swaps, never re-edits. No separate JP-cut vs EN-cut exists.
## Tempo — mismatch, NOT silently stretched
- Song: 152 BPM, ~9.5f/beat @24fps. Dance visual: ~107 BPM, 13-14f/beat @24fps, LOCKED for 2D.
- This test visual stays at 107 BPM. JP/EN audio excerpts below are the real song's first 4.521s at its native 152 BPM, so beats do NOT land beat-for-beat on the visual in this test — stated, not hidden. This is a scene/layout test, not a beat-synced final.
- Stretched demo, labelled DEMO ONLY, not used as JP/EN audio: songs-temp-vocals-20261101/cj-song-stretched-152-to-107-demo-20261101.wav, 17.94s, ffmpeg atempo 0.70395. Temp songs in that folder are synthesised originals, NOT the repo song, NOT recorded voice, NOT JP/EN language versions.
## Test built — front standing dance, hero in one spot, world/lighting change
- Base visual: dance-recreation MAIN frames-a (217f, front-facing, knee-feet-corrected + arm-front-snap lineage, image-interpolated).
- CORRECTION to task wording: this is NOT the V6 sitting rig. V6 (rig-34-locked-neck-v6) is a sitting 3/4 pose, it cannot do a standing dance. The front standing dance rig is the only front dance rig on disc. Do not claim V6 is dancing.
- Canvas 1920x1080, 217f @48fps, 4.521s, hero centred, opaque bbox bottom aligned to ground y=950 in every frame, no hand-draw, no new pieces, no debug labels in finals.
- Environments, all clean painted BGs (verified by eye, no hero, no debug dots in the plates themselves):
  1. f000-072: CJ-23 room painted (warm room, bookshelf, window, rug) — art-owed-backgrounds-20261031/per-shot/CJ-23-bg-room-painted-new-20261031.png
  2. f073-144: CJ-09 stage painted (pink/purple spotlights, curtains) — CJ-09-bg-stage-painted-new-20261031.png
  3. f145-216: CJ-29 night-city painted (moon, blue night, rooftop) — CJ-29-bg-night-city-painted-new-20261031.png
- Lighting change = BG/lighting change per segment (warm room → stage spotlights → moonlit night). Hero itself was not regraded in this test.
- FIRST BUILD DISCARDED after own-eyes check (not shown to Mars): canonical-room scene plate + showcase on-background plates contain a second hero and/or red debug joint dots. Those plates were NOT used in the final test. Showcase on-background-*.jpg are hero-on-background composites with debug dots, not clean BGs — do not reuse them as clean plates.
- Inherited defects, not hidden: kick f042 weak/tangled, twist is a stand-in, JoJo-tension pink on twist frames (visible in night-city segment), interpolation ghosting on fast moves in recreation frames. Dance hands here are curled fists (beat sheet), so the open-hand wrist gate is N/A; fists stay attached in viewed keys per prior checks. Feet move as dance steps/kick lifts, not a planted-idle — labelled dance motion, not airborne flight.
- Files:
  - dance-test-visual-silent-20261101.mp4 (1920x1080, 217f, 48fps, 4.521s, silent)
  - dance-test-JP-excerpt-20261101.mp4 (same visual + first 4.521s of song-full-v2-jp.mp3, TEST EXCERPT, not full song)
  - dance-test-EN-excerpt-20261101.mp4 (same visual + first 4.521s of song-full-v2-en.mp3, TEST EXCERPT, not full song)
  - dance-test-20261101.gif (960x540 chat version)
  - frames/test-f000..f216.png, build_test2.py, check2-f*.png (segment-boundary checks, viewed)
- One visual cut works for both languages: JP and EN MP4s share the identical silent visual file; only the audio track differs.
## Still owed
- Mars approval of this test: 0/1. Song-list approval: 0/1 (prior).
- Beat-sync decision: re-time song, stretch song, or re-grid dance to 152 BPM — Mars decision, not silently done here. Full-song version (75.8s) would need the dance looped/rebuilt to full length, not done here.
- Reworked kick, true torso twist, two-hand device grip, background-life pass, clean full-size final render with lighting, rig-angle inbetweening (vs image interpolation) — all still owed per recreation report.
- Landing: this folder is local only, no PR claimed. Side-view bone-parent fix is a separate running task, not done here.
