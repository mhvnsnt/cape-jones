# MuseScore Studio — Cape Jones Wiring

**What:** MuseScore Studio — free and open source music notation / score-engraving
software (the canonical WYSIWYG sheet-music editor: write, play, print scores).
**Slot:** **MUSIC NOTATION** — notation-first composition and engraving.
**Upstream:** https://github.com/MuseScore/MuseScore · pinned @ 7f96e9f623f09c489f38acc57b1b6bcd9aad7c04
(HEAD 2026-10-23, 15,287 stars, not archived)
**License:** **GNU GPL v3** (own-eyes verified on LICENSE.txt in this tree — the full
"GNU GENERAL PUBLIC LICENSE" text follows the MuseScore header; bundled fonts under
the GNU Freefont License with an embedding exception so documents you create are not
infected by the font license). Free + commercial ✅ (same bar as
Audacity/Glaxnimate/Flowblade/ComfyUI).
**Location in repo:** `production/tools/audio/musescore/` (519MB, 10,160 files, code-only;
0 binaries >50MB; `share/sound/*.sf3` built-in soundfonts kept — app assets under the bar).
**Submodules intentionally empty:** `muse/` and `muse_deps/` (upstream `muse_framework` +
`muse_deps` submodules) were NOT initialized in this vendored tree (build-time
`git submodule update --init --recursive` fetches them upstream) — same handling as the
Audacity pull's `muse/`/`muse_deps/`.
**Trimmed:** upstream `.github/workflows/` only (house convention); issue templates and
other metadata kept.

## Why this slot is real (not a duplicate of the Audacity pull)

Audacity 4's notation UI is built *from* MuseScore code (see the `MuseScore-CLA-applies`
headers and `muse-migration` tools inside `production/tools/audio/audacity/`) — but what
Audacity vendors is a notation *component*. This pull is the **standalone notation studio**:
the engraving engine, score layout, parts extraction, and the full notation editor. LMMS
covers beat/arrange-first composition; ACE-Step covers AI music generation; MuseScore
covers notation-first composition + professional engraving. Three distinct slots, no overlap.

## Chain position (audio pipeline)

```
[compose]  LMMS (beat/arrange-first) ───stems/mix───┐
[generate] ACE-Step (music AI) ─────────stems───────┤
[notate]   MuseScore (notation-first) ──midi/pdf───┤
[dialogue] tts → rvc → lipsync ────────────────────┤
[sfx]      mmaudio (video→foley) ──────────────────┤
                                                    ▼
                                         Audacity (edit/mix/master)
                                                    ▼
                                         Flowblade/melt (picture lock)
```

MuseScore renders scores to MIDI/audio or exports parts as PDF — the notation feeding the
same downstream mix as the LMMS/ACE-Step assets.

## Setup

```bash
# Developer environment + Qt (upstream wiki — same pages Audacity 4 references):
#   https://github.com/musescore/MuseScore/wiki/Set-up-developer-environment
#   https://github.com/musescore/MuseScore/wiki/Install-Qt-and-Qt-Creator
# MuseScore 4 builds on Qt 6.

git submodule update --init --recursive   # muse_framework + muse_deps (build-time only)
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && cmake --build . -j$(nproc)
```

## Usage (headless batch — the automation story)

MuseScore exports scores headlessly — the notation equivalent of `melt`/`lmms --render`:

```bash
# Export a score to PDF (no GUI):
musescore --export-to score.pdf score.mscz

# Export parts / other formats (midi, mp3, wav, ogg, flac, svg, png, musicxml):
musescore --export-to score.mid score.mscz
musescore --export-to score.wav score.mscz

# Batch-convert a folder of scores:
for f in *.mscz; do musescore --export-to "${f%.mscz}.pdf" "$f"; done
```

Show-pipeline uses:
- **Score composition:** write character themes, orchestral stings, entrance music as
  `.mscz` scores; export stems (MIDI → LMMS for arranging, WAV → Audacity for mastering).
- **Sheet-music deliverables:** engraved parts/PDFs for any live-player sessions.
- **MusicXML interchange:** round-trip scores between MuseScore, LMMS (via MIDI), and
  the AI music tools.

GPU note: not needed — MuseScore is a CPU desktop app. Build once per platform; the
headless export runs anywhere (VM, Kaggle CPU, render box).
