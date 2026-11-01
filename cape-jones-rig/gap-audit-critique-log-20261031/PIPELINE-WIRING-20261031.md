# Pipeline Wiring — Gap Closure (2026-10-31)
## How each closed gap is wired into the pipeline (not just filed)

Stage order (UNIVERSAL-PIPELINE + PIPELINE-TEMPLATE, unchanged; this file
adds the new gates and outputs to those stages, it does not replace them):

1. POSE — rig v7c, labels=False clean only. New gates, in order:
   - Hand first (C-02): elbow, forearm direction, fist vs flat, palm/thumb,
     then cuff piece. Gauntlet flip = per-row, cuff only.
   - Knee-feet first (C-01): knee direction = foot direction, same angle.
   - Fist-view naming (C-04): knuckle-front / palm / back / side. A punch
     pose uses knuckle-front only. v3 = palm-facing, v4b = knuckle-front.
   - Wrist seam (C-05): cap behind fist, no ring across fist face, no gap
     rows; flex poses named anticipation / true-final / over-flex.
   - Alignment QC (gap-close-rig alignment_qc_gap_close.py): run on every
     new punch/flex pose; v4c scored 11/11 PASS.
   - ARM SNAP GATE (standing, wire-100 2026-10-31): BEFORE any pose
     ships, run face-cowl-snap-wire100-20261031/check_pose_snap.py
     from the pose angles (a flat PNG cannot prove layer order after
     the fact). Exit 0 = PASS, exit 1 = FAIL. Rules: FACE (lower vs
     head > 5000) = whole chain above head; COWL = UPPER ONLY above
     the collar, and only with a recorded eye-check (whole-chain cowl
     is BANNED — it covers JoJo 02's face); CHEST (lower vs torso
     > 1000) = warning for eye-check, FAIL only if the eye-check says
     the upper is eaten and no snap was applied. Priority FACE > COWL
     > CHEST, per arm, never a whole-pose blanket reorder. New poses
     render with snap_figure.py (normal / chest / cowl-upper / face
     passes); frozen approved-pose builders are not edited — the gate
     sits in front of them. Full audit: 31 entries / 62 side-checks,
     FACE 3%, COWL-CANDIDATE 15%, CHEST 13%, NO SNAP 69%; new fixes
     Ginyu 03 + v7c-jump cowl-upper, approval 0/1 each.
2. EXPOSURE / TIMING — timing written in frames before in-betweens.
   Punch CJ-01: windup 6 / snap 2 / impact hold 12 / recover 6 @24fps.
   Smear = a drawn frame, never a blur filter (method draft in gap-audit).
   Silhouette gate: action must read at 110px thumbnail, or re-stage.
3. CAPE — separate prop rig, never baked into body. Bone-chain
   (B0 neck → B1 → B2 → hem fan L/C/R), lag 1–2 frames, settles AFTER
   the body (gap-close-rig diagram + composite).
4. COLOUR — two dialects, kept separate, composable:
   - Dialect 1 (lighting): LUT first (approved 70/70), rim follows key
     ±20°, bleed, cool shadow. Standard view = strict Rec.709 gamma 2.4
     finish; ACES 1.3 / 2.0 are creative looks (measured darker/greyer),
     never the L5 finish unless Mars says so.
   - Dialect 2 (JoJo shift): palette REPLACEMENT, not a gain. Cape = full
     colour, suit = white OR changed, choice = cool-first per beat.
     Shot spec must name trigger + palette + scope + duration +
     return-to-base, or it is not a shift. Rim under a shift follows
     the SHIFTED key. Mixed shots labelled MIXED (C-07).
5. LIGHTING / EFFECTS — Level 2 = no god rays, ever. Level 3 = Blender
   volumetric god rays + bleed + shadow interaction (PIL composites in
   this audit are labelled PIL and are proof, not production L3).
   Production-effect gate (C-10): spill + shadow + atmosphere, or it is
   a draft. Effects wiring map (sound-edit chunk) assigns systems to
   CJ shots; a system with no shot-spec field is PROPOSED, not wired.
6. SOUND / LIP-SYNC — 5 layers (dialogue/SFX/music/ambience/device beep),
   -14 LUFS target, measured value reported even when it misses
   (demo measured -16.27). Visemes v2, mask-first: base head carries NO
   mouth; old mouth + cheek lines masked with skin BEFORE the new mouth
   draws (C-09). Real dialogue timing comes from recorded audio only.
7. CAMERA / EDITING — 180° rule: camera stays on one side of the axis
   for a whole sequence; crossing flips left/right and is re-shot, never
   fixed by flipping a frame in post. EDL: cuts only unless a spec says
   otherwise; assumed holds are flagged ASSUMED in the EDL, never
   presented as spec claims.
8. QC / DELIVERY — automated QC over all 30 shot specs (TV chunk):
   required fields, LUT in approved 70/70, rim ±20° (or FAIL, as for
   CJ-05/06/26), god-ray decision, audio cue, label gate (0 strong-red
   pixels). Safe areas are percentage-based only (action 90%, title
   80%) until Mars sets the delivery frame size. Version-lock: a file
   Mars has seen is never overwritten; new versions get new dated
   filenames; chat delivery is embedded images, audio as links only.
9. ARCHIVE — TV archive manifest (68 files) + this audit's file lists
   are the reassembly order. Nothing in this audit was pushed; the push
   workstream lands it PR-only, gate-checked, verified on main by
   size + SHA after merge (see PUSH-HANDOFF-20261031.md).
