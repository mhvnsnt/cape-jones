# Animation Resources — pulled, researched, and queued

**Scout pull-in lane, 2026-10-17.** Covers the owner's animation-set directive:
idle, walk, run, sit/stand, reach/grab, dialogue gestures, reactions — idle
first. The rig/animation specialist retargets everything to the 85-bone rig.

## PULLED (in this repo, this PR)

### CMU MoCap starter pack → `3d-assets/animation/mocap-cmu/`
13 BVH motions, license-clean (CMU: free for research AND commercial worldwide,
attribution appreciated — verbatim terms in MANIFEST.md). No login needed.
Verified importing in Blender 4.0.2. Covers: idle ×2, sitting idle (fidget),
walk ×2, run, sit/stand ×2, dialogue gestures, wave, laugh, anger, drink.
Full manifest + retarget notes: `3d-assets/animation/mocap-cmu/MANIFEST.md`.

### Blaster VFX asset → `3d-assets/vfx/blaster/` (separate PR)
Built (not downloaded): `cj_blaster_vfx.blend` — jagged starburst bolts, beam,
muzzle flash, shockwave ring, color-casting light rig. Locked palette (core
#FFFFFF, glow #FFB300). See `docs/research/BLASTER-VFX-RESEARCH.md`.

## RESEARCHED (documented, not pulled — with reason)

### Mixamo (Adobe) — NEEDS PARENT BROWSER LANE
The best free mocap + auto-rigger library for our needs (thousands of clips,
FBX, Mixamo-to-Blender retarget is a solved workflow). **Blocker: requires an
Adobe account login to download — a subagent cannot do this.**
Spec for the parent browser lane:
1. Sign in at mixamo.com (Adobe account).
2. Download as FBX for Blender (no skin): idle set — "Idle", "Sitting Idle",
   "Talking On Phone Idle"? (pick dialogue idles); locomotion — "Walking",
   "Running"; sitting — "Sitting" clips; gestures — "Waving", "Pointing",
   "Laughing", "Angry" packs.
3. License: free with Adobe account, royalty-free for commercial use (verify
   current Mixamo EULA at pull time — terms have changed before).
4. Drop FBXs where the specialist says (likely `3d-assets/animation/mocap-mixamo/`).

### Rigify — already in Blender, no pull needed
Verified present in our Blender 4.0.2 (`RIGIFY-BUILTIN-YES`). Standard free
retarget target for Mixamo/CMU mocap; face-rig bones available. Documented as
the retarget intermediary if the specialist wants it.

### BlenRig 6 — already in `production/tools/blenrig6/`
Facial rig = mouth-rigging baseline per team briefing. No action needed.

### Blender Studio open movies (Sintel, Rain, Sprite Fright cast)
CC-BY production files — the best public "studio-grade" rigs to study
(toon face rigs especially). **Not pulled:** multi-GB downloads, old files may
need 4.x migration. The specialist can pull per-need; the face-rig research
doc (`docs/research/BATMAN-FACE-RIG-RESEARCH.md`) covers what's where.

### Face-rig technique research — separate deliverable
`docs/research/BATMAN-FACE-RIG-RESEARCH.md` (PR: research/batman-face-rig-20261017):
Arkham/Telltale technique study, Preston Blair viseme system, Rhubarb Lip Sync,
swap-set/pupil-toggle architecture, toon-shader stack, licenses, and the
recommended comedy-first face system. The mouth-rigging task starts there.

## License posture (whole lane)
- Pulled: only CMU (commercial-safe) + original builds. Nothing redistributed.
- Ripped game assets (models-resource etc.): study-only, never in the repo.
- Paid tools (FaceIt, Gumroad laser pack): documented as technique, never
  purchased, never cracked.
- Every future pull logs its license in its PR. No exceptions.
