# Cape Jones Shading Preset Library — SHD-20261031-v1

**This is a shading library, NOT a lighting library.** Shading presets are a SEPARATE axis from lighting levels L0-L5, lighting packs V5/V6, and gold presets. Do NOT file a shading preset as a lighting level, and do NOT renumber lighting levels. Pick a shading tier the same way you pick a lighting level — independently, then combine them on a shot.

**Normals warning, on every preset:** normals are ESTIMATED from silhouette distance transform (EDT ~1 px/px, Gaussian sigma 2, z-scale 1.5), NOT a true 3D mesh pass. True 3D character model normal pass is still owed 0/1. Clean apose production relight without faceting is still owed 0/1. Per-shot shading is 0/30.

**Base art untouched.** Presets live at their source paths (below); this library does NOT duplicate preset PNGs and does NOT recolour the base. Thumbnails in `thumbs/` are browsing copies only, not new presets. Base: rig-apose-v7c-clean-transparent.png, 1100x1500, mask 373,846 px, centre x561.5; arms-up mask 369,712 px, centre x550.

## How to get a preset back — retrieval (RUN)

```
python3 retrieve.py --tier CLEAN
python3 retrieve.py --pose ARMS_UP
python3 retrieve.py --light RIGHT
python3 retrieve.py --finish CEL
python3 retrieve.py --query "smooth blender apose"
python3 retrieve.py --id CORE-V9
python3 retrieve.py --tier TEST_ONLY   # REFUSED for production (exit 2) unless --allow-test
```

Proof: `retrieval-proof-20261031.txt` — 9 queries run. 8 returned presets; 1 returned NO MATCH honestly: there is NO right-facing cel preset in this library (V3 RIGHT is faceted Lambert, not cel; cel presets N04/V4 are LEFT). 1 refusal proof: `--tier TEST_ONLY` refuses for production unless `--allow-test`.

## Counts — 54 entries total

- ARCHIVE 20 (Set One, contact only) · REFERENCE 2 · CLEAN 6 · STRONG 7 · SOFT 5 · EXPERIMENTAL 13 · TEST_ONLY 1
- Plates: APOSE 51 · ARMS_UP 3 (HERO, X01-ARMS, X07-ARMS)
- Files with individual PNGs: 34. Set One: 20 entries, NO individual files exist — source is the contact sheet only, stated per entry, not invented.

## Tiers — levels of shading for him

### ARCHIVE — Set One, Mars label BARELY WORKS — DO NOT USE FOR PRODUCTION
Record of what did not work. Whole-canvas gradient / weak pseudo-normal tweak, not per-pixel form shading. Exceptions, listed separately, visibly moved but NOT true form shading: I05 side weight L (-18.2), I06 side weight R (+17.2), X08 high contrast (-6.1, crushes contrast). Rest: -14.6 to +9.6, did not read as shading.
| S1-I01 | Set One I01 lambert L | APOSE | LEFT | -10.9 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I02 | Set One I02 lambert R | APOSE | RIGHT | 9.6 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I03 | Set One I03 rim only | APOSE | LEFT | -0.8 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I04 | Set One I04 distance norm | APOSE | LEFT | -4.0 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I05 | Set One I05 side weight L | APOSE | LEFT | -18.2 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I06 | Set One I06 side weight R | APOSE | RIGHT | 17.2 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I07 | Set One I07 soft normal | APOSE | LEFT | -10.0 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I08 | Set One I08 hard normal | APOSE | LEFT | -10.7 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I09 | Set One I09 top light | APOSE | TOP | -1.0 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-I10 | Set One I10 bottom light | APOSE | BOTTOM | -0.7 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X01 | Set One X01 pseudo-depth | APOSE | LEFT | -14.6 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X02 | Set One X02 edge-aware | APOSE | LEFT | -10.6 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X03 | Set One X03 faceting test | APOSE | LEFT | -1.2 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X04 | Set One X04 dual light | APOSE | DUAL | -0.4 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X05 | Set One X05 warm/cool split | APOSE | LEFT | -10.9 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X06 | Set One X06 gradient mesh | APOSE | LEFT | -5.5 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X07 | Set One X07 inverted depth | APOSE | LEFT | 3.6 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X08 | Set One X08 high contrast | APOSE | LEFT | -6.1 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X09 | Set One X09 blur relight | APOSE | LEFT | -9.5 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |
| S1-X10 | Set One X10 no shade ctl | APOSE | NONE | -0.8 | None | BARELY WORKS — DO NOT USE FOR PRODUCTION |

### REFERENCE — controls and flaw records
V0 = no shade (edge +1.8). V1 = old G2 flaw reproduced (half -13.3, edge +0.5, FAIL as shading). Use to prove a new run actually moves form.
| CORE-V0 | control, no shade | APOSE | NONE | -3.4 | 1.8 | REFERENCE — CONTROL ONLY |
| CORE-V1 | old G2 gradient, reproduced flaw | APOSE | LEFT | -13.3 | 0.5 | REFERENCE — FLAW RECORD, DO NOT USE AS SHADING |

### CLEAN — cleanest production form, use first
Apose: V9 Blender (smooth, edge +27.6, half +0.1), V7 (half +17.4, edge +40.1, smoother), V10 (half +17.7, edge +29.6, smoother). Arms-up: HERO (half +52.0, edge +78.0), X01-ARMS (+51.4 / +75.3), X07-ARMS (+51.6 / +75.9).
| CORE-V7 | form depth + side-weight LEFT | APOSE | LEFT | 17.4 | 40.1 | DEFINITELY WORKS — CLEANEST FIRST, USE ON APOSE |
| CORE-V10 | combined normal + side-weight + AO LEFT | APOSE | LEFT | 17.7 | 29.6 | DEFINITELY WORKS — CLEANEST FIRST, USE ON APOSE |
| CORE-V9 | Blender compositor Lambert LEFT | APOSE | LEFT | 0.1 | 27.6 | DEFINITELY WORKS — CLEANEST FIRST, SMOOTH, BLENDER RUN |
| CORE-HERO | arms-up Lambert LEFT | ARMS_UP | LEFT | 52.0 | 78.0 | DEFINITELY WORKS — CLEAN + STRONG, ARMS-UP ONLY PLATE |
| CONT-X01-ARMS | edge-aware ARMS-UP | ARMS_UP | LEFT | 51.4 | 75.3 | DEFINITELY WORKS — CLEAN ON ARMS-UP |
| CONT-X07-ARMS | multiscale ARMS-UP | ARMS_UP | LEFT | 51.6 | 75.9 | DEFINITELY WORKS — CLEAN ON ARMS-UP |

### STRONG — strong form, FACETED on apose — do NOT ship as clean apose relight
High edge delta, but apose plate facets (dense interior linework + narrow limbs). The method works; the apose plate facets. Use on arms-up, or as a strength reference.
| CORE-V2 | Lambert LEFT strong | APOSE | LEFT | 3.8 | 73.9 | DEFINITELY WORKS — FACETED ON APOSE, DO NOT SHIP AS CLEAN APOSE RELIGHT |
| CORE-V3 | Lambert RIGHT strong (mirror) | APOSE | RIGHT | -8.4 | -72.4 | DEFINITELY WORKS — FACETED ON APOSE, MIRROR OF V2 |
| CORE-V4 | toon cel LEFT 3-band | APOSE | LEFT | 3.3 | 75.6 | DEFINITELY WORKS — FACETED ON APOSE, DO NOT SHIP AS CLEAN APOSE RELIGHT |
| CORE-V6 | AO + Lambert LEFT | APOSE | LEFT | 3.5 | 61.8 | DEFINITELY WORKS — FACETED ON APOSE |
| CONT-N01 | half-Lambert LEFT | APOSE | LEFT | 4.0 | 75.6 | DEFINITELY WORKS — FACETED WARNING ON APOSE |
| CONT-N04 | cel 5-band LEFT | APOSE | LEFT | 4.2 | 81.9 | DEFINITELY WORKS — FACETED WARNING ON APOSE |
| CONT-N07 | specular LEFT | APOSE | LEFT | 4.1 | 75.7 | DEFINITELY WORKS — FACETED WARNING ON APOSE |

### SOFT — mild, ambient, rim, top
Low half-mean movement, gentle form. V8 top light: left/right delta expected small (-1.8 / -1.1) — do not misread that as failure.
| CORE-V5 | three-point LEFT warm / RIGHT cool | APOSE | LEFT | 1.3 | 51.3 | DEFINITELY WORKS |
| CORE-V8 | top light | APOSE | TOP | -1.8 | -1.1 | DEFINITELY WORKS — TOP LIGHT, LEFT/RIGHT DELTA EXPECTED SMALL |
| CONT-N02 | wrap light LEFT | APOSE | LEFT | 1.9 | 55.3 | DEFINITELY WORKS |
| CONT-N03 | rim only LEFT | APOSE | LEFT | 0.3 | 43.9 | DEFINITELY WORKS |
| CONT-N08 | hemisphere ambient | APOSE | LEFT | 0.4 | 37.5 | DEFINITELY WORKS |

### EXPERIMENTAL — new methods and proxies, limits labelled per preset
All PIL runs on the same normal field. Proxy limits that must be quoted with the preset: N05 = SSS approximation only (true volumetric SSS owed); N10 = PIL ramp equivalent only (Blender Shader-to-RGB node owed); X08 = y-band proxy only (true limb segmentation owed); X01 = gaussian-smooth proxy only (true guided/bilateral filtering owed); N06 = gradient mesh, moves half-mean (+20.3) not form (edge +4.9 only).
| CONT-N05 | SSS approx LEFT | APOSE | LEFT | 2.4 | 47.7 | DEFINITELY WORKS — APPROXIMATION ONLY, TRUE VOLUMETRIC SSS STILL OWED |
| CONT-N06 | gradient mesh LEFT | APOSE | LEFT | 20.3 | 4.9 | DEFINITELY WORKS — MOVES HALF-MEAN, NOT FORM (edge +4.9 only) |
| CONT-N09 | cast-shadow falloff | APOSE | LEFT | 3.9 | 71.9 | DEFINITELY WORKS |
| CONT-N10 | Shader-to-RGB equivalent LEFT | APOSE | LEFT | 2.8 | 70.8 | DEFINITELY WORKS — PIL RAMP EQUIVALENT ONLY, BLENDER NODE RUN STILL OWED |
| CONT-X01 | edge-aware LEFT | APOSE | LEFT | 3.5 | 61.5 | DEFINITELY WORKS — SMOOTHED, STILL MOTTLED/FACETED ON APOSE |
| CONT-X02 | depth-dark LEFT | APOSE | LEFT | 3.3 | 58.6 | DEFINITELY WORKS |
| CONT-X03 | linework-aware LEFT | APOSE | LEFT | 3.9 | 73.8 | DEFINITELY WORKS |
| CONT-X04 | chromatic wrap LEFT | APOSE | LEFT | 3.6 | 73.9 | DEFINITELY WORKS |
| CONT-X05 | dual-key cross | APOSE | DUAL | -2.2 | 16.6 | DEFINITELY WORKS — NO SINGLE SHADOW SIDE |
| CONT-X06 | diagonal light | APOSE | DIAGONAL | 2.9 | 54.5 | DEFINITELY WORKS |
| CONT-X07 | multiscale smooth LEFT | APOSE | LEFT | 3.6 | 65.0 | DEFINITELY WORKS — SMOOTHED, STILL MOTTLED/FACETED ON APOSE |
| CONT-X08 | per-zone LEFT | APOSE | LEFT | 3.5 | 71.3 | DEFINITELY WORKS — Y-BAND PROXY ONLY, TRUE LIMB SEGMENTATION STILL OWED |
| CONT-X09 | rim + AO power | APOSE | LEFT | 3.2 | 63.1 | DEFINITELY WORKS |

### TEST_ONLY — DO NOT SHIP
| CONT-X10 | inverse TEST ONLY | APOSE | RIGHT | -8.6 | -72.0 | TEST ONLY — DO NOT SHIP |

## Master contact and per-tier contacts

- Master contact (12 representatives, one per tier + cleanest first): `shading-preset-master-contact-20261031.png` — viewed before reporting.
- Per-tier contacts in `contacts/`: tier-archive, tier-reference, tier-clean, tier-strong, tier-soft, tier-experimental, tier-test_only.
- Set One tier contact is a single tile of its contact sheet, labelled as such, because no individual Set One files exist.

## Industry-standard organization — what was pulled in, RUN vs MAPPING

RUN in this folder (local implementation, not a vendor claim):
1. Shader-library taxonomy — tier + tags + version (SHD-20261031-v1), after Blender Asset Browser / Substance 3D Assets category-and-tag practice.
2. Tag search index — every entry carries tier, plate, light direction, finish, source set, smooth/faceted tags; `retrieve.py` searches them.
3. Preview thumbnails + contact sheets per category — standard asset-browser preview practice.
4. Versioning + deprecation log — see CHANGELOG-DEPRECATION-20261031.md.
5. Retrieval-by-intent — pose + light + finish + tier queries, with a production refusal for TEST_ONLY/ARCHIVE.
6. Parameter record per preset — half-mean delta, edge delta, method, run, proxy note, in the JSON catalog, so a preset can be recreated or compared without reopening the image.

MAPPINGS only, with reason not run:
- Blender Asset Browser (GUI asset browser, not run headless here; catalog format mirrors its category/tag/preview model).
- Substance 3D Assets / Adobe shader library (paid/vendor, not run, no purchase).
- Unreal Material Library / Unity Shader Graph library (engine libraries, not run; taxonomy only).
- MaterialX / USD material naming (standard naming practice, not a MaterialX file export — none claimed).
- OpenColorIO / ACES view-transform handling for the V9 Blender-vs-PIL gap (gap investigation still owed 0/1, not claimed resolved).

## Added beyond the brief, and why

- Thumbnails (34) + per-tier contacts (7) + master contact: browse and sort without opening 34 full 1100x1500 plates.
- Retrieval refusal for TEST_ONLY/ARCHIVE: stops a test preset being shipped by accident.
- Gap finding: NO right-facing cel preset exists — recorded, not invented. A right cel is a new build if Mars wants it.
- Deprecation log: Set One superseded by Set Two; V9 sRGB first run (+25.7) superseded by Non-Color run (+27.6); V1 flaw record kept, not deleted.
- Cross-axis warning on every catalog entry: shading ≠ lighting, so a future agent cannot file a shading preset as L4/L5 or V5/V6.

## Still owed

Library approval 0/1. No repo push. True 3D normal pass 0/1. Clean facet-free apose relight 0/1. Per-shot shading 0/30. Blender-vs-PIL V9 gap investigation 0/1. True volumetric SSS 0/1. Blender Shader-to-RGB node 0/1. True limb segmentation 0/1. Right-facing cel preset 0/1 (new build, if wanted).
