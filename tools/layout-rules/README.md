# layout-rules — deterministic interior layout engine

Replaces "AI guesswork" placement with a contract + validator + applier:

1. **`living_room_layout.json`** (lives in `3d-assets/`) — the layout contract.
   Every furniture item: footprint, target position, rotation, anchor relation
   to the owner's reference drawing. This file is the ONLY thing a human edits.
2. **`layout_rules.json`** — the interior-design rule corpus (walkway 0.91 m,
   sofa↔coffee-table gap 0.40–0.46 m, TV viewing 1.5–2.5× diagonal, door-swing
   clearance, zero overlap). Sources: Coohom room-planner + floor-planner
   guides, FasterCapital arrangement guide (verified 2026-10-16).
3. **`validate_layout.py`** — headless checker. No Blender, no GPU:
   `python validate_layout.py 3d-assets/living_room_layout.json`
   Fails loudly on out-of-bounds, overlaps, blocked walkways, bad gaps,
   TV distance/angle violations. Fix the JSON, not the scene.
4. **`apply_layout_blend.py`** — headless Blender applier. Moves ONLY the
   named furniture objects to the validated transforms. Never touches
   materials, colors, LED walls, or scene settings. Idempotent.

## Workflow (build lane)

```
# 1. edit the contract (anchors from the owner's drawing)
nano 3d-assets/living_room_layout.json

# 2. validate (fast, no GPU)
python tools/layout-rules/validate_layout.py 3d-assets/living_room_layout.json

# 3. apply + render previews
xvfb-run -a env -u PYTHONPATH <blender> -b 3d-assets/living_room.blend \
  --python tools/layout-rules/apply_layout_blend.py -- \
  3d-assets/living_room_layout.json --preview-out /tmp/cj-previews/

# 4. owner judges the renders; loop back to step 1
```

## Staging order (owner law 2026-10-16)

Furniture placement FIRST → then window + doorway (Archimesh, Blender-bundled,
for clean wall holes) → then wall decor → then the ghost-cave basement.
The character seat stays EMPTY until the real rig lands for the light-flicker gag.

## Why not a neural layout model?

See `docs/research/AI-SCENE-LAYOUT.md` §1. Every verified generator
(ATISS, DiffuScene, Holodeck, Infinigen…) invents layouts from learned
distributions — they cannot reproduce the owner's specific drawing. The
stealable pattern (from Holodeck) is *constraints → deterministic solver*,
which is exactly what this folder implements without the API key, the GPU,
or the Unity install.
