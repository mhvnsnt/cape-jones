# Audacity — cape-jones wiring

Pulled 2026-10-23 (overnight idle pipeline) via `~/workspace/tools/pull-to-repo.sh`.
Upstream: `audacity/audacity` @ `f515da46486301d48db89f195729ef0c87980668`
(master, pushed 2026-10-22, 18,813 stars, not archived).

**License (own-eyes on LICENSE.txt in this tree): GPLv3.** The header states:
"Audacity is released under the GNU General Public License version 3 (GPLv3).
Individual source files may be available under other licenses... many source
files are available under GPL version 2 (GPLv2) or (at your option) any later
version, and this is the default license used where no other license is
specified. Documentation is distributed under a Creative Commons-Attribution
license. (CC-BY 3.0)". Free + commercial use OK (same bar as the
Glaxnimate/Flowblade/Natron GPL pulls).

**Why it's here — the DAW slot.** The audio chain in `production/tools/audio/`
had: source separation (demucs, audio-separator), TTS (kitten/piper/parler/
higgs/cosyvoice/qwen3), voice conversion (RVC), restoration (deepfilternet,
voicefixer), SFX (mmaudio), music (ACE-Step), speech-to-speech (step-audio2) —
but NO interactive multitrack audio editor. Every AI-generated asset (dialogue
line, converted voice, generated score, synthesized SFX) still has to be CUT,
ARRANGED, MIXED and MASTERED by hand somewhere. Audacity is that somewhere:
the world's standard free DAW, multitrack editor + recorder, VST/AU/LV2
effects host. This is the END of the audio chain — everything the AI lanes make
lands here for editing/mixing/mastering before it goes to the video edit
(Flowblade project / `melt` farm render).

## What's in this tree

- `src/` — Audacity 4 app code (built on the MuseScore framework).
- `au3/` — the classic Audacity 3 codebase (kept in-tree upstream).
- `muse/`, `muse_deps/` — submodule checkouts (EMPTY in this depth-1 pull).
  A real build needs `git clone --recursive` (or init these two + build the
  au3 deps per BUILDING.md). Documented, not fetched: no submodules in
  vendored pulls, per house convention.
- `au3/modules/scripting/` + `au3/scripts/piped-work/` — mod-script-pipe
  scripting support (drive Audacity from Python via named pipes).
- `thirdparty/`, `help/`, `locale/` — deps, manual sources, translations.
- Trimmed from upstream: `.github/` CI only (house convention).
- Verified: 0 binaries > 50MB, 0 model weights, 0 prebuilt `.so`/`.dll`.

## Build (from upstream BUILDING.md — not run on this VM)

CMake build (`cmake -S . -B build`, presets in `CMakePresets.json`).
Needs the muse/muse_deps submodules initialized first. Linux/macOS/Windows
all supported upstream. GUI app — for interactive lanes; no GPU needed.

## Automation story (how this fits the pipeline)

1. **Interactive (primary):** run the built Audacity for dialogue-take
   editing, arrangement, mixing, mastering — the human/authoring step the AI
   chain cannot replace.
2. **Macros:** Audacity's built-in Macro chains = batch processing recipes
   (normalize → de-click → EQ → compress → loudness-normalize → export).
   Save the show's mastering chain as a Macro; every episode's final mix runs
   the identical chain = consistent loudness across episodes.
3. **mod-script-pipe:** `au3/modules/scripting` lets Python drive Audacity
   through named pipes — scripted batch edits (trim silence, apply chains,
   batch-export stems) from a lane without opening the GUI.
4. **Round-trip with the farm:** export stems/masters as WAV → they become
   the audio tracks in Flowblade/MLT (`production/tools/flowblade/`,
   `production/tools/mlt/`) for the final episode assembly + `melt` render.

## Show-pipeline uses

- Dialogue editing: cut/comp the best takes from TTS/RVC/voice lanes before
  lip-sync (rhubarb-lip-sync needs clean, final-timed audio).
- Voice-design passes: stack pitch/formant/VST effects on converted voices.
- SFX layering: place mmaudio's generated SFX against the dialogue/music beds.
- Mastering: per-episode loudness chain (Macro) so EP01..EPnn sound like one show.
- Sample prep: cut loops/stingers for the game (Western Heart) menus/entrances.

## Chain position

```
voicefixer → demucs/audio-separator → RVC → [dialogue/music/SFX AI lanes]
        → AUDACITY (edit/arrange/mix/master) → Flowblade/melt (picture lock)
```

## Notes

- GUI runs headful (Xvfb on the VM like the Blender lane, or a dev box).
  Batch Macro runs can be scripted via mod-script-pipe from a lane.
- Prefer the repo's AppImage/binary installs for interactive use; this vendored
  source is for reference, patching, and building custom effect/plugin lanes.
