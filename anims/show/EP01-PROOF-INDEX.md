# Episode 1 "Immortal Qombat" — proof index (Track B, 2026-10-24)

Every frame below was VIEWED by the Track B worker (Workbench renders,
640x360, solid + material color + cavity — pose/contact proof, NOT
beauty rendering). Workbench shading is flat gray with face-texture
noise; head SHAPE is intact in all viewed frames. Shading artifacts are
not face-stretch defects. EEVEE/Cycles beauty rendering was not done
and is not required for animation verification.

## Single clips — Cape (proof/cape/, fixed T3 bake)

- `ep1_cape_stance` f0001 / f0054 / f0107: held guard, coherent, feet on
  ground. (Near-identical frames are the near-static stance data, not a
  playback bug.) PASS.
- `ep1_cape_strike_light` f0011 (mid-spin, upright, one leg raised,
  torso twisted, arm up), f0021 (standing, turned 180 deg, guard, feet
  on ground). PASS as a spinning strike. (Pre-fix crumpled-ball /
  upside-down versions are superseded and must not be used.)
- `ep1_cape_strike_heavy` f0017 (upright, leaning into overhead/hook
  swing, arm cocked high, lunge, feet on ground). PASS.
- `ep1_cape_hit` f0010 (staggering/reeling, head back, arm up). PASS.
- `ep1_cape_hit_launch` f0012 (airborne tumbling, curled,
  upside-down-ish). PASS as a launch reaction MID-CLIP. Tail frames 15+
  drive the pelvis below ground (measured) — the paired choreography
  uses frames 0-14 only.
- `ep1_cape_ko` f0039 (flat on back/side, sprawled, ON the ground plane,
  no sinking). PASS.

## Single clips — Pantera (proof/pantera/)

- `ep1_pantera_stance` f0037 (standing panther guard, tail visible,
  feet on ground). PASS. Framing is tight at the top.
- `ep1_pantera_grab` f0017 (character mostly ABOVE the frame mid-throw
  lift — framing failure, not motion failure), f0034 (lying on back on
  the ground, legs up-ish, tail visible — suplex ending). PASS as a
  suplex with the framing note.

## Paired fight — v1 (proof/paired/, SUPERSEDED by v2 for the chain)

- f0000 (Pantera deep-crouch stance frame 0 + Cape stance), f0060 (both
  standing guards), f0135 (Cape staggering, Pantera closed in), f0161
  (grab start, Pantera low, close). Viewed; beats carried into v2.
- f0175 v1: FAIL — the two bodies tumbled separately with no contact.
  Fixed in v2 (trimmed launch + follow offsets).
- f0196 v1: FAIL — tangled heap at the win cut (Pantera stance frame 0
  = deep crouch + Cape ko frame 0 overlapping). Fixed in v2 (win strip
  from standing stance frames 30-69).
- f0235 v1: Pantera standing + Cape down, but void background (no
  ground plane). Ground plane added in v2.

## Paired fight — v2 (proof/paired2/, the deliverable proof)

- f0176 (lift peak): bodies locked together airborne through the lift
  — contact reads. Lift peak is slightly cut at the top of the frame
  (camera look target 1.0 vs ~1.4 m lift + 1.8 m bodies) — framing note
  for the final (pull camera back / raise target). PASS.
- f0185 (slam): both on the ground in a heap, intertwined — the slam
  landing reads. PASS.
- f0196 (win cut): Pantera STANDING guard + Cape on the ground beside
  him — clean win cut, no heap. PASS.
- f0235 (end): Pantera standing ON the ground plane + Cape flat on the
  ground — the finish reads (winner standing, loser down). PASS.
- Ground plane (neutral, at arena ground level) makes foot/ground
  contact legible. The arena GLB is 140 m wide, so at fight-camera
  distance its dressing falls outside the frame and reads as void —
  arena-composited beauty proof is PENDING (see choreography doc), not
  faked.
- `ep1_chain_170_195.mp4`: 26 frames @30fps, realtime, assembled from
  the viewed v2 chain frames. NOTE: the video file itself was not
  played back (no playback tool in this lane); every frame it contains
  was viewed individually as a PNG.

## Living-room beats (proof/room2_*, room GLB stage)

- `room2_flip` f0000 / f0020 / f0045 / f0120 (south view): seated pose,
  arm point (f0020), head turns + hand wags (f0045/f0120) all read;
  Cape at the frame edge in that camera. Pulled-back f0020: seated
  figure FULLY in frame, arm extended pointing, legs visible. PASS.
  (Feet dangle past the footrest — documented staging note.)
- Tight nofloor f0000 / f0020: full seated body verified (legs present
  and correctly posed). This resolved the v1 "floating torso" misread:
  the legs were occluded by the coffee table from the low front camera,
  not missing from the clip. PASS.
- `room2_flight` f0025 (standing at chair, frame edge), f0060
  (superman mid-flight toward the TV, pitched forward, arms back, legs
  extended). PASS. Path-camera f0095/f0115: Cape at the frame edge /
  occluded — framing failure, not motion failure.
- Landing close-up `land_f0095` / `land_f0115`: crouch in front of the
  TV console (CRT TV visible, arms out, knees bent) — the arrival beat
  reads. Camera is rolled ~20-45 deg (diagonal view) — framing note.
  PASS.
- v1 room proofs against `living_room.blend` (proof/room_flip/,
  proof/room_flight/) are SUPERSEDED: that .blend's built-in Cape body
  does not follow a posed rig and its Recliner collection is empty, so
  those renders show no character. Do not use them.

## LED gag

- Numeric proof (printed key values): flicker f30=1.0, f32=0.1,
  f34=1.0, f36=0.2, f38=1.0, f40=0.1; pulse f50=0.98, f65=0.86; dropout
  f90=0.05, f100=0.05; steady f105=1.0. The pattern exists in the
  material's keyframes. PASS (pattern).
- EEVEE visual (on vs dropout): PENDING at proof-index writing (CPU
  EEVEE render in progress). If it does not complete before the PR, the
  gag ships with the script + numeric proof, and the EEVEE visual stays
  an open verification item — it is not claimed as viewed.
