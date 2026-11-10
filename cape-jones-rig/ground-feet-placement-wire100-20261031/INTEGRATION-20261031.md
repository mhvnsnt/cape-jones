# INTEGRATION — how the gate is wired into existing builders

No original builder file was edited in this task (task rule: no existing
file overwritten). Wiring is therefore: (a) an importable mandatory
check, (b) re-gating wrappers that actually run on existing outputs,
(c) exact insert lines for the next edit of each builder, below.
A builder is not "wired" until its own gate run exits 0 on a delivery
and 2 on a floating delivery — the wrappers prove that shape now.

## Importable check
    from wrappers.gate_mandatory import pre_delivery_check
    pre_delivery_check({"shot": "CJ-01", "mode": "GROUNDED",
                        "ground_y": 700, "feet_y": measured_feet_y,
                        "feet_centre_x": measured_cx,
                        "figure_height": measured_h})
    # FAIL raises SystemExit(2). PASS returns the verdict dict.
    # Optional: pre_delivery_check(spec, log_path=".../delivery-log.jsonl")

Feet values passed in MUST be measured (ground_gate.plate_feet or
composite_feet), never a builder's claimed paste coordinate. The proof
shows why: paste feet 700 measured 693 (light-foot fringe, -7 px),
paste feet 653 measured 646 (-54 px offset, -47 intended float + -7
fringe). The gate's tolerance (10 px) absorbs the fringe, not the float.

## Wrappers (run, not just documented)
    python3 wrappers/check_existing.py multiplane   # BARS 24/24, exit 0
    python3 wrappers/check_existing.py size         # walk 44/44 + power 54/54, exit 0
    python3 wrappers/check_existing.py dual         # portrait A PASS + old FAIL, exit 0 (discriminates)
    python3 wrappers/check_existing.py rig          # proof figure, exit 0
    python3 ground_gate.py --composite P --background BG --mode GROUNDED --ground-y 700
    python3 ground_gate.py --plate P.png --mode AIRBORNE --ground-y 700 --height 180 \
        --flight-line "hover 180px above floor"

## Exact insert points (for the next builder edit, not applied here)
- multiplane (build_multiplane_upgrade.py): after feet_y_world is
  computed per frame, call pre_delivery_check with mode from the shot
  spec (default GROUNDED, never assumed from the pose alone) and
  ground_y = ground_line_y_world. BARS spec already carries
  ground_line_y_world = 700.
- size (build_size_power.py): after each frame's feet_y is computed,
  call the sequence check at the end of the template (it already
  records feet_y_all; feed that list to check_sequence, GROUNDED).
  Size ground_y = 1500, canvas 1600x1800.
- dual-orientation (dual_orientation.py + check_room_scale.py):
  portrait: rug mode (rug_far 1421, rug_near 1868, planted band
  [0.55, 0.95]) plus the existing furniture-ratio gate; landscape:
  ground line mode on the master scene (feet 1550) plus the landscape
  scale gate. Do NOT quote the old 0.607 frame-ratio gate as a ground
  gate — it passed a 17.6% furniture regression.
- rig poses (joint_locked_rig_v7c.py and successors): plates are
  transparent with no ground in the file. The builder must supply
  ground_y AFTER scaling/pasting (the paste coordinate is not the
  measurement; re-measure with plate_feet/composite_feet and then gate).
  A rig pose with no shot spec and no ground reference must FAIL
  with "NO GROUND REFERENCE", not ship unlabelled.

## Shot spec fields (required from now on)
    mode: "GROUNDED" | "AIRBORNE"   (required, no default)
    ground_y: int                    (GROUNDED line, or AIRBORNE reference)
    rug_far / rug_near: int, int     (rug mode, alternative to ground_y)
    height_px: int                   (AIRBORNE, required, > tolerance)
    flight_line: str                 (AIRBORNE, required, e.g. "hover 180px above floor")
    feet_y / feet_centre_x / figure_height: measured, not claimed
