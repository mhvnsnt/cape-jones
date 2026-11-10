# Free-first wiring — Mars, 2026-10-31 14:47 CDT

Standing order, in Mars's sense: wire everything up in the freest way possible.
Anything that is not free, reverse-engineer the METHOD and rebuild it free —
methods, systems, timing, passes, node order — never a proprietary character,
logo, asset, or copied code. That is the same line as the standing forbidden
list: characters/names/logos/cries/literal dialogue/town names straight from
another game are out; structure, order, windows, inputs, values, data shapes,
mechanics, and tools are in.

## Free stack actually wired here (not a shopping list)

- Blender 5.2.3 LTS — production compositor, verified `blender --version`.
  Node builder: blender-compositor-stack.py. Blender 4.5.3 on disk is NOT
  the production standard and is not used for production passes.
- FFmpeg — `lut3d` for every .cube in this project (30 base + 24 spectrum +
  16 spectrum v2), delivery encode, -14 LUFS audio target.
- PIL / Python — apply_compositor.py (layer stack, same order as the Blender
  tree), slice_clean.py (clean cuts, component-based, no hand rectangles),
  joint_locked_rig_v7c.py (ball-centre pivots, round-masked caps, no square crops).
- OpenColorIO — bundled with Blender 5.2.3; ACES input/output transform is
  still NOT wired in PIL (stated in WIRED-COMPOSITOR-STATUS.md) — that gap
  is owed, not claimed.
- Free compositing equivalents reverse-engineered from public behaviour:
  Nuke-style pass/AOV compositing -> separate pass PNGs + Plus/Multiply
  merges in PIL and in the Blender tree (see apply_lighting_levels.py);
  DaVinci Resolve grading order -> colour management, primary, secondary,
  look LUT, output transform, in that order in LIGHTING-LEVELS-0-5.md;
  Toon Boom / OpenToonz-style cleanup -> stray-pixel, hole, and line-weight
  metrics in cleanup v2 (owed as a full pass, not claimed done here).

## What "reverse engineer" does NOT mean here

- No downloaded commercial game, ROM, or full proprietary asset in any repo.
- No proprietary character or logo generated or pasted into a shot.
- No paid tool is claimed as installed, and no paid run happens without
  Mars's approval for that specific run (standing GPU rule).

## Counts for this wiring batch

- Pass-based lighting script: apply_lighting_levels.py, levels 0–5, colored +
  non-colored, passes written out separately (shadow, rim, bleed, volume,
  emission, finishing) so each can be tuned without re-rendering.
- LUT totals after this batch: base approved 30/30, spectrum approved 6/24,
  spectrum v2 expanded 16/16 files, approved 0/16. Total .cube files 70.
  Approved total: 36/70 = 51%.

## Industry standards pull, 2026-10-31 (append, not a rewrite)
- 12 principles checklist: 12-PRINCIPLES-CHECKLIST-20261031.md (12/12, per-shot application 0/30).
- Pipeline template: PIPELINE-TEMPLATE-20261031.md (10/10 stages, end-to-end shots 0/30).
- Full pull + repo tools (24 entries, wired 6/24): INDUSTRY-STANDARDS-PULL-20261031.md.

## Free animation stack — installed + wired 2026-10-31 (free-stack batch)
Installed home: ~/workspace/tools-industry/ (never /usr system dirs as durable
storage; apt packages below are system installs, their versions are recorded,
and the portable builds live in tools-industry).

CORRECTION TO A COMMON MISREADING: Gumball's actual production software was
Adobe Flash/Animate (paid) + After Effects + Cinema 4D/Maya — NOT free, and
Animate is in maintenance/discontinuation, not current and not free. The free
stack below is the industry-standard free REPLACEMENT set, not a claim that
Gumball used these tools. The TikTok "free animation software" memory does not
change that: no free tool used on Gumball was found; the free replacements are
what is wired here.

### Installed, version-verified (5/5 of the install list)
- Tahoma2D 1.6.3 (OpenToonz fork, preferred) — portable tarball
  Tahoma2D-linux-clang-1.6.3.tar.gz, extracted to
  tools-industry/tahoma2d-1.6.3/ (AppImage + tahomastuff, 436 MB).
  Verified: `./AppRun -version` -> "Tahoma2D v1.6.3" under Xvfb.
  Note: the AppImage was extracted (squashfs-root/) because this VM has no
  FUSE; the .AppImage file itself is kept as the source artifact.
- Krita 5.2.2 — apt (Ubuntu noble, 1:5.2.2+dfsg-2build8). Verified under Xvfb
  with an explicit screen; QT_QPA_PLATFORM=offscreen is IGNORED by Krita
  (it forces xcb), so Xvfb is required for any Krita run here.
- Pencil2D 0.6.6 — apt (0.6.6-3build2). Verified: `pencil2d --version`.
- Synfig 1.5.1 (renderer) + Synfig Studio 1.5.1 (GUI) — apt
  (synfig 1.5.1+dfsg-3build7, synfigstudio 1.5.1-1build2). Verified:
  `synfig --version` -> synfig 1.5.1.
- Already on disk, re-verified: Blender 5.2.3 LTS, FFmpeg 8.1.2, PIL.

### Tests passed 4/4 tools with a real Cape Jones test (all outputs viewed)
- Tahoma2D/Toonz test: 24-frame beat-grid level, 24 fps, beat markers
  1/7/13/19, plate sliding 0/+10/0/-10 px per 6-frame beat cell.
  Files: showcase/free-stack-tests/frames-24/ (24 PNGs),
  cape-jones-24f-beat-grid-20261031.mp4,
  cape-jones-24f-beat-grid-contact-20261031.jpg (VIEWED, 6x4 contact sheet),
  tahoma-cape-jones-24f/ (inputs/ + xsheet-beat-grid-20261031.json).
  HONEST LIMIT: the level folder + xsheet spec are import-ready and the
  binary is verified, but a Tahoma GUI scene open + render was NOT run here
  — that step is owed, not claimed.
- Krita test: (a) plate import/export — krita-plate-export-20261031.png is
  PIXEL-IDENTICAL to rig-apose-v7c-clean-transparent.png (same 1100x1500,
  alpha identical, RGB mean abs diff 0.0 on opaque pixels), VIEWED.
  (b) frame test via kritarunner — krita-frame-test.py creates a document
  with frame1 = plate and frame2 = plate shifted +10 px, saves
  krita-frame-test-20261031.kra (718 KB), re-exported to
  krita-frame-test-export-20261031.png, VIEWED. First export attempt failed
  on syntax (--export needs --export-filename separately); second attempt
  with the correct syntax passed.
- Pencil2D test: GUI-drawn stroke saved as pencil2d-cape-jones-test-20261031.pclx
  (main.xml, bitmap layer, camera layer, fps 12), headless-exported to
  pencil2d-export-20261031.mp4, frame 1 VIEWED (diagonal stroke).
  Then a real Cape Jones frame was added: plate scaled to 400x545 as
  data/004.001.png, frame 2, in pencil2d-cape-jones-plate-centred-20261031.pclx.
  GOTCHA FOUND AND FIXED: Pencil2D topLeftX/topLeftY are relative to canvas
  CENTRE, not top-left — (200,27) put the plate half off the bottom-right
  corner; (-200,-272) centres it. Centred frame 2 VIEWED (full character).
- Synfig test: synfig-cape-jones-tween-20261031.sif, a red circle tweening
  left->right over 24 frames @24 fps. Rendered frames 0/12/24 with the synfig
  CLI: circle centre x 74.5 -> 274.5 -> 474.5, same 8,064 red pixels each
  frame (no distortion). Frame 12 VIEWED. Note: the PNG background renders
  transparent (black in the viewer), not grey-128 — the grey plate is a
  separate layer in real use, not part of the .sif.

### Not installed here, and why (2/2 checked, 0 installed)
- Wick Editor: free + open source, but WEB-BASED (runs in the browser) and
  flagged discontinued in directory listings. No Linux install exists to
  wire here; it is not claimed as installed. A Wick project would have to be
  authored in a browser, which a subagent cannot do.
- Cavalry: free for individuals since April 2026 (Canva-owned, Canva account
  required), but Mac/Windows ONLY — no Linux build. Not installed here, and
  no account sign-in was attempted. Its procedural-rig / data-driven motion
  role is covered here by Synfig (vector tween + bones) and Blender
  (drivers / geometry nodes) instead.
- OpenToonz (upstream): NOT installed separately. Upstream ships no Linux
  binary; the community route is Flatpak io.github.OpenToonz 1.8.0, and
  flatpak is not installed on this VM. Not attempted, because Tahoma2D
  (its fork, preferred in the task) is installed and verified — that is the
  free way around, per the standing free-way-around rule, not a roadblock
  report.

### Reverse-engineered non-free equivalents (method only, no paid software
installed, no paid tool claimed as installed)
- Adobe Animate symbol / timeline / XFL -> our XFL parser (proven on Gumball
  FLAs: ZIP local-header walk, scene + puppet extraction) + JSFL builders
  (build-fla-timeline.jsfl, build-cape-jones-rig-v7.jsfl — written, NOT yet
  run, Animate is not on this VM) + Tahoma2D timeline/xsheet (this batch)
  + Pencil2D timeline (this batch). Symbol = a named piece + its frames;
  timeline = xsheet columns + beat grid; XFL = the ZIP/XML scene format we
  already parse, not a file we claim to open in Animate here.
- Toon Boom rig (bone / deform / plastic tool) -> our v7c rig
  (joint_locked_rig_v7c.py: ball-centre pivots, round-masked caps, pose-
  driven piece swaps) + Tahoma2D/OpenToonz plastic tool for mesh deformation
  + Synfig bones for vector deformation. Rig mechanics, not rig files.
- After Effects compositing (node / layer effects, glows, god rays) ->
  Blender 5.2.3 compositor stack (blender-compositor-stack.py, 18 nodes /
  22 links as a file) + PIL compositor stack (apply_compositor.py, same
  layer order) + FFmpeg delivery. God-ray production = Blender volumetric
  passes, not flat PIL wedges (PIL god rays are draft proof only).
- Maya 3D (modelling / rigging / rendering) -> Blender 5.2.3 LTS
  (modelling, armature rigging, Cycles/Eevee rendering, OCIO colour
  management). No Maya file, scene, or binary is used or claimed.
- What reverse-engineering does NOT cover: no proprietary character, name,
  dialogue, logo, or copied code is used; no paid licence is bypassed; no
  commercial game/ROM is involved. Methods, systems, timing, passes, and
  node order only.

### Counts for this batch
- Tools installed: 5/5 install list (Tahoma2D, Krita, Pencil2D, Synfig,
  Synfig Studio) + Blender/FFmpeg/PIL already present.
- Tool tests passed: 4/4 (Tahoma2D level/xsheet, Krita, Pencil2D, Synfig).
- Tools checked but not installed here: 3 (Wick Editor web-only, Cavalry
  Mac/Windows-only, OpenToonz upstream via Flatpak not attempted — Tahoma2D
  covers it).
- Owed, not claimed: Tahoma GUI scene open + render; Krita animation
  timeline (frames as a .kra animation, not just layers); Synfig Studio GUI
  pass (CLI render only so far).
