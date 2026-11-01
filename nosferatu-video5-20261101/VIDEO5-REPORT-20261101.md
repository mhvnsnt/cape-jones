# VIDEO 5 — Johnny Bravo dances ONLY + Nosferatu music — REPORT 2026-11-01

## Honest-source label (per Mars HONEST LABELING RULE, 2026-11-01 11:46 CST)
- NEW FILE, OLD VISUALS: this MP4 was built 2026-11-01 from Oct 31 Cape Jones
  dance-improved keys (63 frames, dance-improved-20261031/frames/, f001..f109).
  It is a re-cut/composite of those silent Cape Jones keys onto painted BGs,
  with new audio added. It is NOT new Johnny drawings, NOT show footage,
  NOT a show rig, NOT show art/audio in the picture.
- Johnny moves: "timing description from audit, Cape Jones pieces only."
  Move names come from ANIMATION-EXAMPLES-20261031.md descriptions, applied
  to Cape Jones's own pieces. No Johnny Bravo character, name, logo, or
  dialogue is in the video, and no show frame was copied.
- Audio IS actually used (verified below): Western Heart Nosferatu t01,
  downloaded from mhvnsnt/western-heart on main via GitHub API, size-verified.
  SFX are synthesized originals (this task), NOT show audio, NOT recorded voice.

## Count
- Video 5 total, SEPARATE from Videos 1-4 (Video 1 Johnny+Richard+Scooby
  throughout 75.789s, Video 2 other-show dances 75.789s, Videos 3-4 fixed
  same-visual EN+JP 75.789s). This video does NOT replace any of those 4.

## Nosferatu track — found, Western Heart original
- Repo: mhvnsnt/western-heart, main, description "WESTERN HEART — Chimera-built
  fighting game. Tekken 7 base + Tekken 3 legacy + Eastern Mind soul + wrestling systems."
- Search: GitHub code search for "nosferatu" returned 0 (binary audio is not
  code-indexed); git tree (61,124 entries, truncated) found 25 tracks.
- Decision doc: docs/decisions/2026-10-24-music-rotation-nosferatu-tekken.md,
  3,914 bytes, blob a6fd2e9e8e99a0c443649188a451ad72cfeaee94.
  It says: 25 Nosferatu game tracks, contiguous 0-5067s, cut from
  `nosferatu-exact.mp3` = owner's video audio = Internet Archive
  `Nosferatu1922VHS` transfer, anonymous 1980s VHS synth score, MoMA 1947 print.
  NO composer name exists in any documented source; none invented.
  License: VHS synth score copyright status UNKNOWN — do NOT label it public
  domain. Use-basis decision pending (per that doc).
- Track used (primary, first track, opening): game/assets/music/nosferatu-t01-opening-credits.mp3
  - Repo size: 5,065,389 bytes, git blob 04fc0c0afb1fc79cf82735aade919324d78fec9f
  - Downloaded copy in this folder: 5,065,389 bytes (exact match), md5 27f97f71d8c4b1357ced4af922497a89
  - Duration (ffprobe): 211.000000 s exactly
  - Other 24 tracks (t02-t25) exist in the same repo folder, listed in the
    task file; they were NOT used in this video. If Mars wants a different
    track (e.g. t11 Nosferatu's Shadow, t25 Finale Dawn), swapping the audio
    track is a re-mux, not a rebuild.
- Cape Jones repo: code search "nosferatu" = 0; git tree call returned 0 entries
  (truncated/failed, not relied on). Local cape-jones-rig .md grep found no
  Nosferatu audio. Mars's "some of it is in this repo too" is NOT confirmed
  for cape-jones by this search — the verified copy is Western Heart only.
  If a cape-jones copy exists under another name, it was not found here.

## Video — what it is
- File: video5-johnny-nosferatu-20261101.mp4, 1920x1080, 24 fps, 5,064 frames,
  duration 211.000000 s, 37,695,725 bytes, md5 05b60d1fd206af2b119041e76f6267fc
- Visual source: 63 dance-improved keys, each held 2 frames (24 fps, on 2s),
  one loop = 126 frames = 5.25 s, 40 full loops + first 12 keys = 5,064 frames.
  Loop point is the phrase return/breath to A-pose rest, so loops are clean.
  NO image-interpolation inbetweens were used — that is the flicker fix:
  the old 48 fps recreation (217 frames) FAILs the flash gate with 40 forearm
  flips (see dance-test flash JSON), while keys-on-2s cannot flip frame-to-frame.
- BGs (clean painted plates, no hero, no debug dots, verified in dance test):
  7 cuts, 30 s each, last cut 31 s, BG rotates room -> stage -> night-city:
  0-30s CJ-23 room, 30-60s CJ-09 stage, 60-90s CJ-29 night-city,
  90-120s room, 120-150s stage, 150-180s night-city, 180-211s room.
  Hero centred (x 613, 693x945), front standing rig, white suit + purple cape.
  No debug labels, no on-video text.
- NO Richard, NO Scooby gang in this video — Johnny only, per task.

## Johnny move mapping — honest status per named move
Phrase beats in every loop (from dance-improved BEAT-SHEET.md):
stride -> groove -> kick+punch snap -> split stance arms-up -> twist stand-in
-> arms-up hold -> return/breath.
- _6 dance flex, fists up at chest, knees bent, bouncing: PRESENT in groove
  keys (fists up, knees bent, bounce on 2s).
- _16 lab flex/dance, fists up, legs apart, bouncing: PRESENT in split/arms-up keys.
- _12 arms swinging across body, legs bent, torso twist: PARTIAL — arms swing
  and legs bend in stride/groove keys; true torso twist is a STAND-IN
  (asymmetric arms/legs, per beat sheet), NOT a drawn torso twist. Not claimed otherwise.
- _13 arms crossed forward, legs wide, grinning: NOT a distinct drawn pose in
  this key set. Arms swing across the body in groove keys, but the locked
  crossed-arms perfect reference (upper arms/bicep on TOP layer, torso NOT
  eating upper arms, Mars 2026-11-01 11:48 CST) was NOT verified on these keys
  and is NOT claimed here. Distinct crossed-arms pose still owed if wanted.
- _23 dance punch, one arm forward, other back, legs stepping: PRESENT as
  punch-style arm snap on the kick beat (on 1s in the original phrase, held
  on 2s here). Kick itself is WEAK/tangled per beat sheet — reworked forward
  kick still owed (foreshortened kick-leg piece first, per 2026-11-01 honest audit).
- _26 finger snap / karate kick: NOT distinct drawings in this key set.
  Snap SFX (below) marks the snap beat; a drawn finger-snap pose and a clean
  karate kick pose are NOT in these keys and are NOT claimed.
- _28 arms up, hands open, chest out: PRESENT in arms-up hold keys (fists
  curled in these keys, not open hands — open-hand variant not claimed).
- Fall pose (_24/_26/_27 sheets): NOT present, NOT faked, omitted.
- Hands: fists curled throughout this key set (per beat sheet). Open/palm/
  point/relaxed hand variants are NOT in this video's visuals; hand follows
  wrist in the original rig keys, no wrist cut was made here (no piece was
  cut, trimmed, or split in this build — keys were composited whole).

## Sound track — fully made clip, per Mars 2026-11-01 11:14 CST update
- Primary: Nosferatu t01, full 211.0 s, no excerpt, no stretch, volume 1.0.
- SFX (synthesized originals, make_sfx.py, seed 42, NOT show audio, NOT
  recorded voice, NOT Cape Jones song):
  - Step thump: 80 Hz sine, 0.09 s decay, on every beat (~0.583 s grid).
  - Bounce: 140 Hz sine, 0.12 s, on groove beats.
  - Finger-snap mark: noise burst + 2000 Hz ping, 0.05 s, on the kick/punch
    beat of each 5.25 s loop (this is an AUDIO mark, not a drawn snap pose).
  - Kick whoosh: noise sweep, 0.30 s, same beat as the snap.
  - SFX track: sfx-johnny-20261101.wav, 211.0 s, mixed at 0.35 volume under
    the Nosferatu track.
  - Picture-vs-audio check (per honest rule): snap/whoosh land on the
    punch beat, NOT on a flex moment; steps land on beat grid. No sweep/
    impact was placed over a flex-only frame on guess.

## Flash gate — PASS
- Script: flash_check.py, output flash_check.json.
- 5,064 frames @24 fps, 480x270 gray sampling.
- Forearm black/white flips (<100 -> >180 in one frame): 0.
- Max large whole-frame jumps per second (>50 mean): 1 (BG cuts every 30 s
  and key changes, not alternating flips).
- Whole-frame max jump: 65.9, forearm max jump: 68.8 (BG-cut jumps, not
  1-frame reversals).
- Verdict: PASS under WCAG 2.3.1 / Harding-style criteria used here
  (flips = 0, flashes/sec < 3). This is a measured gate on this file, not
  a claim that all dance videos pass — the old 48 fps test video FAILs
  (40 forearm flips) and is being fixed separately.

## Still owed / not claimed
- Mars approval of Video 5: 0/1.
- Distinct crossed-arms perfect pose, drawn finger-snap pose, clean forward
  karate kick pose, fall pose: NOT in this video, owed if wanted, not faked.
- GIF preview: first attempt (960px, 12 s) was Killed (OOM, sibling encodes
  sharing the VM); a smaller 640px/12fps/6s retry was still running at report
  time — MP4 is the deliverable, GIF is preview-only and is NOT claimed
  until it exists on disc.
- Repo landing: this folder is local only, no PR claimed, no commit made
  from the sparse cape-jones-flying clone.
- License note: Nosferatu VHS synth score copyright UNKNOWN per Western Heart
  doc — do not label public domain, do not ship as public-domain music
  without Mars's use-basis decision.
