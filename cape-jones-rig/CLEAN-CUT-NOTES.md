# Clean-cut rule — Cape Jones (Mars, 2026-10-31, standing)

No square-crop hand tooling. Every slice, every time, uses
`slice_clean.py` in this folder:
- background colour from sheet corners, mask by distance from that bg,
- morphological closing + hole fill so black outlines do not fragment a piece,
- connected components found by the sheet itself (no hand rectangles),
- 1px alpha feather + fringe decontamination (unmultiply edge pixels away
  from bg colour), trim to the component silhouette only.
Remained honest about AI removal: rembg was NOT installed here, and on
2026-10-25 a rembg run in the title-creatures lane timed out/killed at
~335s with no model landed (U2-Net ~1.02 GB at ~700 kB/s). A rembg
install in a venv under this folder was started 2026-10-31 to test the
small u2netp model; it is NOT the default until a test on the exact sheet
beats the scripted method. For flat gray/black production sheets the
scripted method is the correct professional method — AI removal risks
eating the black cape on a black sheet and the white suit on a gray sheet.
That test result, when it lands, replaces this paragraph, it does not
retroactively claim rembg was used.
Pack 1 clean proof: pack1-clean/ 25 pieces, same count as the zone method,
contact sheet pack1-contact.png eye-checked clean, no gray boxes.

UPDATE 2026-10-31 ~10:05 CDT — rembg test, evidence not assumption:
- Install succeeded in cape-jones-rig/venv (rembg + onnxruntime, "rembg ok").
- u2netp per-crop: Pack1 UpperArm crop 2.3s, clean; cape crop 2.4s, clean,
  opaque 343,007 vs scripted 295,238 — rembg recovered more dark cape edge.
- u2netp FULL Pack1 sheet: 3.1s, opaque only 296,309 vs scripted 521,940,
  eye-checked ghosting/fading — right/bottom pieces fade out, hands almost
  gone. u2netp is a single-salient-object model, it is NOT a multi-island
  sheet tool.
Wired pipeline going forward, every time:
1. Full sheet -> slice_clean.py component method (proven 25/25 Pack1).
2. Single-piece crops, especially black-on-black (cape), -> rembg u2netp
   as a check/second pass; keep whichever silhouette is fuller with no ghosting.
3. NEVER rembg a full multi-piece sheet with u2netp.
Test files: pack1-rembg-full.png, rembg-test-pack1-upperarm.png, rembg-test-cape.png.
