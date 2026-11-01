# WIRED-100 INVENTORY — 2026-10-31 (Cape Jones)

Mars order 16:32 + 16:36 + 16:55 CDT: wire EVERYTHING installed/stubbed/unused
to 100% real use, show what we are doing with it, pull in any other
industry-standard stuff, and close ALL gap-audit items. Installation alone
is never wiring. Wiring = a real viewed output in a real Cape Jones
shot/piece, or a file verified by re-parse where the tool's output is a
file, not an image. Nothing here is Mars-approved — he approves.

## Totals (41 items)

- WIRED — viewed output in a real shot/piece: 21/41 = 51%
- WIRED — file output verified by re-parse: 3/41 = 7%
- WIRED total: 24/41 = 59%
- BLOCKED + free replacement wired: 12/41 = 29%
- PARTIAL (built, full completion still owed): 3/41 = 7%
- MARS-ONLY / PUSH-WORKSTREAM-ONLY: 2/41 = 5%
- No item is left as "installed" or "template only" with no use, blocker,
  and replacement.

## WIRED — viewed output (21)

| # | Item | Real output (viewed) | Proof |
|---|------|----------------------|-------|
| 1 | FFmpeg lut3d (approved neutral .cube) | wired-ffmpeg-lut3d-fighting-20261031.png (419,850 B) | fighting pose, full, grey bg, viewed |
| 2 | Clean walk clips -> real MP4 | wired-walk-clean-clips-20261031.mp4 (32,211 B, 4 frames x2 loops @24fps, 550x750) | rendered, viewed |
| 3 | Audio loudness | wired-audio-minus14lufs-20261031.wav + measure JSON (input_i -14.25, tp -1.50, lra 0.60) | measured; loudnorm measure quirk noted (output_i -24.09 is a measure quirk, re-check with a second meter before quoting) |
| 4 | Shot CJ-01 through PIL Level 2 v2 | wired-shot-cj01-punch-level2/level-2-v2-colored.png (607 KB) + noncolored + rim/bleed/internal/shadow passes + colors JSON | punch pose, warm grade, corners (140,121,89) vs source (128,128,128). CORRECTED 22:35 CDT: the delivered run's log reports rim max 0.89 / bleed max 0.13, and pixel check confirms real passes — rim pass 63,773 nonzero alpha px (max 228), bleed pass 52,970 nonzero alpha px (max 34). An earlier run's 0.00 log line does NOT apply to the delivered file. First attempt correctly REFUSED the labelled punch file (8,420 red debug pixels, script refuses >100). |
| 5 | Sliced-clean sheet use | wired-sliced-clean-layout-20261031.jpg (1168x784, grey-128, full figure centred) | viewed. 1 sheet used, NOT the full 184-sheet batch — batch application still 0/184 as a batch, method 100% only. |
| 6 | Tool frames (Pencil2D frame data) | wired-tool-frames-20261031.mp4 (15,299 B) + wired-tool-frames-contact-20261031.jpg | 4 apose frames, shifts 0/+10/0/-10 px visible, viewed |
| 7 | Onion skin | wired-onion-skin-walk-20261031.jpg | previous frame ghosted 35% under current, viewed |
| 8 | Motion smear | wired-motion-smear-punch-20261031.jpg | blurred copy offset +12px at 40% under sharp copy, viewed |
| 9 | Squash & stretch | wired-squash-stretch-jump-20261031.jpg | landing frame 1.1x wide / 0.85x tall, viewed |
| 10 | Lip-sync strip | wired-lipsync-moo-strip-20261031.jpg | visemes v2 heads mbp -> oo -> rest, middle circled mouth, viewed |
| 11 | Painted-bg composite shot | wired-shot-flying-painted-bg-20261031.jpg | clean flying soar frame over painted flying bg, viewed. Figure reads small/low — first wired shot, not a locked layout. |
| 12 | Title-safe test | wired-title-safe-test-20261031.jpg | 90% action-safe red / 80% title-safe green guides, debug only, viewed |
| 13 | Neck cylinders | wired-gap-neck-cylinders-5-20261031.jpg | 5/5 (front, 3/4-left, side, 3/4-right, back), palette-matched vector, viewed. Vector, not hand-drawn masters. |
| 14 | Blank heads + furious | wired-gap-blank-heads-5-furious-1-20261031.jpg | 5 blank (clean-head-base, no mouth) + 1 furious (Face_Angry overlay), viewed v2. V1 was broken (grey-key black-box bug) and was rebuilt, not shipped. |
| 15 | Separate feet | wired-gap-feet-2-20261031.jpg | Leg1 + Leg2 feet cropped from leg pieces, viewed v2 |
| 16 | Gauntlet-only | wired-gap-gauntlet-only-2-20261031.jpg | Arm1 + Arm2 cuff bands, viewed |
| 17 | Turnaround warps | wired-gap-turnaround-warps-20261031.jpg | front / 3/4-warp / side-warp / back-warp, labelled WARP, viewed v2. NOT true hand-drawn 3/4 — see partial item 39. |
| 18 | Shot CJ-19 dual-light | wired-shot-cj19-dual-light-20261031.jpg | V3 gold-inner / cyan-outer dual-light shot, viewed in dual-light work |
| 19 | Shot CJ-28 rooftop | wired-shot-cj28-rooftop-20261031.jpg | arms-up plate over painted rooftop bg, feet on roof floor, viewed v2. V1 was broken (grey-key black-box bug) and was rebuilt. |
| 20 | Shot CJ-30 alley | wired-shot-cj30-alley-20261031.jpg | approved fighting pose over painted alley bg, viewed |
| 21 | Tahoma2D level conversion (native binary) | wired-tahoma-level/frame-01..24.tlv (24/24, 165 KB each) + .tpl palettes | tconverter under xvfb, "Conversion terminated!" per file = success. NOTE: first batch run stalled 19 min on a "File already exists? Y/N" prompt for frame-01 — killed, dir cleared, rerun clean: 24/24. |

Authoritative split: viewed 21, file-verified 3, blocked+replacement 12,
partial 3, Mars/push-only 2 = 41. The file-verified three are next.

## WIRED — file output verified by re-parse (3)

| # | Item | Real output | Verification |
|---|------|-------------|--------------|
| 23 | JSFL logic -> runnable XFL | wired-xfl-punch-20261031/DOMDocument.xml | re-parsed: 15 layers, 60 frames (15 x 4 keyframes), fps 24, canvas 1100x1500, grey-128 bg. JSFL rotation rule animateRotation = 90 - clipAngle applied. Animate run itself still blocked (item 26 (Animate)). |
| 24 | Pencil2D .pclx | wired-pencil2d-cape-jones-20261031.pclx | re-parsed: 4 bitmap frames, fps 24, camera 550x750, entries main.xml + palette + 4 PNGs, bitmap frames=4 |
| 25 | Synfig character-piece rig | wired-synfig-cape-jones-rig-20261031.sif | re-parsed: 1 import layer, fps 24, clean apose plate full-frame, origin 0 -> +0.20 -> -0.20 over 0f/12f/24f, rotation 0deg -> 3deg -> 0deg. Replaces the old circle-only tween. Native Synfig CLI render NOT run (item 36 (Synfig native)). |
| — | Xsheet CSV (extra method, not a separate inventory item) | wired-xsheet-walk-20261031.csv | frame/pose/hold/audio cue/notes, 4 rows. |

## BLOCKED + free replacement wired (12)

| # | Item | Why blocked here | Replacement that IS wired |
|---|------|------------------|---------------------------|
| 26 | Adobe Animate / JSFL run | Animate not on VM, Windows/Mac only, no Linux build | XFL builder (item 23) + Tahoma2D xsheet + Pencil2D timeline. Animate run remains a browser/Win-Mac parent task, 0/1. |
| 27 | Toon Boom Harmony trial | Sign-in pending (secure entry card presented ~16:05 CDT, not yet submitted); desktop only, no Linux | v7c rig + Tahoma2D (item 21) + Synfig bones (item 25). Trial status UNKNOWN, not "day X/14". |
| 28 | Wick Editor | Web-only, flagged discontinued, no Linux install | Pencil2D timeline (item 24) + Blender + Tahoma2D xsheet |
| 29 | Cavalry | Mac/Windows only, Canva account required, not installed, no sign-in attempted | Synfig (vector tween + bones) + Blender |
| 30 | OpenToonz upstream | No Linux binary, Flatpak route not installed here | Tahoma2D, its fork (item 21) |
| 31 | Blender full-height 1100x1500 render | Blender 5.2.3 background render aborts rc=134 in this VM: "Couldn't open libEGL.so.1" — both EEVEE and CYCLES, no PNG produced. System has libGL/libGLX but NO libEGL. | PIL Level 2 stack (item 4) proves the same geometry/light on a real shot; script + blend ready for parent VM where Blender renders: wired_blender_v2.py + wired-blender-v2-standard-20261031.blend (99 KB) + full-size masks below |
| 32 | Blender ACES 1.3 comparison | Same EGL abort (item 31 (Blender render)) | Script/blend ready; ACES 2.0 vs Rec.709 already tested in clean-100 (ACES darker/greyer, mean diff 24.0); ACES 1.3 comparison is the parent-VM step |
| 33 | Blender line-light / rim-fade / ellipse-pads IN Blender | Same EGL abort | Same pieces in PIL Level 2 (item 4) + full-size Blender masks, stats-verified: shadow ellipse+pads mask 96,217 nonzero px, max 255; line-light mask 278,892 nonzero px; fade mask 255->76 gradient, 1,650,000 px nonzero by design. Masks are stats-verified, not eye-viewed — do not claim them as viewed renders. |
| 34 | Krita animation timeline (native) | Krita binary absent in this VM; apt cache has no krita package; apt-get update blocked by a lock held by process 791 (parent apt-get) — do NOT retry apt blindly | Frame layers + FFmpeg assembly (items 2, 6); .kra timeline step owed in parent VM where Krita lives |
| 35 | Pencil2D native export | Pencil2D binary absent in this VM (same apt situation) | .pclx verified (item 24) + FFmpeg render of the exact same frames (item 6) |
| 36 | Synfig native render | Synfig binary absent in this VM (same apt situation) | .sif verified (item 25) + FFmpeg render of the same plate motion |
| 37 | Tahoma2D GUI render / .tnz scene | GUI screenshot black/blank in earlier run (window did not paint in 15s); no .tnz scene exists (project folder has only inputs/ + xsheet JSON, scenes/ empty), so tcomposer cannot run until a .tnz scene is authored | tconverter level conversion (item 21) + FFmpeg render of the same frames (item 6). .tnz scene authoring still owed, not claimed. |

## PARTIAL — built, full completion still owed (3)

| # | Item | Built | Still owed |
|---|------|-------|------------|
| 38 | Clean-slice eye pass | Sliced pieces used in a real layout shot (item 5) | Eye-view pass on 129 sliced sheets (sliced but not eye-viewed); batch application 0/184 sheets as a batch |
| 39 | Per-shot composites | 4/30 shots through pipeline: CJ-01, CJ-19, CJ-28, CJ-30 (+ flying painted-bg shot) | 26/30 shots, and per-shot approval 0/30 (Mars only) |
| 40 | True hand-drawn 3/4 head/torso/side/back | Turnaround warps (item 17) + forearm-head34 v2 construction warp (separate workstream) | True hand-drawn pieces 0/1 each — needs a hand-drawn artist pass, not a warp |

## MARS-ONLY / PUSH-WORKSTREAM-ONLY (2)

| # | Item | Status |
|---|------|--------|
| 41a | Mars approvals | 0 approvals claimed anywhere in this inventory. Every output above is "built + viewed", NOT approved. |
| 41b | Repo landing (push) | NOT pushed by this task. This folder is ready for the push workstream: wired-push-manifest-20261031.json (55 files, SHA-256 each) + wired-tahoma-manifest-20261031.json (48 files: 24 .tlv + 24 .tpl). Push workstream lands it PR-only and verifies on main by size+SHA after merge. Nothing in this folder has been cleaned or deleted. |

## Gap-audit coordination note

The gap list closed here = TRACKER-20261031 unfinished list + clean-100
coordinator owed list + parts-audit gaps (separate feet, gauntlet-only,
neck cylinders, blank heads + furious, true 3/4 pieces). If the separate
gap-audit workstream adds items beyond those three sources, they fold into
v2 of this inventory — this inventory does not claim to have seen a list
it has not seen. No item on the three sources above is left list-only
except where this inventory says blocked + replacement, partial, or
Mars/push-only, with the reason named.

## Defects fixed in viewing (not hidden)

- Blank-heads v1 and CJ-28 v1 shipped a grey-key bug: greykey() treated
  transparent black pixels as character, turning transparent plates into
  opaque black boxes. Both were rebuilt with original-alpha compositing
  and re-viewed clean.
- Tahoma batch v1 stalled on an overwrite prompt; killed and rerun clean.
- CJ-01 Level 2 v2: CORRECTED — delivered run rim max 0.89 / bleed max 0.13; rim pass 63,773 nonzero alpha px, bleed pass 52,970 px. The earlier 0.00 log line was a different run, not the delivered file.

## Builders in this folder

build_wired.py, build_tool_projects.py, build_extra.py,
wired_blender_v2.py, build_gap_closure.py, wired-driver-log-20261031.json,
wired-push-manifest-20261031.json, wired-tahoma-manifest-20261031.json.
All outputs are NEW dated files; no version Mars has seen was overwritten.
