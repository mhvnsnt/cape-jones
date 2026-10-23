# TRACK D PULL — Video Editing + Motion Graphics + Pre-production
Date: 2026-10-16 (document-only re-issue; disk at 86% — NO new downloads, NO clones).
License rule: commercial use OK; GPL fine for desktop tools.
Everything marked "on disk" was pulled by the first Track D attempt; nothing added in this pass.

---

## 1. VIDEO EDITING

### NLEs

| Tool | URL | Local path | License | Size | Status / what / why |
|---|---|---|---|---|---|
| **Kdenlive** — PRIMARY NLE RECOMMENDATION | https://kdenlive.org — AppImage: https://download.kde.org/stable/kdenlive/26.08/linux/kdenlive-26.08.2-x86_64.AppImage — Flatpak: `org.kde.kdenlive` | documented only | GPL-2.0+ | ~250MB AppImage | NOT on disk. Best fit for an animation pipeline: the only open NLE with **OpenTimelineIO import/export** (round-trips timelines with our OTIO lane), built-in proxy workflow for heavy PNG-sequence timelines, keyframable effects, titler, audio mixer. Active dev (26.08.x); a dopesheet-alpha build with per-parameter keyframes is in testing. Install path: AppImage, no sudo. |
| **Olive 0.1 / 0.2** | https://github.com/olive-editor/olive — https://www.olivevideoeditor.org/download | `tools/video-editing/olive-src` (ON DISK) | GPL-3.0 | 50MB source | Source pulled `--depth 1` (first attempt). Node-based compositor + NLE in one; 0.2 lists OpenTimelineIO as optional dependency. 0.1.0 is alpha but usable; 0.2 is nightly. Watch-list: could eventually rival Kdenlive on node compositing for motion work, but don't build the pipeline on it yet. |
| **Shotcut** | https://shotcut.org | documented only (see note) | GPL-3.0 | ~100-150MB AppImage | Solid fallback NLE: GPU effects, keyframes, rich filters, good timeline. Already noted in stack; no OTIO support. |
| **Flowblade** | https://github.com/jliljebl/flowblade | `tools/video-editing/flowblade-src` (ON DISK) | GPL-3.0 | 64MB source | Source pulled `--depth 1`. Python/GTK editor that runs straight from source — lightweight, no compile. Good low-spec alternative; film-style insert/overwrite editing. |
| **Pitivi** | https://gitlab.gnome.org/GNOME/pitivi | `tools/video-editing/pitivi-src` (ON DISK) | LGPL-2.1 | 35MB source | Source pulled `--depth 1`. GStreamer-based, simple and clean, but least suited to heavy animation timelines — fine for quick assembly, not primary. |
| **LosslessCut** | https://github.com/mifi/lossless-cut — AppImage: https://github.com/mifi/lossless-cut/releases/latest/download/LosslessCut-linux-x86_64.AppImage | documented only | GPL-2.0 | ~100MB AppImage | NOT on disk. Swiss-army lossless cutter: instant trims/splits/joins/extract-audio without re-encode. Perfect for slicing renders and dailies before NLE assembly. |
| **Avidemux** | http://avidemux.sourceforge.net | documented only | GPL-2.0 | ~30MB | NOT on disk. Simple cutter/filter/join; mostly superseded by LosslessCut for our purposes — documented for completeness. |

None of Olive/Shotcut/Flowblade/Pitivi was in `tools/` before this track; Shotcut and LosslessCut and Avidemux remain document-only per disk rules.

### FFmpeg frontends / batch processors (all documented only, all free)

- **Shutter Encoder** — https://www.shutterencoder.com — best-in-class FFmpeg batch GUI (re-encode, merge, burn subtitles, image-sequence handling). Free.
- **HandBrake** — https://handbrake.fr — GPL-2.0, GUI + CLI transcoder; `HandBrakeCLI` is the batch workhorse.
- **FFqueue** — http://ffqueue.bruchhaus.dk — Qt FFmpeg queue GUI, free.
- **WinFF** — http://www.winff.org — GPL-3.0, simple FFmpeg preset GUI.
- **MKVToolNix** — https://mkvtoolnix.download — GPL-2.0, `mkvmerge`: lossless join/split/remux.

### Proxy workflow
- **`tools/post-pipeline/proxy_gen.py`** (on disk, from first attempt): batch half-res proxies (`--height 540`, mpeg4/mjpeg/h264) + `proxy_manifest.csv` for relink; `--clean` to remove. Kdenlive also has built-in proxies (Settings → Configure Kdenlive → Proxy clips) — use that interactively, this script for batch/off-machine.

### NLE recommendation for the animation pipeline
**Kdenlive as primary.** (1) Only open NLE with OpenTimelineIO I/O — our OTIO lane hands timelines back and forth; (2) mature built-in proxy workflow for heavy PNG-sequence timelines; (3) keyframable effects + titler for assembly; (4) active development with an animation-relevant dopesheet alpha in testing. **LosslessCut** alongside for instant lossless trims of renders/dailies. **Olive 0.2** on the watch-list (node compositor + OTIO optional dep). For interactive editing on the VM: install the Kdenlive AppImage from the download.kde.org link above.

---

## 2. MOTION GRAPHICS

| Tool | URL | Local path | License | Size | Status / what / why |
|---|---|---|---|---|---|
| **Manim** (3Blue1Brown engine) | https://github.com/ManimCommunity/manim — `pip install manim` | documented only | MIT | ~300-500MB with system cairo+pango deps | NOT installed (deps heavy, disk at 86%). Animated diagrams/titles/math explainers — great for explainer inserts and animated title cards. Install path: `pip install manim` on a machine with headroom. |
| **Motion Canvas** | https://github.com/motion-canvas/motion-canvas | `tools/motion-graphics/motion-canvas` (ON DISK) | MIT | 8.7MB source | Pulled `--depth 1` (first attempt). TypeScript programmatic 2D animation with editor + timeline + audio sync — the fully-open Remotion alternative. Top pick for code-driven motion graphics in our pipeline. |
| **HyperFrames** | https://github.com/heygen-com/hyperframes | `tools/motion-graphics/hyperframes` (ON DISK) | Apache-2.0 | 411MB | Pulled (first attempt — includes heavy assets; do NOT re-clone). HTML/CSS → deterministic video renderer, agent-workflow oriented. |
| **MoviePy** | https://github.com/Zulko/moviepy — `pip install moviepy` | documented only | MIT | pip-sized | Python compositing (clips, text, effects) — the quick scriptable compositor. |
| **Remotion** | https://github.com/remotion-dev/remotion | documented only | **Source-available, NOT OSI-open** (Remotion License: free for individuals / ≤3-person companies; paid company license above) | — | Documented for awareness only — prefer Motion Canvas for fully-open work. |
| **ReelForge** | https://github.com/fahmid-juboraj/reelforge | documented only | (check repo; open) | — | Open GPU motion-graphics skill (kinetic type, visualizers, logo reveals), moderngl-based. |
| **gl-transitions** | https://github.com/gl-transitions/gl-transitions | documented only | MIT | — | 200+ WebGL transition shaders (wipe/burn/glitch/morph) for programmatic cuts. |
| **lottie-web** | https://github.com/airbnb/lottie-web | `tools/motion-graphics/lottie-web` (ON DISK) | MIT | 80MB source | Pulled (first attempt). Web Lottie renderer (Bodymovin lineage); pair with headless capture → ffmpeg for video, or use LottieConverter below. |
| **LottieConverter** | https://github.com/sot-tech/LottieConverter | `tools/motion-graphics/lottie-converter` (ON DISK) | BSD-3-Clause | 2.6MB source | Pulled `--depth 1`. rlottie-based CLI: Lottie JSON → PNG/GIF frames; pipe to ffmpeg for MP4. Tiny, genuinely useful. |
| **rlottie** (Samsung) | https://github.com/Samsung/rlottie | documented only | MIT | — | C++ Lottie player lib; ships a `lottie2gif` demo. |
| **puppeteer-lottie** | (via LottieFiles/awesome-lottie) | documented only | MIT | — | Renders Lottie → image/GIF/MP4 via headless Chrome — alternative to the C++ route. |
| **awesome-lottie** | https://github.com/LottieFiles/awesome-lottie | documented only | — | — | Curated index of all Lottie tools/libs. |

### Built glue (on disk, `tools/post-pipeline/`, from first attempt)
- **`kinetic_type.py`** — kinetic typography: `typewriter` (char-by-char + cursor), `word` (TikTok-caption style word pops, `--wps`), `cascade` (staggered hero titles). PIL frames → ffmpeg; mp4 on bg color or `--transparent` ProRes 4444 mov with alpha.
- **`lower_thirds.py`** — animated lower third (slide-in ease-out, hold, slide-out; `bar`/`box` styles, `--accent`) → ProRes 4444 `.mov` WITH ALPHA for NLE overlay + `_preview.mp4` for review.
- **`storyboard_sheet.py`** — printable worksheet PNG/PDF: header (title/project/page/date) + N 16:9 panels with thirds guides and SCENE/SHOT, ACTION, DIALOGUE, DUR fields.
- **`fountain_to_animatic.py`** — `.fountain` → per-scene title-card animatic mp4 (est. durations, optional audio laydown). Pairs with `script-tools/fountain_to_cues.py` and `post-pipeline/build_animatic.py`.

### Template libraries (documented only)
- **reveal.js** — https://github.com/hakimel/reveal.js → `tools/motion-graphics/reveal-js` (ON DISK, MIT, 19MB): HTML slide decks, exportable to PDF — doubles as pitch-deck tool and animated title-card system.

---

## 3. PRE-PRODUCTION

### Fountain / screenwriting

| Tool | URL | Local path | License | Size | Status / what / why |
|---|---|---|---|---|---|
| **screenplain** | https://github.com/vilcans/screenplain — `pip install screenplain` | `tools/pre-production/screenplain` (ON DISK) | MIT | 3.1MB source | Pulled `--depth 1`. Fountain → PDF/HTML/FDX CLI + Python library — the formatter backbone for script outputs. |
| **afterwriting** | https://github.com/ifrost/afterwriting-labs — web: https://afterwriting.com | documented only | MIT | — | Fountain → PDF + script analytics (character stats, locations, page balance). |
| **textplay** | https://github.com/olivertaylor/Textplay — `pip install textplay` | documented only | (check repo) | — | Python Fountain → PDF/HTML/FDX alternative to screenplain. |
| **Trelby** | https://github.com/trelby/trelby | `tools/pre-production/trelby-src` (ON DISK) | GPL-2.0 | 7.7MB source | Pulled `--depth 1`. Full desktop screenwriting app (Python/wx): Fountain import/export, FDX, PDF, reports, 200k name DB. Linux-native. |
| **Beat** | https://github.com/lmparppei/Beat | documented only | GPL | — | Excellent Fountain editor — **macOS/iOS only**, documented not pulled. |
| **Story Architect (STARC)** | successor of KIT Scenarist | documented only | open core | — | Full studio screenwriting suite, all platforms; Fountain import. |
| **ScriptCraft / OpenScene** | already in `tools/script-tools/README.md` | `tools/script-tools` (ON DISK) | — | — | Already documented by an earlier lane. |

### Beat boards / outlining
- **Manuskript** — https://github.com/olivierkes/manuskript → `tools/pre-production/manuskript` (ON DISK, GPL-3.0, 32MB): open-source writing studio with outliner + corkboard/index-card (beat-board) views + distraction-free editor. The beat-board answer. (Storyboarder already in stack has printed worksheets + Fountain import.)

### Storyboard templates
- **`storyboard_sheet.py`** (on disk, `tools/post-pipeline/`): printable worksheet PNG/PDF generator — see above.

### Pitch decks
- **reveal.js** — `tools/motion-graphics/reveal-js` (ON DISK, MIT, 19MB): HTML slide decks; export to PDF; good for pitch decks.
- **Marp** — https://github.com/marp-team/marp-cli — `npm i -g @marp-team/marp-cli` (MIT, documented only): Markdown → slide deck / PDF / PPTX.

### Concept art (beyond Krita, already in stack)
- **G'MIC** — https://gmic.eu (documented only): 500+ image filters, CLI + GIMP/Krita plugin — texture/stylization helpers for concept art. Free software (CeCILL license).

### Built: NEW `fountain_to_beats.py`
- **`tools/post-pipeline/fountain_to_beats.py`** (BUILT this pass, 119 lines, smoke-tested): stdlib-only Fountain parser → `<basename>_beats.json` + `<basename>_beats.md` beat sheets: per-scene sluglines, action/dialogue beats, speakers, word counts, est. durations (@`--wpm`, default 150). Fills the gap between raw script and `fountain_to_animatic.py` — the beats are the pre-production breakdown document (cast list, pacing, scene budget) feeding the animatic.

---

## DISK ACCOUNTING
- This pass: **zero downloads/clones** — one 4.9KB glue script added.
- Pre-existing on-disk from first Track D attempt (do not re-pull): flowblade-src 64MB, olive-src 50MB, pitivi-src 35MB, screenplain 3.1MB, trelby-src 7.7MB, motion-canvas 8.7MB, lottie-converter 2.6MB, lottie-web 80MB, manuskript 32MB, reveal-js 19MB, hyperframes 411MB. Total ≈ 711MB — largest single item is hyperframes (candidate for TeraBox/backup if disk pressure continues).
- Document-only this pass: Kdenlive AppImage (~250MB), LosslessCut AppImage (~100MB), Manim (~300-500MB with system deps), all other table entries above.
- Glue scripts total: <150KB.

## NLE RECOMMENDATION (animation pipeline)
**Kdenlive primary** (OpenTimelineIO I/O + proxies + keyframable effects + titler + dopesheet alpha), **LosslessCut** for instant lossless trims of renders/dailies, **Olive 0.2** as watch-list. Install Kdenlive via AppImage (https://download.kde.org/stable/kdenlive/26.08/linux/kdenlive-26.08.2-x86_64.AppImage) when needed — documented only, not pulled.
