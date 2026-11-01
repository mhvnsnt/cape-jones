# CHARACTER BIBLE — consolidated document (wiring-100-20261031)
This is the consolidated INDEX + construction document TV-08 owed. It does not
create new character art and does not approve any version.
- Rig: joint_locked_rig_v7c.py, pivots 4/4, T-pose / A-pose lock (TPOSE-LOCKED-v8).
- Gauntlet flip rule: GAUNTLET-FLIP-RULE.md, regression check_gauntlet_flip.py 5/5 (prior).
- Wrist rule: wrist end to forearm end (wrist-attach-fix-20261031/check_wrist_attach.py).
- Snap rules: face / cowl / chest snap gates (face-cowl-snap-wire100-20261031/check_pose_snap.py).
- Eyes: pack4 eye strips 8/8 (prior). Cape states: cape-styles-v2 15 styles + cape-consumed
  bare / upper-only-collar variants (prior folders, not overwritten here).
- Visemes: 14/14 (visemes-v2-20261031/head-v2-01..14), see lip-sync-strip in this folder.
- Turnarounds on file: front = rig-apose-v7c-clean-transparent.png; back =
  showcase/model-back.jpg; 3/4-back = showcase/model-3quarter-back.jpg.
  HONEST GAP (art, not wiring): a true hand-drawn 3/4 head/torso is still owed;
  the 3/4-back file above is a stand-in reference, not claimed as that drawing.
  The bible document itself is wired (1/1); the hand-drawn 3/4 art remains owed as art.
- Colour: base art is never recoloured; light/shadow/rim/bleed are separate layers
  (apply_compositor.py layer order). Rim follows key / shifted key within +/-20 deg
  (RIM-COLOR-RULE.md), dual-light exception only where the shot spec names it.
- Scale: room 2.5x standing (rig 950px), seated 2.3x; feet anchor = alpha-bbox bottom.
- Version-lock: every shown version gets a new dated file, never overwritten.
