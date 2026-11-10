#!/bin/bash
# batch_process.sh — Run the full Cape Jones pipeline on every video in a directory.
# Vertical scaling: process 100 FlipaClip exports in one command.
#
# Usage:
#   batch_process.sh <input_dir> <output_dir> [grade] [led_preset]
#
# Example:
#   batch_process.sh ~/flipaclip-exports/ ~/finished-segments/ cj-royal purple-pulse
#
# Each input video goes through:
#   1. flipaclip_post.sh (denoise → cleanup → interpolate → deghost → upscale → sharpen)
#   2. finish.py (QC → color grade → LED preset → audio mix → final encode)
#
# Failed files are logged to <output_dir>/batch-failures.log, successes to batch-success.log.
# The script continues past failures — check the logs at the end.

set -u

INPUT_DIR="${1:?Usage: batch_process.sh <input_dir> <output_dir> [grade] [led_preset]}"
OUTPUT_DIR="${2:?Usage: batch_process.sh <input_dir> <output_dir> [grade] [led_preset]}"
GRADE="${3:-cj-day}"
LED="${4:-}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
POST_SH="$SCRIPT_DIR/flipaclip_post.sh"
FINISH_PY="$SCRIPT_DIR/finish.py"

mkdir -p "$OUTPUT_DIR"
SUCCESS_LOG="$OUTPUT_DIR/batch-success.log"
FAIL_LOG="$OUTPUT_DIR/batch-failures.log"
: > "$SUCCESS_LOG"
: > "$FAIL_LOG"

count=0
ok=0
fail=0

for input in "$INPUT_DIR"/*.mp4 "$INPUT_DIR"/*.mov "$INPUT_DIR"/*.avi; do
    [ -e "$input" ] || continue
    count=$((count + 1))
    base="$(basename "$input")"
    name="${base%.*}"
    tmp_out="$OUTPUT_DIR/${name}.post.mp4"
    final_out="$OUTPUT_DIR/${name}.final.mp4"

    echo "[$count] Processing: $base"

    # Stage 1: post pipeline
    if ! bash "$POST_SH" "$input" "$tmp_out" >>"$OUTPUT_DIR/batch.log" 2>&1; then
        echo "$base : flipaclip_post.sh failed" >> "$FAIL_LOG"
        fail=$((fail + 1))
        continue
    fi

    # Stage 2: finish (grade + LED + QC)
    finish_args=( "$tmp_out" "$final_out" --grade "$GRADE" )
    [ -n "$LED" ] && finish_args+=( --led "$LED" )
    if ! python3 "$FINISH_PY" "${finish_args[@]}" >>"$OUTPUT_DIR/batch.log" 2>&1; then
        echo "$base : finish.py failed" >> "$FAIL_LOG"
        fail=$((fail + 1))
        continue
    fi

    rm -f "$tmp_out"
    echo "$base -> ${name}.final.mp4" >> "$SUCCESS_LOG"
    ok=$((ok + 1))
done

echo "=== BATCH DONE: $ok ok, $fail failed, $count total ==="
echo "Success: $SUCCESS_LOG"
echo "Failures: $FAIL_LOG"
