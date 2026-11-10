# Movement Library — Cape Jones, transform only
Date: 2026-11-01. Mars, 2026-11-01 11:13 CST: pull all animations/movements
that can be found in Gumball, Foster's Home, Smiling Friends, Nickelodeon,
Disney, Cartoon Network shows, to build episodes with, and send clips of
Cape Jones doing those animations.

HARD LIMIT (standing, and for this task): MOVEMENT ONLY is pulled.
No show character art, no rig file, no .fla/.swf/.mov, no dialogue, no
name, no logo, and no leaked archive was downloaded for this library.
What is used is already-verified material on disc: SHOW-REPO-DEEP-AUDIT-20261031.md
(41 rows), show-repo-animation-audit-20261031 (22 archives newly listed),
dance-gumball-darwin-words-sc057-sc059.json (prior, cited in audits),
ANIMATION-EXAMPLES-20261031.md (29 files, descriptions + timing only),
and the public-domain animation technique library. If a show has no
verified movement file, it is listed NOT FOUND below — no movement was
invented for it, and its archive was not downloaded on guess.

## How to read this library
- Timing is the pull, not the picture. A beat grid, a keyframe count, an
  on-1s/on-2s rule, a stride→groove→kick→twist progression, a walk
  contact/passing cycle, a pose-swap library — those transfer to Cape
  Jones's own pieces. The donor character does not.
- Cape Jones mapping is always: front standing rig (NOT V6 sitting rig),
  his own white suit + purple cape/cowl, his own hands (wrist gate:
  wrist end to forearm end, wrist nearer than fingertip, hand follows
  wrist bone where a bone rig is used), legs (knee+feet same direction,
  feet grounded unless a step/kick lift is labelled), cape swing/drape,
  torso twist where the rig allows it (true torso twist piece still
  owed in places — stand-in noted where it applies).
- Sound per clip is synthesized original SFX (numpy, in build_clips.py),
  NOT show audio, NOT a show song: footsteps = low thump, punch/kick =
  whoosh + impact thump, dance bounce = sine blip, finger snap = short
  noise burst. No copyrighted music is in these clips. Final episode
  mixes still need a -14 LUFS loudnorm pass — these SFX tracks are
  peak-normalised to -1 dB, not claimed as a final mix.

## Verified movement families (clips built)

### 1. Gumball — Darwin dance, "The Words" GB214
- Source verified: Sc057 wide 198f + Sc059 close-up twist 105f, 25 fps,
  beat grid ~14f (~107 BPM), keyframed on twos, Sc059 twist layer
  32 keyframes f43-97, progression stride → groove → kick → split
  stance → twist, puppet slots head / L-R fin / L-R leg / body.
- Also: 20 dance FLAs in RAR5 walk, 10 unique Darwin dance scenes
  (duplicated across trees, so ~half the count is unique content).
- Cape Jones version: clip 01-gumball-dance-strut-twist (dance-recreation
  main lineage, knee-feet-corrected + arm-front-snap, 217f @48fps source,
  4.52s). Sound: footsteps on beat grid + bounce blips between beats.
- Episode use: dance scene, hero in one spot, world/lighting changes
  around him. Twist is the hardest part — true torso twist still owed
  in some frames (stand-in in source lineage, noted, not hidden).

### 2. Gumball — fight scenes
- Source verified: KeyAnim + fight FLAs: DARWIN_HURT_BACK_KICK Sc159,
  GUMBALL_HURT_FACEKICK Sc155, HURT_FLOOR Sc160, HURT_HIMSELF Sc158/161,
  GB202REMOTE Sc144/147, GB218Flakers Sc002/117. XFL timelines, keyframed
  on stage. Fight-move timing + puppet slot structure are the pull.
- Cape Jones version: clip 02-gumball-fight-kick (dance-improved lineage,
  groove + kick, kick at f042 in source keys — weak/tangled in original
  lineage, reworked kick still owed, stated in clip report).
  Sound: footsteps + whoosh + impact thump at kick.
- Episode use: fight / reaction beats, grounded, punch/kick on 1s.

### 3. Foster's Home — pose-swap gesture / web reels
- Source verified: 7 .fla + 15 .swf CN dot-com reels (Berry 1,847f,
  Bloo 2,190f, Cheese 1,892f, Coco 1,808f, Ivan 1,618f, Uncle Pockets
  2,031f, Wilt 1,892f, ALL 24 fps, SWF headers parsed). Frankie rig
  pds3hx.fla: 1 binary FLA, 430 part comps, turnaround views
  (3/4: 118, side: 82, 3/4-back: 30, front: 28, back: 16), chin+mouth
  expression pair. Dance: NOT VERIFIED — long character reels, no
  dance identified. Rig only for Frankie, no performed scene in it.
- Cape Jones version: clip 03-fosters-pose-swap-gesture (chain-punch
  lineage: windup → snap → impact locked → recover, 24 fps, 3.12s).
  Sound: whoosh + impact + snap on gesture changes.
- Episode use: gesture / talk / reaction, pose-swap on beat, holds.

### 4. Smiling Friends — pose-swap / head / mouth libraries
- Source verified: Charlie .fla 82,390 B + PimRigUpdate .fla 296,483 B,
  Animate 22, 1920×1080, master-symbol stacks (Charlie 9 layers,
  Pim 5 layers), head sub-symbols, pupil/brow/lid symbols, mouth as
  frame-addressed drawing library (Charlie mouth 25 frames), leg
  library 10 frames, arms 2-3, brows/lids 3 each, mask layers.
  Dance: NO. Scene timelines EMPTY — rigs only, no saved scene.
- Cape Jones version: clip 04-smiling-friends-pose-swap-head
  (successor-pose-dialects lineage, 24 fps, 5.58s, pose swaps held
  per frame, head/mouth/leg swaps). Sound: snap on each swap + blip
  on head turn. No donor mouth art is in the clip.
- Episode use: dialogue / reaction / head-turn beats, mouth/eye swaps.

### 5. Scooby-Doo Mystery Inc. — song-step timing
- Source verified: 0 .fla in inventory. Only song material: ep. 607
  act D song animatic .mov (baked video, timing only). Model packs /
  storyboards / scripts are reference, not motion. Dance: NO rig.
- Cape Jones version: clip 05-scooby-song-step (chain-dance lineage,
  24 fps, 3.88s, step on beat). Sound: footsteps + bounce blips.
- Episode use: song-step / group-energy solo dance, stepping in sync.

### 6. Nickelodeon single-show archive — baked-cache walk
- Source verified: 8 Maya .ma rigs (character v041, location v008,
  noodle-arm/hands/feet/noodle-wrap/catcher props) + 4 Alembic .abc
  caches (frames 1-182, 183-244, 244-399, 400-586) = animation saved
  as baked cache, not timeline. Also: pose-sheet + storyboard PDFs,
  1 dance video (timing only, show unidentified in audit), 1,028 audio
  files (NOT used — show audio barred). nick.7z (7.21 GB): UNKNOWN,
  not listed, no 7z tool on VM — NOT claimed empty, NOT claimed to
  hold rigs.
- Cape Jones version: clip 06-nick-baked-cache-walk (chain-walk
  lineage: contact → passing → contact → passing, 24 fps, 2.79s,
  continuous, no holds — the baked-cache analogue).
  Sound: footsteps on every contact.
- Episode use: walk cycles, travel, entering a room, grounded.

### 7. Johnny Bravo — flex / dance (from Mars's GIF pose sheets)
- Source verified as descriptions only: ANIMATION-EXAMPLES Batch 1+2.
  _6 dance flex fists up chest knees bent bouncing, _16 lab flex/dance
  fists up legs apart bouncing, _12 arms swinging across body legs
  bent torso twist, _13 arms crossed forward legs wide grinning,
  _23 dance punch forward/other back legs stepping, sheets _24-_28
  flex/dance/lean/arms crossed/pointing/finger snap/karate kick/
  arms up hands open chest out. Johnny Bravo repo itself: model
  sheets/bible only, rig NO evidence, zip NOT listed — no rig dance
  was pulled from that repo.
- Cape Jones version: clip 07-johnny-bravo-flex-dance (chain-flex-fight
  lineage, 24 fps, 3.12s). Sound: bounce blips + snaps on finger snap.
- Episode use: flex / show-off / dance groove, holds 6-24f on flex.

### 8. Richard + Scooby gang — arms-up / stepping dance
- Richard: _32 Richard dancing on a couch, arms up, legs apart.
  NO rig dance exists (pose library / model sheet only, 0 performance).
- Scooby gang: _11 group dance, 4 characters stepping, arms up/swinging,
  in sync; _29 Gumball+Darwin dancing together, arms up, legs stepping.
- Cape Jones version: clip 08-richard-scooby-gang-step
  (dance-recreation combine lineage, 215f @48fps source, 4.48s,
  stepping + arms up/swinging, solo version of a group dance).
  Sound: footsteps + bounce blips.
- Episode use: group-energy dance, party / stage, arms-up chorus.

## NOT FOUND / NOT PULLED (plain list)
- Disney TVA: bibles + pilot MP4s only, catalogued not pulled. Rig NO,
  dance NO. Bible/pilot structure only — no movement clip built from it.
- Disney FLA rar: 1 .fla by filename only (ww226_26s_016_final.fla,
  39.9 MB unpacked), content NOT downloaded, unknown. NOT claimed.
- Powerpuff Girls: PPG_flas.rar contains 1 ZIP, 0 .fla (name promise
  debunked). Original zip: model sheets + QTVR turnarounds only.
- Teen Titans (all 3 archives): 0 .fla/.swf, model sheets only.
  No rig, no saved animation — pose/expression reference only.
- Rick & Morty Toon Boom files (17.7 MB zip): present, UNOPENABLE here
  (no Toon Boom on VM, trial blocked on Mars's secure entry).
- Regular Show, Foster's complete, Adventure Time cnzip, OK K.O.
  complete, nick.7z: UNKNOWN — archives as held do not terminate with
  a readable central directory, or were not listed. Never "empty".
- Cartoon Vault unsorted other 7 FLAs (alien/earth/BOSS/BG/poster):
  format-level only, content unexamined, UNKNOWN.
- Adventure Time loose: animatic .mov/.mp4 + notes PDF only, timing
  study only, no rig. Camp Lazlo, Chowder, Dexter, Duck Dodgers,
  Ed Edd n Eddy, Grim, Johnny Test, KND, Looney Tunes, MGM, Animaniacs,
  Pink Panther, Robot Chicken, Space Ghost, Cow & Chicken, My Gym
  Partner, I Am Weasel, Bakugan, Samurai Jack, Primal: model sheets /
  art / bibles / docs only, or empty/placeholder — 0 verified dance/rig
  in this audit, so no clip was invented for them.
- Randy Cunningham: 6 .fla + 4 .swf + 1 AE project for a saved scene
  (RC118_SC001) IS verified, but its FLA check (XFL vs binary) + AE
  structure is still owed — so no Randy clip is claimed here; its
  scene-layer structure is the next pull, not a guessed dance.
- Public-domain technique library: films (pre-1931, PD) + playbook —
  timing principles only (squash, stretch, holds), no character reuse;
  characters in some PD films are still trademarked, so study only.

## Counts
- Movement families with a clip: 8/8 in this build.
- Shows/networks inventoried from audit: 41 rows in deep audit,
  plus animation-audit archives (22 newly listed).
- Verified performed dance in whole audit: 1 (Gumball Darwin GB214).
- Verified saved-animation repos: Gumball, Foster's reels, Randy
  scene, Smiling Friends rigs, ch_max/ch_ruby builds, Nick Maya caches.
- Clips in this folder: 8 MP4 (with sound) + 8 GIF previews.
- No show art, no show rig file, no show audio, no dialogue, no
  name, no logo was copied into any clip or into this library.
