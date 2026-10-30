# Cape Jones — 3D dance proof

A 20-second looping dance proof for Cape Jones, rendered in Blender (EEVEE)
from the repo rig `3d-assets/cape-jones-rig/cape_jones_mpfb_wired.blend`.
The world cycles around him — day → LED magenta → LED cyan → night → day —
while the dance (a 48-frame step-touch loop with a shrug accent) repeats.
Sections 2 and 4 are mirrored for variety, as in v1.

## v2 — what was wrong with v1, and what changed

Owner's verdict on v1: *"he's too still and reads unrigged, and has a
tattered cape, and should be moving more naturally... but still some comedic
snappiness to reference he's still a cartoon character even in his 3d form."*

Measured on v1 (see `docs/production/MOVEMENT-GAP-RESEARCH.md`): 8 held
poses with zero in-between frames, whole-body travel ~8% of body width, and
a cape that never moved at all. v2 rebuilds all three faults:

1. **Motion is real keyed rig animation now.** A 48-frame step-touch loop
   (13 pose anchors: shift → lift → plant wide → close → mirror → bigger
   second half → arms rise → **shrug snap** → settle → release) keyed on the
   FK bone chain (pelvis, spine, chest, neck, head, thighs, shins, feet,
   upper arms, forearms, hands), tiled 10× over 480 frames. Interpolation
   is smooth Bézier everywhere **except** the shrug and the nod, which are
   keyed linear so the accent lands as a snap — comedic snappiness as
   seasoning, not as the base motion. Weight transfer is in the keys:
   pelvis shifts ±5 cm, dips 3.6–4.2 cm onto the planting leg, knees bend,
   the trailing foot rolls, head turns/nods/tilts against the chest twist.
2. **The cape is fixed at the model.** Forensics on the rig found three
   separate cape faults: the `CapeJones_Cape` object is an un-skinned patch
   slab (no armature modifier — it could never move); the body mesh's own
   cape is a multi-island scan whose inter-island slots show through as
   tears; and its low side panels hang as separated ribbons. v2 deletes
   the slab, trims the ribbon panels, adds three cape bones down the spine
   (chest-children) with a height-gradient weight blend so the cape sways
   and flutters 3 frames behind the body, and covers the scan cape with a
   clean one-piece parametric cloth sheet whose radius at every angle and
   height is the scan cape's **measured** radius + 12 mm — one whole cloth
   in every frame, verified on zoomed front/back/hem stills at the motion
   extremes.
3. **Bone-channel signs were measured, not guessed.** Two probe passes
   keyed single bones ±30° and read back world positions: arm lowering is
   rotation −X on both upper arms (v1-style Z keys only swing the arms
   fore/aft), leg abduction is −Z left / +Z right, cape sway/fluter axes
   confirmed. The v2 choreography is built on the measured map.

Rendering at the full 910k-vert scan resolution costs ~50 s/frame on this
box, so the body is decimated for the render copy (evaluated-mesh
writeback at 0.35 × 0.30 ≈ 120k verts, vertex groups preserved) — eval
drops to ~0.2–0.5 s/frame and the silhouette/material read is unchanged
at 960×540.

Movement-spec verification (research doc §5 method, measured on the final
video's first loop): **torso-band travel 10.0% of body width** (spec ~10%;
v1 measured 7.7%), **foot-band travel 14.9%** (v1: 8.1%), foot/torso ratio
1.49 (spec ≥ 0.5), and **40 of 48 frames distinct** (v1: 8 held poses).
Pelvis travel is 16.4 cm peak-to-peak across the loop. The cape passes the
zoom checks (front, back, hem close-up at the deepest-dip frame): one
continuous cloth, no slots, no separated ribbons.

## Files

- `build_dance.py` — stage A: loads the rig, repairs the cape, builds the
  backyard set + section lighting, keys the dance, saves `scene_v2.blend`.
- `render_frames.py` — stage B: `check` renders low-res verification
  stills (front loop phases, back views, back hem close-up); `frames FS FE`
  renders the JPEG sequence (skips frames already on disk — resumable).
- `make_chiptune.py` — the track (unchanged from v1): a 20.0 s chiptune
  loop generated in pure Python, exactly 480 frames at 24 fps.

## Build

```sh
BLENDER=~/workspace/tools/blender/blender-4.0.2-linux-x64/blender
RIG=3d-assets/cape-jones-rig/cape_jones_mpfb_wired.blend   # repo path
xvfb-run -a env -u PYTHONPATH $BLENDER -b $RIG --python build_dance.py
xvfb-run -a env -u PYTHONPATH $BLENDER -b scene_v2.blend --python render_frames.py -- check
xvfb-run -a env -u PYTHONPATH $BLENDER -b scene_v2.blend --python render_frames.py -- frames 1 480
python3 make_chiptune.py   # writes music.wav (20.0 s)
# assemble: sections 1-96 / 97-192 (hflip) / 193-288 / 289-384 (hflip) / 385-480
ffmpeg -framerate 24 -start_number 1   -i frames/f%04d.jpg -frames:v 96 -c:v libx264 -crf 18 -pix_fmt yuv420p seg1.mp4
ffmpeg -framerate 24 -start_number 97  -i frames/f%04d.jpg -frames:v 96 -vf hflip -c:v libx264 -crf 18 -pix_fmt yuv420p seg2.mp4
ffmpeg -framerate 24 -start_number 193 -i frames/f%04d.jpg -frames:v 96 -c:v libx264 -crf 18 -pix_fmt yuv420p seg3.mp4
ffmpeg -framerate 24 -start_number 289 -i frames/f%04d.jpg -frames:v 96 -vf hflip -c:v libx264 -crf 18 -pix_fmt yuv420p seg4.mp4
ffmpeg -framerate 24 -start_number 385 -i frames/f%04d.jpg -frames:v 96 -c:v libx264 -crf 18 -pix_fmt yuv420p seg5.mp4
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\n" > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -i music.wav -c:v copy -c:a aac -b:a 160k -movflags +faststart cj-dance-proof-3d-v2.mp4
```

Output: `cj-dance-proof-3d-v2.mp4` — 20.0 s, 960×540, 24 fps.
