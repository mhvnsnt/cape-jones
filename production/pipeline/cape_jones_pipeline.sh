#!/bin/bash
# CAPE JONES MASTER PIPELINE
# ==========================
# One command: FlipaClip drawings → finished, graded, scored animation.
#
# Full studio pipeline in a box:
#   1. Denoise + deflicker
#   2. Line cleanup (OpenCV)
#   3. Frame interpolation (RIFE local / ToonCrafter GPU / ffmpeg fast)
#   4. De-ghosting (post-interpolation artifact removal)
#   5. Upscale (Lanczos / ESPCN / RealESRGAN-anime)
#   6. Sharpen + color punch
#   7. Color grade (24 grades) + LED presets (8 animated)
#   8. Effects (energy blast, stroke reveal overlays)
#   9. Audio mix (music + SFX)
#  10. Final encode (web/broadcast presets)
#
# Usage:
#   cape_jones_pipeline.sh input.mp4 output.mp4 [options]
#
# Options:
#   --interp METHOD     rife (default), tooncrafter, fast
#                       tooncrafter = GPU notebook (see kaggle-tooncrafter/)
#   --grade GRADE       Color grade (see --list-grades)
#   --led PRESET        Animated LED preset (see --list-led)
#   --led-speed X       LED animation speed multiplier
#   --audio FILE        Background music/audio to mix
#   --audio-volume X    Audio volume (default 1.0)
#   --blast TYPE        Add energy blast: beam, rings, freeze, burst
#   --blast-x X --blast-y Y --blast-angle DEG
#   --upscale           ESPCN neural upscale (for <720p sources)
#   --upscale-anime     RealESRGAN anime 4x upscale (slower, better for animation)
#   --fast             Use ffmpeg minterpolate (quick preview, lower quality)
#   --preset PRESET     Encoding: web (default), broadcast, master
#   --list-grades      List all color grades
#   --list-led         List all LED presets
#   --keep-temp        Don't delete temp files (for debugging)
#
# Examples:
#   # Basic: cleanup + RIFE + grade + music
#   cape_jones_pipeline.sh flipaclip.mp4 finished.mp4 \
#       --grade cj-royal --audio music.mp3
#
#   # Full: LED party lights + energy blast + trippy grade
#   cape_jones_pipeline.sh flipaclip.mp4 finished.mp4 \
#       --grade cj-trippy --led party-strobe \
#       --blast beam --blast-x 540 --blast-y 960 \
#       --audio nebulas.mp3 --preset broadcast
#
#   # Quick preview (fast interpolation, no upscale)
#   cape_jones_pipeline.sh flipaclip.mp4 preview.mp4 --fast --grade cj-day

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Defaults
INTERP="rife"
GRADE="cj-day"
LED=""
LED_SPEED="1.0"
AUDIO=""
AUDIO_VOL="1.0"
BLAST=""
BLAST_X=""
BLAST_Y=""
BLAST_ANGLE="0"
UPSCALE=""
UPSCALE_ANIME=""
FAST=""
PRESET="web"
KEEP_TEMP=""

# Parse args
IN=""
OUT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --interp) INTERP="$2"; shift 2;;
        --grade) GRADE="$2"; shift 2;;
        --led) LED="$2"; shift 2;;
        --led-speed) LED_SPEED="$2"; shift 2;;
        --audio) AUDIO="$2"; shift 2;;
        --audio-volume) AUDIO_VOL="$2"; shift 2;;
        --blast) BLAST="$2"; shift 2;;
        --blast-x) BLAST_X="$2"; shift 2;;
        --blast-y) BLAST_Y="$2"; shift 2;;
        --blast-angle) BLAST_ANGLE="$2"; shift 2;;
        --upscale) UPSCALE="1"; shift;;
        --upscale-anime) UPSCALE_ANIME="1"; shift;;
        --fast) FAST="1"; INTERP="fast"; shift;;
        --preset) PRESET="$2"; shift 2;;
        --keep-temp) KEEP_TEMP="1"; shift;;
        --list-grades)
            python3 "$SCRIPT_DIR/finish.py" --list-grades; exit 0;;
        --list-led)
            python3 -c "from led_controller import PRESETS; [print(f'  {k}: {v[\"desc\"]}') for k,v in PRESETS.items()]"; exit 0;;
        -*)
            echo "Unknown option: $1"; exit 1;;
        *)
            if [ -z "$IN" ]; then IN="$1";
            elif [ -z "$OUT" ]; then OUT="$1";
            else echo "Too many positional args"; exit 1; fi
            shift;;
    esac
done

if [ -z "$IN" ] || [ -z "$OUT" ]; then
    echo "Usage: $0 input.mp4 output.mp4 [options]"
    echo "Run with --list-grades or --list-led to see options"
    exit 1
fi

if [ ! -f "$IN" ]; then
    echo "Input not found: $IN"
    exit 1
fi

WORK=$(mktemp -d -p ~/workspace/tmp)
if [ -z "$KEEP_TEMP" ]; then
    trap "rm -rf $WORK" EXIT
else
    echo "Temp dir (keeping): $WORK"
fi

echo "=========================================="
echo "  CAPE JONES PIPELINE"
echo "  Input:  $IN"
echo "  Output: $OUT"
echo "  Interp: $INTERP | Grade: $GRADE | Preset: $PRESET"
[ -n "$LED" ] && echo "  LED: $LED (speed $LED_SPEED)"
[ -n "$BLAST" ] && echo "  Blast: $BLAST"
[ -n "$AUDIO" ] && echo "  Audio: $AUDIO (vol $AUDIO_VOL)"
echo "=========================================="

# ── Stage 1-6: Base pipeline (flipaclip_post.sh) ──
echo ""
echo "### Stages 1-6: Cleanup + Interpolation + Upscale ###"
POST_ARGS=()
[ -n "$UPSCALE" ] && POST_ARGS+=(--upscale)
[ -n "$FAST" ] && POST_ARGS+=(--fast)

if [ "$INTERP" == "tooncrafter" ]; then
    echo "ToonCrafter mode: run base pipeline WITHOUT interpolation,"
    echo "then use the Kaggle GPU notebook for ToonCrafter interpolation."
    echo "See: ~/workspace/cape-jones-build/kaggle-tooncrafter/README.md"
    echo ""
    echo "Running stages 1-2 + 4-6 (skipping local interpolation)..."
    # For now, fall back to RIFE with a warning
    echo "WARNING: ToonCrafter GPU run is manual. Using RIFE for now."
    INTERP="rife"
fi

"$SCRIPT_DIR/flipaclip_post.sh" "$IN" "$WORK/06_base.mp4" "${POST_ARGS[@]}"

# ── Stage 7a: Energy blast overlay ──
CURRENT="$WORK/06_base.mp4"
if [ -n "$BLAST" ]; then
    echo ""
    echo "### Stage 7a: Energy Blast ($BLAST) ###"
    BLAST_ARGS=(--type "$BLAST" --base "$CURRENT" --output "$WORK/07_blast.mp4"
                --angle "$BLAST_ANGLE")
    [ -n "$BLAST_X" ] && BLAST_ARGS+=(--x "$BLAST_X")
    [ -n "$BLAST_Y" ] && BLAST_ARGS+=(--y "$BLAST_Y")
    # Match blast duration to video duration
    DUR=$(ffprobe -v error -show_entries format=duration \
          -of default=noprint_wrappers=1:nokey=1 "$CURRENT")
    BLAST_ARGS+=(--duration "$DUR")
    python3 "$SCRIPT_DIR/energy_blast.py" "${BLAST_ARGS[@]}"
    CURRENT="$WORK/07_blast.mp4"
fi

# ── Stage 7b: LED preset (animated color) ──
if [ -n "$LED" ]; then
    echo ""
    echo "### Stage 7b: LED Preset ($LED) ###"
    python3 "$SCRIPT_DIR/led_controller.py" \
        --input "$CURRENT" --output "$WORK/08_led.mp4" \
        --preset "$LED" --speed "$LED_SPEED"
    CURRENT="$WORK/08_led.mp4"
fi

# ── Stage 8-10: Finish (grade + audio + encode) ──
echo ""
echo "### Stages 8-10: Grade + Audio + Final Encode ###"

# Map preset to encoding params
case $PRESET in
    web)
        EXTRA_ARGS=(--crf 23);;
    broadcast)
        EXTRA_ARGS=(--crf 18);;
    master)
        EXTRA_ARGS=(--crf 12);;
    *)
        echo "Unknown preset: $PRESET (using web)"
        EXTRA_ARGS=(--crf 23);;
esac

FINISH_ARGS=("$CURRENT" "$OUT" --grade "$GRADE" "${EXTRA_ARGS[@]}")
[ -n "$AUDIO" ] && FINISH_ARGS+=(--audio "$AUDIO" --audio-volume "$AUDIO_VOL")

python3 "$SCRIPT_DIR/finish.py" "${FINISH_ARGS[@]}"

echo ""
echo "=========================================="
echo "  DONE: $OUT"
echo "=========================================="
ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate,duration \
    -of default=noprint_wrappers=1 "$OUT"
