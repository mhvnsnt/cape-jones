# Fist v5 — pulled from Mars's uploaded fists, cut out, fitted

## Correction, plainly
V4 was PIL vector shapes drawn by code. That IS hand-tooled in effect, NOT a generated or pulled fist image. Do not call a vector-drawn piece "generated" again. V4's report wording was wrong on that point.

## Source (superseding, Mars 17:09 CDT)
- Mars's own upload: workspace/user/files/1000179204_34_scne.jpg — two front-facing fists side by side on a beige background, knuckles at top facing camera, near-white, black outline.
- These two uploaded fists ARE the source. The earlier SmackDown search is superseded as the main source and was NOT used for the v5 shape. (For the record, that search did find the SmackDown stage fist: the giant metal fist centred above the entrance, debuted August 16, 2001, used 2001-2008, with shattered-glass panes — but Mars's upload replaced it, so no SmackDown image is in v5.)
- No WWE logo, no wrestler character, no branding is shipped in v5. Fist shape only, from Mars's upload.

## Method — pulled + cut out + fitted, NOT generated, NOT hand-drawn
1. Split the upload at the midpoint gap between the two fists (left crop x0-254, right crop x255-509).
2. Flood-fill from the borders through beige (243,230,213) pixels; the black outline encloses each fist, so the near-white interior (249,248,243) is NOT flooded out. Largest component kept per crop. Result: 189x169 px each, identical size, symmetric pair.
3. 1px feather on alpha (Gaussian 0.8). No beige halo remains; background is transparent.
4. Desaturation: chroma reduced to 15% of original (luminance preserved) — near-white glove, black outline stays black, finger lines intact. No shapes redrawn, no vector polygons.
5. Seating: each fist rotated 180° in-plane so knuckles go to the strike edge (bottom) while still facing camera. Old fist erased below y=88 on the v3 standard-clean forearm (first attempts at y=115/125 left old-fist peek-through; those were discarded and rebuilt). New fist 170px wide, top at y=65, seated over the cuff/wrist, 320x300 canvas.
   - Arm2 = LEFT source fist (thumb bottom-right in source -> thumb top-left after rotation, per Arm2 thumb-left rule).
   - Arm1 = RIGHT source fist (thumb bottom-left in source -> thumb top-right after rotation).

## Files
- fist-left-v5-20261031.png — 189x169, transparent, knuckles top
- fist-right-v5-20261031.png — 189x169, transparent, knuckles top
- forearm-v5-arm2-front-punch-fist-20261031.png — 320x300, seated Arm2
- forearm-v5-arm1-front-punch-fist-20261031.png — 320x300, seated Arm1
- proof-v5-source-cutouts-seated-20261031.png — proof sheet (grey-128 background for viewing only)
- cut_fists.py, seat_fists_v3.py, build_proof.py — builders (cut/seat, not drawing)

## Honest residual
- After the 180° rotation, the source's bottom thumb detail sits at the wrist end of the seated fist, largely tucked behind the cuff, so the seated fist reads as knuckles-forward with finger lines and no prominent side thumb. That is the source shape as fitted, not a redrawn thumb.
- The small white shape peeking at the top side of each seated fist is the forearm cuff's lower edge, not leftover old fist (old fist was erased below y=88 and verified by viewing).

## Still owed
- Mars approval: 0/1.
- Full punch pose integration: 0/1 (pieces + seated forearms built, full pose not built).
- No repo push made in this task.
