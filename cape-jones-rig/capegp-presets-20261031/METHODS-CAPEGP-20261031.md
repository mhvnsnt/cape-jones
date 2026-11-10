# CapeGP methods — industry-standard layer / linework wiring

Counts: 11 methods named. Real runs in this pack: Blender GP build +
renders, cv2 tracing, Chaikin smoothing, joint-cleanup reference reads.
Method mappings (named, wired as a layer rule or a parameter, NOT a run
in that vendor tool): Harmony, Animate, Godot, Spine, OpenToonz/Tahoma2D,
traditional cel. No vendor tool is claimed to have run when it did not.

| # | Method | Source / standard | How it is wired into CapeGP | Run or mapping |
|---|--------|-------------------|------------------------------|----------------|
| 1 | Blender Grease Pencil layer tree + material per layer | Blender 5.2.3 GP | CapeGP object, 10 layers in fixed order, one GP material per layer, use_lights=False | REAL RUN (build_capegp.py, renders) |
| 2 | Harmony Z-depth + drawing substitution | Toon Boom Harmony cut-out workflow | Snap presets map to Z-order: FaceSnapArm above Head, CowlUpperArm above Collar, ChestSnapArm above Torso — same decision as Harmony's Z-depth, implemented as GP layer assignment | MAPPING (Harmony trial download pending, not run) |
| 3 | Animate reparenting / layer order | Adobe Animate timeline layers | Preset = a layer reparenting: move an arm chain to a different layer without moving its geometry (COWL_SNAP lowers stay put, uppers move) | MAPPING (Animate sign-in pending, not run) |
| 4 | Godot Z + draw order | Godot 2D Z index / draw order | Layer index = draw order: index 0 draws first (front). CapeGP layer list order is the draw order, documented in README | MAPPING (rule wired, Godot project not built) |
| 5 | Spine keyable draw order | Spine draw-order keys | Each preset is a draw-order key: same geometry, different layer per preset; a new preset is a new key, not new art | MAPPING (Spine paid, not run) |
| 6 | OpenToonz / Tahoma2D layer SO values | OpenToonz column / SO (stacking order) | CapeGP front-to-back list maps 1:1 to a column SO list; a port script would emit layers in this order | MAPPING (GUI not run) |
| 7 | Traditional cel stacking | Traditional animation cel layers | Face/cowl/chest snaps are cel stacking: the arm cel goes above the head/collar/torso cel for the frames it crosses them | MAPPING (method, not a tool) |
| 8 | Line weight by depth | Industry linework practice | STATED AS OWED, not built: current radius is fixed 0.035 for all layers. Next pass varies radius by layer/depth (front thicker, back thinner) | OWED, not claimed |
| 9 | Interior linework | Industry linework practice | STATED AS OWED, not built: current strokes are external contours only (cv2 RETR_EXTERNAL). Interior lines need a separate interior-contour pass | OWED, not claimed |
| 10 | Colour fills | GP fill / material fill | STATED AS OWED, not built: current strokes are outlines only, no fills | OWED, not claimed |
| 11 | Joint smoothing (see JOINT-SMOOTHING doc) | GP stroke smoothing / simplify + cutout joint practice | Chaikin corner-cutting x2 on every stroke polyline in JOINT_SMOOTH preset; taper / cap-omission / seam-masking from joint-cleanup as method reference | REAL RUN (Chaikin on traced data) + REFERENCE (clean_joints.py) |

## Joint-smoothing methods pulled in (detail in JOINT-SMOOTHING-20261031.md)
- Grease Pencil stroke smoothing / simplify: Chaikin corner-cutting, run here.
- Joint taper: corridor taper from clean_joints.py (method reference, not
  re-run on GP strokes here — taper applies to filled silhouettes, GP here
  is outlines; a taper pass on outlines would shrink the outline, so it is
  documented as the wrong tool for outline strokes, not faked).
- Overlap / cap placement: upper and lower pieces already overlap at the
  ball-centre pivot in v7c tracing, so the joint reads continuous; cap
  strokes are included in the same layer as their limb, not a separate
  floating ball.
- Deformer smoothing: Blender lattice / curve deformer concept, mapping
  only — the Chaikin pass is the implemented equivalent for polylines here.
- Seam masking: clean_joints.py seam-mask (dilated union) as reference;
  for GP outlines the equivalent is keeping upper/lower/cap strokes in
  one layer so no layer edge cuts the joint in half.
