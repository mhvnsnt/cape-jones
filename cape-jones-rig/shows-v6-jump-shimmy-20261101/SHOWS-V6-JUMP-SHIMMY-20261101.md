# Shows: V6 + Jump-to-Shimmy, in plain words — 2026-11-01
Mars, 2026-11-01 00:30 CDT: "jump to shimmy you need to show me that ... I don't know what you mean by key sequence" and "V six you need to show those to me I don't know what that mean"
No push, no original touched. Approval 0/1 jump-to-shimmy (re-key vs drop), 0/1 V6 power candidate, 0/1 V6 rename, all separately. No decision made here.

## Key sequence, plain definition
A key sequence is just the list of poses, in order, in plain words.
Example: jump up -> land crouch -> stand -> shimmy start. It is NOT a code term.

## Jump-to-shimmy
- Jump chain: already built, 62 frames @24fps, 2.58s, AIRBORNE.
  Keys: apose f0, jump crouch f10, jump takeoff f22 (height 30px), jump tuck apex f33 (height 100px), jump land (crouch) f45.
- Shimmy chain (successor): already built, 61 frames, 2.54s, GROUNDED.
  Keys: apose f0, shimmy centre f10, shimmy sway left f22, shimmy sway right f33.
- Missing link: old V1 land pose exists ONLY as a finished picture (a rendered clip frame). It has no builder config, so it cannot be rebuilt exactly.
- Proposed re-key sequence, if Mars picks re-key (NOT decided):
  1 jump crouch -> 2 jump takeoff -> 3 jump tuck in the air -> 4 NEW land crouch (built from the rig) -> 5 stand up -> 6 shimmy centre -> 7 shimmy sway left -> 8 shimmy sway right
- If Mars picks DROP IT: jump ends at land, shimmy starts separately, successors stay 8/9 = 89%. Nothing else is lost, other 8 successors stand.
- If Mars picks RE-KEY: pose 4 is built new, successors go 8/9 -> 9/9.

## V6
- V6 = standalone gold/cyan split, NOT a level, NOT V5. V5 stays V5, old golds unchanged.
- Seam: x650 RIGHT, LOCKED (Mars 2026-11-01 00:01 CDT). Gold left, cyan right of the split line. Main show image is medium 12px at seam 650.
- Rim: outer-only by construction (dilate(alpha,N) minus alpha, plate pasted AFTER rim, interior black preserved 100%).
  Thin 6px = DEFAULT (locked 2026-11-01 00:02 CDT). Medium 12px = saved as option. Heavy/thick 20px = saved as option.
  Honest note: thin/heavy width examples in the show are the original 20261031 builds at seam 550, labelled as width examples; seam 650 is the split-line position, it applies to whichever width is chosen, it is not a different picture.
- Power candidates, labelled candidates, NO canon power named yet:
  DUAL-CHARGE: thin rim + glow under it. Two charges, gold + cyan, charging up.
  DUAL-AURA: medium rim + glow. A wider two-colour aura around the figure.
  SPLIT-OVERLAY: heavy rim + dark background. The split laid ON TOP, like an overlay.
  Note: the reused 20261031 power-candidates contact has 4 panels; top-left, top-right, bottom-left are the 3 candidates, bottom-right is a V6 medium reference, NOT a 4th candidate.
- Rename original file, plain words:
  YES = the old V6 original file gets a new name with V6 in it. You find it as V6. Its old name is gone.
  NO = the old file keeps its old name, exactly as it is now. V6 files keep their own new names. Nothing is renamed.
  Nothing is deleted either way. This is only about the name.
  Source note: the V6 original was NOT edited, NOT renamed in place, NOT overwritten in the 20261031 report; its source path is unchanged. That is why YES vs NO is still a live question.

Files:
- contacts/show-jump-to-shimmy-20261101.png (1100x1900)
- contacts/show-v6-20261101.png (1100x4917)
- Individual V6 candidates (originals, reused, not edited):
  gold-split-rim-upgrade-20261031/v6-power-candidate-1-dual-charge-20261031.png
  gold-split-rim-upgrade-20261031/v6-power-candidate-2-dual-aura-20261031.png
  gold-split-rim-upgrade-20261031/v6-power-candidate-3-split-overlay-20261031.png
