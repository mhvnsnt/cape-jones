#!/bin/bash
# check_before_ship.sh — run this BEFORE any Cape Jones clip/video is shown or sent.
# Exit 1 blocks delivery. There is no --force. If it fails, fix the pose, do not bypass.
set -u
GATE="$(dirname "$0")/pre_delivery_gate.py"
if [ $# -lt 2 ]; then echo "usage: check_before_ship.sh <pose-table.json> <clip-id> [video.mp4]"; exit 2; fi
if [ $# -ge 3 ]; then python3 "$GATE" --pose-table "$1" --clip-id "$2" --video "$3"
else python3 "$GATE" --pose-table "$1" --clip-id "$2"; fi
