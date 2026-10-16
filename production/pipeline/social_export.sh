#!/bin/bash
# social_export.sh — One-command social media delivery presets.
#
# Takes a finished 16:9 (or any) video and exports platform-ready versions:
#   tiktok / shorts / reels  → 9:16 vertical (1080x1920), smart center-crop
#   instagram-square          → 1:1 (1080x1080)
#   instagram-portrait        → 4:5 (1080x1350)
#
# Usage:
#   social_export.sh input.mp4 output_dir [preset ...]
#   social_export.sh input.mp4 out/           # all presets
#   social_export.sh input.mp4 out/ tiktok instagram-square
#
# Smart crop: keeps the vertical center by default. Pass --focus-top / --focus-bottom
# to bias the crop (useful when the character's head is high in frame).

set -e
if [ $# -lt 2 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
  echo "Usage: social_export.sh input.mp4 output_dir [preset ...] [--focus-top|--focus-bottom]"
  echo "  Presets: tiktok instagram-square instagram-portrait (default: all)"
  exit 0
fi
INPUT="$1"
OUTDIR="$2"
shift 2 || true

FOCUS="center"
PRESETS=()
for a in "$@"; do
  case "$a" in
    --focus-top) FOCUS="top" ;;
    --focus-bottom) FOCUS="bottom" ;;
    *) PRESETS+=("$a") ;;
  esac
done
[ ${#PRESETS[@]} -eq 0 ] && PRESETS=(tiktok instagram-square instagram-portrait)

mkdir -p "$OUTDIR"
BASE=$(basename "$INPUT" .mp4)

# y-offset expression per focus for the 9:16 crop
case "$FOCUS" in
  top)    Y916="(ih-oh)/4" ;;
  bottom) Y916="(ih-oh)*3/4" ;;
  *)      Y916="(ih-oh)/2" ;;
esac

for p in "${PRESETS[@]}"; do
  case "$p" in
    tiktok|shorts|reels)
      OUT="$OUTDIR/${BASE}_9x16_tiktok.mp4"
      ffmpeg -y -i "$INPUT" -vf \
        "crop=ih*9/16:ih:(iw-ow)/2:${Y916},scale=1080:1920:flags=lanczos" \
        -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
        -movflags +faststart -c:a aac -b:a 128k "$OUT"
      ;;
    instagram-square)
      OUT="$OUTDIR/${BASE}_1x1_ig.mp4"
      ffmpeg -y -i "$INPUT" -vf \
        "crop=min(iw\,ih):min(iw\,ih):(iw-ow)/2:(ih-oh)/2,scale=1080:1080:flags=lanczos" \
        -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
        -movflags +faststart -c:a aac -b:a 128k "$OUT"
      ;;
    instagram-portrait)
      OUT="$OUTDIR/${BASE}_4x5_ig.mp4"
      ffmpeg -y -i "$INPUT" -vf \
        "crop=ih*4/5:ih:(iw-ow)/2:(ih-oh)/2,scale=1080:1350:flags=lanczos" \
        -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
        -movflags +faststart -c:a aac -b:a 128k "$OUT"
      ;;
    *)
      echo "Unknown preset: $p (tiktok|shorts|reels|instagram-square|instagram-portrait)"
      exit 1
      ;;
  esac
  echo "wrote $OUT"
done
echo "done."
