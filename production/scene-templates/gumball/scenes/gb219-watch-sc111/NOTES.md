# The Watch — Sc111: faces mashed flat against the glass pane (KeyAnim line art)

**Episode:** GB219 "The Watch" (Season 2) · **Scene:** Sc111 · **Frames:** 68 @ 25fps · **Source:** GB219WATCH_Sc111_KeyAnim_V002.fla / .swf

## Story / beat
Gumball (top) and Darwin (below), riding mobility scooters, come up behind a glass pane and squash against it. For the first ~30 frames they are upright and worried, palms pressed to the glass. Then the press lands: cheeks flatten and balloon, features smear across the pane (red animator circles mark the contact points), and by f43–68 both are fully mashed blobs — feet, hands and faces all flattened against the glass.

## Cast
- **Gumball** — GB219WATCH_Costume_MobiltyScooterPoses_GUMBALL_PUPPET_001 (30 kf), the episode-specific scooter-pose puppet; stock GB200_GUMBALL_PUPPET_001 (256 kf) also in the library, plus single-pose variants BACKVIEW (8 kf), FLOPPED (9 kf) and FRONTVIEW (10 kf).
- **Darwin** — GB219WATCH_Costume_MobiltyScooterPoses_DRW_ORIGINAL_PUPPET_v001 (33 kf); stock GB200_DRW_ORIGINAL_PUPPET_v001 (235 kf) in the library.
- Note: the builder's cast list also surfaces 'GB200_ORIGINAL_PUPPET_FRONTVIEW_v001' as a separate entry — it is one of Gumball's single-pose variants above, not a third character.

## Construction
- The gag is a foreground layer: GB219Watch_Props_GlassPane_v001.fxg sits on its own 'glass' scene layer over everything, slightly translucent with diagonal reflection streaks.
- The scooter sandwiches the riders: SCOOTER_FRONT_SC111_A and SCOOTER_BEHIND_SC111_A layers around the GB_MobilityScooterPose / DRW_MobilityScooterPose layers, under a folder 'DRW+GB_MobilityScooterPose_sc111_A'.
- Background: GB219WATCH_Sc111_LO_BG.jpg (bitmap plate, frames 0–68), mostly hidden behind the pane. ROUGH_Gumball (11 kf) and ROUGH_DARWIN (9 kf) DOMShape layers ship in the file.

## Techniques (tags + evidence)
- **costume-variant-puppet** — episode-specific scooter-pose puppets for both characters (30 + 33 kf) built instead of redressing the stock puppets (manual, symbol names).
- **rough-layer-shipped** — ROUGH_Gumball layer ships inside the KeyAnim file (auto).
- **face-comp-driven** — face comps 3,868 kf vs body puppets 581 kf; the squash lives in the dedicated scooter-puppet face comps (scooter GB mouth comp 457 kf) (auto).
- **layout-mov-reference** — scene carries a 'layout mov' reference-video layer (auto).

## What Cape Jones steals from this scene
- Put the gag surface on its own foreground layer: a translucent pane prop over the shot turns an ordinary approach into a squash gag — the characters animate the press, the pane sells it.
- Squash reads through face comps, not bodies: cheeks and features deforming across the glass carry the whole joke while the bodies stay simple.
- Build a pose puppet for the vehicle state (scooter poses, 30–33 kf) instead of posing the stock puppet into the vehicle every scene.

## Media status
- Contact sheet: done (68 frames). Video: done, production audio muxed from the SWF sound asset. Frames rendered: 68/68.

## Gaps / honesty
- The companion SWF is the KeyAnim pass: the render is pale line art with unfinished colour (white below the glass line, only accent colours such as Gumball's ear and Darwin's legs) and the animator's red markup circles still visible. That is the file's real state and is what the sheet shows — the construction is the lesson, not the finish.
