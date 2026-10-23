#!/bin/bash
# FlipaClip Post-Production Pipeline
# Takes a hand-drawn FlipaClip video and makes it broadcast-ready.
#
# Stages:
#   1. Denoise + deflicker (ffmpeg)
#   2. Line cleanup (OpenCV - smooths noise, crisps thin lines, preserves fills)
#   3. Frame interpolation 12fps -> 24fps (RIFE AI, at source res)
#      --fast flag: use ffmpeg minterpolate instead (quicker, lower quality)
#   4. Upscale 2x (Lanczos - fast; ESPCN available for low-res sources)
#   5. Sharpen + color punch (ffmpeg)
#
# NOTE: Interpolation runs BEFORE upscale to avoid OOM on 4K frames.
#
# Usage: flipaclip_post.sh input.mp4 output.mp4 [--upscale] [--fast]
#   --upscale: also run ESPCN neural upscale (slower, use for <720p sources)
#   --fast: use ffmpeg minterpolate instead of RIFE (quicker, lower quality)
set -e
IN="$1"
OUT="$2"
UPSCALE=""
FAST=""
for arg in "$@"; do
    [ "$arg" == "--upscale" ] && UPSCALE="--upscale"
    [ "$arg" == "--fast" ] && FAST="--fast"
done

if [ -z "$IN" ] || [ -z "$OUT" ]; then
    echo "Usage: $0 input.mp4 output.mp4 [--upscale]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK=$(mktemp -d)
trap "rm -rf $WORK" EXIT

echo "=== Stage 1: Denoise + deflicker ==="
ffmpeg -y -v error -i "$IN" \
    -vf "hqdn3d=1.5:1.5:6:6,deflicker=size=5:mode=am" \
    -c:v libx264 -preset fast -crf 18 \
    "$WORK/01_denoised.mp4"

echo "=== Stage 2: Line cleanup (per frame) ==="
mkdir -p "$WORK/frames_in" "$WORK/frames_out"
ffmpeg -y -v error -i "$WORK/01_denoised.mp4" "$WORK/frames_in/f%04d.png"
for f in "$WORK"/frames_in/*.png; do
    base=$(basename "$f")
    python3 "$SCRIPT_DIR/cleanup_lines.py" "$f" "$WORK/frames_out/$base"
done
ffmpeg -y -v error -framerate 12 -i "$WORK/frames_out/f%04d.png" \
    -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
    "$WORK/02_cleaned.mp4"

echo "=== Stage 3: Interpolate 12fps -> 24fps (at source res) ==="
if [ "$FAST" == "--fast" ]; then
    echo "  (ffmpeg minterpolate - fast mode)"
    ffmpeg -y -v error -i "$WORK/02_cleaned.mp4" \
        -vf "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir" \
        -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
        "$WORK/03_interp.mp4"
else
    echo "  (RIFE AI - high quality)"
    mkdir -p "$WORK/rife_out"
    ~/workspace/tools/rife-venv/bin/python ~/workspace/tools/rife425/rife_interp.py \
        "$WORK/frames_out" "$WORK/rife_out" --exp 1
    echo "  (de-ghosting RIFE output for cartoon flat colors)"
    ~/workspace/tools/rife-venv/bin/python ~/workspace/tools/post-pipeline/deghost.py \
        "$WORK/rife_out" --pattern "f*.png" --inplace --threshold 30
    ffmpeg -y -v error -framerate 24 -i "$WORK/rife_out/f%04d.png" \
        -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
        "$WORK/03_interp.mp4"
fi

echo "=== Stage 4: Upscale 2x ==="
if [ "$UPSCALE" == "--upscale" ]; then
    echo "  (neural ESPCN - slower)"
    mkdir -p "$WORK/up_in" "$WORK/up_out"
    ffmpeg -y -v error -i "$WORK/03_interp.mp4" "$WORK/up_in/f%04d.png"
    for f in "$WORK"/up_in/*.png; do
        base=$(basename "$f")
        python3 -c "
import cv2, sys
img = cv2.imread('$f')
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel('$SCRIPT_DIR/models/ESPCN_x4.pb')
sr.setModel('espcn', 4)
up = sr.upsample(img)
# Downscale 4x->2x with Lanczos for clean 2x
h, w = up.shape[:2]
up2 = cv2.resize(up, (w//2, h//2), interpolation=cv2.INTER_LANCZOS4)
cv2.imwrite('$WORK/up_out/$base', up2)
"
    done
    ffmpeg -y -v error -framerate 24 -i "$WORK/up_out/f%04d.png" \
        -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
        "$WORK/04_upscaled.mp4"
else
    ffmpeg -y -v error -i "$WORK/03_interp.mp4" \
        -vf "scale=iw*2:ih*2:flags=lanczos" \
        -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p \
        "$WORK/04_upscaled.mp4"
fi

echo "=== Stage 5: Sharpen + color ==="
ffmpeg -y -v error -i "$WORK/04_upscaled.mp4" \
    -vf "unsharp=5:5:0.8:5:5:0.0,eq=saturation=1.1:contrast=1.03" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
    "$OUT"

echo "=== Done: $OUT ==="
ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate,duration \
    -of default=noprint_wrappers=1 "$OUT"
