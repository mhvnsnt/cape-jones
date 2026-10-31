# Free stacks + industry standards wired in — Cape Jones, 2026-10-31
Rule from Mars: fill gaps with 100% free stacks first, then anything top-level industry standard,
and if something above that is more recommended, reverse-engineer that too and say why it is up there.

## Free stack (100% free, no paid tool needed) — wired
- OpenToonz / Tahoma2D — free, production cutout + tweening, the free equivalent of Toon Boom Harmony
- Synfig Studio — free bone rigs + tweening, the free equivalent of Moho/Animate rigging
- Rigby2D — free 2D rigging, Spine-compatible JSON (cape-jones-rig-spine.json is already in that shape)
- Blender 5.2.3 LTS Grease Pencil — free, industry-used for 2D in 3D space, compositing, grading
- Krita — free clean-up / ink-and-paint, colour management
- RIFE — free frame interpolation for on-2s to smooth playback
- FFmpeg — free delivery encoding, -14 LUFS loudness check
- JSFL / Adobe Animate template — template is wired, but Animate itself is PAID, so it is NOT the free stack;
  the free equivalent above (OpenToonz/Synfig/Rigby) is the default for production, Animate is optional
- LUTs — .cube files are free and portable across Blender, OpenToonz, FFmpeg, DaVinci Resolve (free version)

## Top-level industry standard — why it is up there
- Toon Boom Harmony — TV production standard for rigged cutout shows (CN, Disney TVA, etc.)
  Why up: bone/deform rigs, node compositing, production pipeline, not just drawing.
  Free equivalent wired: OpenToonz/Tahoma2D + Synfig.
- TVPaint — hand-drawn TV standard.
  Why up: bitmap drawing + timing, used for feature/TV hand-drawn.
  Free equivalent wired: Krita + OpenToonz.
- Adobe Animate / After Effects — web/TV pipeline standard for symbol rigs + compositing.
  Why up: symbol library, JSFL automation, compositing.
  Free equivalent wired: JSFL template + OpenToonz/Synfig + Blender compositing.
- Spine — game/TV rig standard.
  Why up: bone hierarchy, slots, animations as JSON — exactly what cape-jones-rig-spine.json already uses.
  Free equivalent wired: Rigby2D + Spine JSON format (no paid Spine licence needed to read/write that JSON).
- DaVinci Resolve (free version) — grading + delivery standard.
  Why up: LUTs, loudness, delivery presets.
  Free equivalent wired: .cube LUTs + FFmpeg -14 LUFS.

## Above that — what is more recommended, and why
- A single pipeline, not a single tool: script -> boards -> animatic -> model sheet -> rig -> scene -> final,
  with manifest + SHA + QC at every stage. That is the TRIPPEDD pattern already wired in, and it is
  above any one tool because a tool alone does not guarantee a show — the pipeline does.
- Open, portable formats over locked formats: PNG cutouts + JSON timelines + .cube LUTs + FFmpeg delivery.
  Why above: they survive a tool going paid, breaking, or disappearing. A .fla alone does not.
- Rig locked to a version (v6) + checkpoint files + PR verification.
  Why above: without a lock, new art drifts and old shots break. That is why v6 is the default lock, not v5/v8.

## What this does NOT change
- No other show's characters, names, logos, dialogue, or cries are pulled in. Only systems, tools, and formats.
- New art packs (3/4, side, back rig pieces, viseme slices, cape states) still need to be made and shown before locking.
  The staged sheets below are reference sheets, not rig pieces, until they are sliced and joint-locked.
