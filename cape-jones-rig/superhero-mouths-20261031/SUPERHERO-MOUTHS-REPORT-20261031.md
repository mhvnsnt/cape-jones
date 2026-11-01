# Superhero mouth library — pulled, Robin only — 2026-10-31

Status: DELIVERED, approval 0/1. No repo push. No existing file overwritten.
Lip-sync layer test status unchanged: DRAFT BASE DEFAULT, production REJECTED.
Visemes v2 mouths are PIL vector, hand-tooled — this library replaces them with
PULLED mouths, nothing redrawn, nothing vector-drawn.

## 1. Archive audit (name search, Teen Titans complete-v1, 970 entries)

Same archive the Robin eyes library used: repo mhvnsnt/cn-gigaleak-teen-titans,
release teen-titans-complete-v1, 970 entries, Robin files 63.
Counts re-verified by name search in this task:

- robin: 63
- batman: 0 — NO Batman-named file in complete-v1
- superman: 0 — NO Superman-named file in complete-v1
- justice: 0, league: 0, flash: 0, wonder: 0, green: 0, lantern: 0,
  aquaman: 0, joker: 0
- Other Teen Titans characters present by count (mouths NOT extracted here):
  cyborg 65, starfire 61, raven 63, beast 65, slade 16
- Other Teen Titans releases exist (teen-titans-cnleaks-v1, 10 assets;
  teen-titans-cowchicken-v1, 8 assets, mostly 100 MB parts) — NOT entry-audited,
  because that would mean downloading 18 x 100 MB parts. Do NOT claim they
  contain or lack Batman/Superman. Complete-v1 is the "complete" pull.
- No Batman/Superman/Justice League repo was verified in the show-repo audit
  beyond the one Disney repo match — do NOT claim a Batman/Superman source
  from another repo without a file in hand.

Conclusion: Batman 0 mouth files, Superman 0 mouth files, stated per character.
Every usable mouth below is Robin.

## 2. Library — 6 usable / 7 extracted = 86%

All Robin, all from Teen Titans complete-v1, Ghostscript renders already in
robin-eyes-100-20261031/render/ (Ghostscript 10.02.1, gsroot toolchain).
Method: verbatim crop from the render, then mouth-only cutout = non-skin
connected components in the measured box, pixels unchanged. Skin test:
R>190, G>165, B>130, R-G 15-115, G-B 5-105 (tightened after the first build
erased Robin's brown tongue, which passed the looser test). Grey eye-shading
excluded (max-min < 35). White teeth KEPT for EPS renders (the first build's
white-background filter erased teeth — fixed: white exclusion applies only to
the Day JPG). Costume pure red/yellow/green dropped from patches 03 and 06
only (those colours never occur in a mouth).

| id | mouth | source file | box in render | viseme | patch px | fitted on Cape head |
|----|-------|-------------|---------------|--------|----------|---------------------|
| 01 | SHOUT / AH, wide open, teeth top, tongue | 51_RBEXPRES01_CA_DCTTAS.EPS | (200,755,600,945) | AH | 54,560 | 281x134, scale 0.701 |
| 02 | CLOSED / MBP, thin closed line | 47_RBEXPRES02_CA_DCTTAS.EPS | (330,1225,480,1250) | MBP | 307 | 281x48, scale 1.861 |
| 03 | OPEN SMILE / EH, wide open, tongue, no teeth | 53_RBEXPRES03_CA_DCTTAS.EPS | (270,1085,565,1182) | EH | 12,239 | 281x93, scale 0.949 |
| 04 | SMILE / EE, closed curved smile line | 50_RBEXPRES04_CA_DCTTAS.EPS | (470,1180,630,1270) | EE | 1,678 | 267x151, height-capped |
| 05 | GRIT, wide teeth grin | 49_RBEXPRES05_CA_DCTTAS.EPS | (135,1110,665,1190) | GK (mapping) | 16,124 | 281x43, scale 0.529 |
| 06 | OPEN SMILE (model), teeth top, tongue | 23_RBN01_CA_DCTTAS.EPS | (525,695,660,780) | AH-alt | 6,821 | 239x151, height-capped |
| 07 | NEUTRAL CLOSED (Day head close-up) | 02_ROBIN_Day.jpg | (890,765,940,775) | rest | 211 | REJECTED, see below |

Fitting: Cape clean-head-base 4x (visemes-v2-20261031/clean-head-base-20261031.png,
476x688), mouth zone box 4x [111,409,392,560], patch scaled by width to zone
width (281px), centred in zone, height scaled down only if it would exceed
zone height (151px). Mouth patch lives INSIDE the head layer only, never above
head/cowl — same rule as the lip-sync layer test. No-crop rule applied:
fitted heads are the full 476x688 head, nothing clipped.

### Honest defects in the usable six (viewed, not hidden)
- 02 closed line is TWO segments with a centre gap, as pulled — it reads as
  closed-mouth corners on Cape's head, not one continuous line.
- 04 smile carries a small upper mark from the source's upper lip line above
  the main curve.
- 03 keeps thin black jaw-outline fragments at the mouth's right edge (source
  outline, verbatim).
- 01 keeps a tiny costume sliver at the mouth's lower right corner at fitted
  scale (trimmed twice; a 1-2px edge remains).

### 07 rejected, not shipped as usable
Day JPG neutral line was located numerically (dark rows x892-937, y768-773)
but is faint/compressed and mixed with nose shading. Fitted proof showed a
grey smudge plus an angular fragment, not a clean line. File kept on disk,
marked rejected-not-cleanly-extractable in the JSON. EXPRES02's closed line
is used for rest/MBP instead.

## 3. PAH GO rebuild — pulled mouths only, no PIL vector mouth

Timeline MBP -> AH -> GK -> OH, 6 frames each at 24fps = 24 frames, 1.0s.
- MBP = 02 closed line
- AH = 01 shout
- GK = 05 grit (MAPPING, not a true GK drawing — no GK-specific mouth exists
  in the Robin set)
- OH = GAP FRAME (clean head, no mouth patch). No round/oval OH or OO mouth
  exists in the Robin set. EXPRES03 open smile is the closest open shape, but
  reusing it for OH would duplicate the EH shape, so the gap is shown, not
  papered over.

Files: pahgo-pulled-mouths-20261031.gif (24f), pahgo-pulled-mouths-20261031.mp4,
pahgo-contact-20261031.png. All frames viewed via fitted heads + contact.
Second test phrase was optional ("if time") and was NOT built — not owed.

## 4. Files in superhero-mouths-20261031/
- build_library.py (builder, boxes + filters as above)
- mouth-library-20261031.json (7 entries, status usable/rejected)
- mouths/ — 7 patches, raw/ — 7 raw crops, fitted/ — 7 fitted heads
- mouth-library-contact-20261031.png (6 usable fitted heads)
- pahgo-pulled-mouths-20261031.gif / .mp4, pahgo-contact-20261031.png
- SUPERHERO-MOUTHS-REPORT-20261031.md (this file)

## 5. Still owed
- Production approval 0/1; no repo push.
- Per-viseme coverage gaps: OH/OO round mouth 0, FV 0, L/SZ/TH/R/W 0 true
  shapes. Covered by mapping only: AH, MBP, EH, EE, GK (mapping), rest (via 02).
- Other Teen Titans characters' mouths (Cyborg/Starfire/Raven/Beast Boy/Slade
  exist in the archive by count) — NOT extracted in this library.
- Batman 0, Superman 0 in complete-v1 — a Batman/Superman mouth needs a
  verified file from another source before it can be claimed.
- Second test phrase (optional, not built).
- Wiring the pulled mouths into the main lip-sync builder (mouth chart swap)
  so future dialogue tests use pulled mouths by default — the PAH GO rebuild
  here is a standalone proof, not yet the builder default.
