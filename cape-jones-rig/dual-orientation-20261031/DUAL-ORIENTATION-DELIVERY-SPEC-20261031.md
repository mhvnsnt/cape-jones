# Dual-orientation delivery spec — YouTube + TikTok — 20261031

**Show:** Cape Jones, 2D. **Job:** one edit, both orientations at once — landscape for
YouTube long-form, portrait for YouTube Shorts + TikTok. **Mars approval: 0/1 — not claimed approved.**
**No repo push in this task. Background plate is the room stand-in (batch-KKGuh),
NOT the canonical room — Mars said the canonical room is a different room he has
pictures of. Do not call this background canonical.**

## 1. What Mars asked for, in plain words
A thing that makes videos in portrait AND landscape at the same time — YouTube and
TikTok ratio frames at the same time. That thing exists, in three forms, and this
spec wires all three so Cape can use whichever fits the shot:
1. **Open-gate / protected-master (industry, camera + broadcast)** — shoot/frame a
   taller master than either delivery, with aspect markers for both ratios on screen
   while framing. Canon EOS R6 Mark III / EOS C50 / Sony FX5 open-gate (full-sensor
   3:2) display two aspect markers at once so one take frames for horizontal AND
   vertical. This is the camera version of what we built in 2D.
2. **Auto-reframe (industry, editors)** — Adobe Premiere Pro Auto Reframe, DaVinci
   Resolve Studio Smart Reframe, Final Cut Pro Smart Conform: subject-tracking
   pan/position keyframes that convert one ratio to another. Premiere's own docs:
   it identifies the main subject and adjusts framing over time, no manual keyframing.
   Free-stack equivalent in this task: subject-bbox-tracked crop (see §5, method C
   warning — a tracked crop from a 16:9 master still cuts a wide subject).
3. **Dual-canvas / multi-format timeline (experimental + app)** — one timeline,
   multiple canvases exported together (CapCut / Premiere multi-sequence / social
   repurposing tools such as Opus Clip / Vizard / Kapwing Smart Crop do the
   auto-crop version; the honest experimental version is our own dual-canvas
   builder in this folder: one master, N exports, one command). No single app was
   found that genuinely renders portrait and landscape *simultaneously from one
   live canvas* as a native feature — every real tool renders one master and
   exports N crops. This spec says that plainly instead of inventing an app.

## 2. Platform specs — researched 2026-10-31, public sources
Labelled: OFFICIAL = platform's own help page as reported by a source;
MEASURED/CONSERVATIVE = third-party measurement or a union of sources.
Platforms do NOT publish exact organic safe-zone pixels — every pixel safe zone
below is therefore labelled MEASURED or UNION, never "official".

### YouTube long-form (landscape)
- Ratio 16:9. Recommended 1920×1080 (1080p), up to 3840×2160 (4K) and higher.
- Container MP4, H.264 High Profile progressive, AAC-LC 48 kHz, Fast Start.
- Frame rate: same as recorded (24/25/30/48/50/60). Do not convert 30→60.
- Bitrate SDR 1080p: 8 Mbps at 24–30 fps, 12 Mbps at 48–60 fps. 4K: 35–45 Mbps
  at 24–30 fps, 53–68 Mbps at 48–60 fps. YouTube re-encodes everything — the
  upload is the best the viewer will ever see, so export at or above these.
- Upload cap: 256 GB or 12 hours, whichever first.
- Safe areas (broadcast convention, applied here): action-safe 5% all round
  (96 px horizontal / 54 px vertical on 1920×1080), title-safe 10% all round
  (192 / 108 px). Keep titles inside title-safe, action inside action-safe.

### YouTube Shorts (portrait)
- Ratio 9:16 (square 1:1 also qualifies as a Short). 16:9 is treated as long-form,
  NOT a Short, even under 3 minutes.
- Length: up to 3 minutes (since 2024-10-15). Recommended 1080×1920; app upload
  tops out at 1080p. Same H.264/AAC encoding as long-form (8 Mbps at 1080p30).
- UI: channel name, title, subscribe, sound label along the bottom; like/dislike/
  comment/share/remix down the right edge. YouTube publishes NO organic pixel
  safe zone. Google Ads Shorts template (official ads spec): top 288, bottom 672,
  left 48, right 192 on 1080×1920.
- MEASURED organic (Slice, 2026-10-02): safe box 745×1265 — top 217, bottom 438,
  left 97, right 238. That measurement already includes ~9% side crop on tall phones.

### TikTok (portrait)
- Ratio 9:16 native. Recommended 1080×1920, MP4 H.264 + AAC, 30 fps (60 for motion),
  ~8–15 Mbps at 1080p, 128–192 kbps audio. Accepts 1:1 and 16:9 but letterboxes them.
- Length: in-app up to 10 minutes, longer via upload (up to 60 minutes on some accounts).
  File: ~72 MB Android / ~288 MB iOS in-app, up to 4 GB web (sources vary — check
  before a big upload; the 1080×1920 frame is the stable part).
- UI: Following/For You tabs + search top, profile/like/comment/save/share stack
  right, username/caption/sound bottom. TikTok publishes NO organic pixel safe zone.
- Conservative working values across sources (1080×1920): top 108–150, bottom
  250–480, right 120–160, left 60. The widest bottom figure (480) is the caption +
  sound + buttons stack; use it for anything that must be read.

### 3. Cape Jones recommended delivery (this spec)
- **Master: 1920×1920 square open-gate master** (2D analogue of a 3:2 open-gate sensor).
  For 4K delivery, scale the whole pipeline ×2: master 3840×3840, landscape
  3840×2160, portrait 2160×3840.
- **Landscape export: 1920×1080** (centre crop y 420–1500 of the master).
- **Portrait export: 1080×1920** (centre crop x 420–1500 of the master).
- **Square export: 1080×1080** (centre crop, intersection) — bonus, qualifies as a
  Short and is accepted on TikTok.
- **Protected square: central 1080×1080 (master x 420–1500, y 420–1500).**
  RULE: subject, essential action, faces and must-read text stay inside this square.
  Anything inside it is whole in BOTH orientations, with no pan, no scale change,
  no re-render. Anything outside it is background only — it may be cut in one
  orientation and that is fine, because it is background.
- **Portrait safe zone — CAPE UNION (use this, it covers both platforms' organic UI):**
  on 1080×1920: left 97, right 238, top 288, bottom 438 → safe box
  x 97–842, y 288–1482 (745 × 1194 px). Faces + must-read text inside this box.
  Ads variant: bottom 672 → box y 288–1248. If a shot will ever run as an ad,
  use the ads box.
- **Landscape safe zone:** title-safe 10% (x 192–1728, y 108–972 on 1920×1080),
  action-safe 5% (x 96–1824, y 54–1026).
- **FPS:** 24 fps for the show (matches the inbetweening work); 30 fps is also
  native to both platforms — pick per shot, never convert mid-shot.
- **Encoding per export:** MP4, H.264 High Profile, AAC-LC 48 kHz, Fast Start,
  8 Mbps at 1080p24/30, 12 Mbps at 1080p48/60. TikTok: same file is accepted;
  keep the TikTok file under the in-app size cap by trimming length, not by
  dropping resolution.
- **Workflow (one edit, both orientations):**
  1. Compose on the 1920×1920 master with BOTH crop windows + the protected
     square + the portrait safe box visible (the diagram in this folder).
  2. Animate / light / effect on the master only. Never animate the crops separately.
  3. Run `dual_orientation.py` (or the same steps in an editor): it crops landscape,
     portrait and square, checks the subject bbox is whole in both, and fails
     loudly if a limb leaves the protected square.
  4. Export clean (no overlays) + safe-overlay proof frames. Upload the clean files.
  5. Preview on a phone before publishing — the only reliable final check, because
     UI layouts shift between app versions and devices.

## 4. Proof — arms-up shot, one master, both orientations (viewed)
Source: approved arms-up base (1100×1500 transparent) on the room stand-in background.
Figure fitted at height 1020 px inside the protected square, centred on the master.
Measured bboxes are in `dual-orientation-measurements-20261031.json` — the proof
script prints them, it does not guess them. Headline result: the figure is WHOLE
in landscape AND in portrait AND in square, because it lives inside the protected
square. Measured: figure in master (737, 613)–(1184, 1322), inside protected
(420, 420)–(1500, 1500); in landscape (737, 193)–(1184, 902), inside title-safe
(192, 108)–(1728, 972); in portrait (317, 613)–(764, 1322), inside the Cape
portrait safe box (97, 288)–(842, 1482). The safe-overlay frames show exactly
that (cyan box = figure bbox, green = safe box, red = UI dead zone / action-safe,
amber = ads bottom extension).

## 5. The three methods, compared honestly
- **A — Protected master (RECOMMENDED for Cape):** whole figure in both, no
  motion, no scale change, one animation. Cost: the frame must be composed for
  the square — wide two-character spreads do not fit; those need method B or a
  two-shot version.
- **B — Blurred pillarbox fill from landscape:** whole figure, no cut, but the
  subject is smaller in portrait (landscape 1920×1080 scaled to 1080 wide = 608 tall,
  centred, blurred landscape behind it). Good for wide shots, weaker for
  portrait-first viewing. Proof file in this folder.
- **C — Blind / tracked 9:16 crop from a 16:9 master (CAUTION, not a warning for
  THIS figure):** a 9:16 crop of a 1920×1080 frame is only 607 px wide. MEASURED
  CORRECTION: this arms-up figure is 447 px wide in landscape (x 737–1184) and
  sits 81–528 px inside the 607 px centre crop — 0 px cut, 160 px headroom. So a
  blind centre crop works for THIS narrow, centred figure. It FAILS when the
  subject is wider than 607 px in landscape, off-centre, or two characters wide —
  then arms/background action are cut. Auto-reframe tools pan this window to
  follow a subject, which helps a single walking subject and does NOT help a
  wide arms-up / spread pose. Proof file renamed accordingly.

## 6. Industry tools wired / mapped
- Premiere Pro Auto Reframe — subject-tracking reframe, keyframes editable.
  Mapped to our subject-bbox tracker; NOT run here (trial blocked on Adobe sign-in).
- DaVinci Resolve Studio Smart Reframe — same class, Studio (paid) feature;
  free Resolve does not include it. Mapped, not run.
- Final Cut Pro Smart Conform — same class, Mac only. Mapped, not run.
- Open-gate cameras (Canon R6 Mark III / C50, Sony FX5) — two aspect markers at
  once; the 2D analogue is our master diagram with both crop windows visible.
- Free-stack wiring in this folder (RUN, not just mapped): `dual_orientation.py`
  + FFmpeg H.264 exports (see §7). That is the tool Cape actually uses today.

## 7. Video exports (FFmpeg, H.264, from the proof stills)
Still-to-video proofs are made from the clean exports (2 s, 24 fps, 8 Mbps target)
so the encoding chain itself is proven, not just the stills. Command pattern:
`ffmpeg -loop 1 -i <clean.png> -t 2 -r 24 -c:v libx264 -b:v 8M -pix_fmt yuv420p -movflags +faststart <out.mp4>`
Files are listed in the measurements / folder listing at delivery time.

## 8. Honest limits
- No app was found that natively renders portrait + landscape simultaneously from
  one live canvas — all real tools are master + N exports. Anyone claiming a
  single live dual canvas should be asked to show the export panel.
- The protected-square rule costs composition freedom: a shot that NEEDS width
  (two characters far apart, a wide room) cannot be protected — use method B or
  shoot it as two framings.
- Safe-zone pixels are unions of third-party measurements + the one official ads
  template, NOT platform-published organic values. Phone preview before publishing
  is still mandatory.
- Background in this proof is a stand-in room, NOT the canonical room.
- Mars approval of this spec: 0/1.
