# General mouth-clean pipeline — short report
- AH-front clean: APPROVED 1/1, locked, untouched.
- SMILE34 clean: APPROVED 1/1, locked, untouched.
- Generalized pipeline: approval 0/1 separately, no repo push.
- Method, layman: remove all the stuff around the mouth without erasing the mouth.
- Method, computer: M1 colour decontamination (dark/white/orange/red classes only);
  M2 garbage/rotoscope matte, keep the dark component touching ALL main interior
  anchors (>=100 px, 2 px dilation), ANY fallback, CHAIN fallback for line mouths;
  M3 overlay erasing per frame at fit (231.5, 504.5); M4 vector line fit (already run
  in the clean-line workstream, kept unchanged here); M5 morphological opening tried
  and rejected (MBP line 67 -> 0 px, AH dark 5,748 -> 5,527 px).
- Proof run: 37 source patches, 37/37 gates PASS, source 596,523 px -> kept 583,651 px,
  dropped 12,872 px. Rules: ALL 19, CHAIN 17, ANY 1. Changed 19, already clean 18.
  Approved patches unchanged: AH-clean 9,051 -> 9,051, SMILE34-clean 3,006 -> 3,006.
- Full doc: MOUTH-CLEAN-PIPELINE-20261031.md (layman + computer terms, per-mouth counts).
- Contacts: contacts/contact-V2-7-before-after-20261031.png,
  contacts/contact-PACKS-before-after-20261031.png,
  contacts/contact-LIPSYNC-before-after-20261031.png,
  contacts/contact-APPROVED-before-after-20261031.png. Cleaned patches in cleaned/,
  fitted heads in fitted/ (37 each).
