#!/bin/bash
# Composite the two BROTHERMAN test videos.
# 1) brotheman-movement-test.mp4 — 96f/4s solo rig proof over a dark
#    background (elbow, knee/squat, wave, fingers, hair follow-through).
# 2) brotheman-test.mp4 — 120f/5s scene test: BROTHERMAN composited at
#    right over the V2 Cape Jones plate (v2/check-f0001.png, read-only,
#    unmodified), speech card f49-96 (t=2.0s..4.0s). SILENT, no voice.
set -e
cd /home/hatch/workspace/_cape-jones-parking-lot-2d/brotheman
PLATE=../v2/check-f0001.png

ffmpeg -y -v error \
  -f lavfi -i "color=c=0x14082a:s=1280x720:r=24:d=4" \
  -framerate 24 -i frames_move/f%04d.png \
  -filter_complex "[0:v][1:v]overlay=0:0:shortest=1" \
  -c:v libx264 -pix_fmt yuv420p -r 24 -t 4 brotheman-movement-test.mp4

ffmpeg -y -v error \
  -loop 1 -t 5 -i "$PLATE" \
  -framerate 24 -i frames/f%04d.png \
  -i speechcard.png \
  -filter_complex "[1:v]scale=430:486,format=rgba[bm];[0:v][bm]overlay=770:204:shortest=1[sc];[sc][2:v]overlay=0:0:enable='between(t,2.0,4.0)'" \
  -c:v libx264 -pix_fmt yuv420p -r 24 -t 5 brotheman-test.mp4

echo "--- ffprobe ---"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration,codec_name -of default=noprint_wrappers=1 brotheman-movement-test.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration,codec_name -of default=noprint_wrappers=1 brotheman-test.mp4
sha256sum brotheman-movement-test.mp4 brotheman-test.mp4
ls -la brotheman-movement-test.mp4 brotheman-test.mp4
