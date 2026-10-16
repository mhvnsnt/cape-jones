#!/usr/bin/env bash
# cartoon-fx.sh — FFmpeg + frei0r cartoon effect chains.
# Uses the pulled frei0r plugin set (~/workspace/tools/frei0r, GPL-2.0).
# Install the plugins once (cmake build) and point ffmpeg at them:
#   export FREI0R_PATH=~/workspace/tools/frei0r/build/src/filter
#
# Usage:
#   cartoon-fx.sh <recipe> <in> <out>        # single recipe
#   cartoon-fx.sh boil+ink+grain <in> <out>  # chained recipes
#   cartoon-fx.sh --list
#
# Recipes:
#   boil      squigglevision — the "Dr. Katz" boiling-line wobble
#   ink       sobel edge detect blended back over the frame (inking)
#   toon      frei0r cartoon + posterize (flat comic look)
#   halftone  colorhalftone print dots
#   grain     filmgrain (16mm-style)
#   weave     gateweave (projector gate wobble)
#   scan      scanline0r CRT scanlines
#   vig       vignette
#   sharp     sharpness pass for line art
set -euo pipefail

list_recipes() {
  grep -E '^\s+[a-z]+\)' "$0" | sed 's/) \\//' | awk '{print $1}' | sort -u
}

if [[ "${1:-}" == "--list" ]]; then list_recipes; exit 0; fi
[[ $# -ge 3 ]] || { echo "usage: cartoon-fx.sh <recipe[+recipe...]> <in> <out>"; exit 1; }

RECIPES="$1"; IN="$2"; OUT="$3"
VF=""

add_vf() { VF="${VF:+$VF,}$1"; }

IFS='+' read -ra R <<< "$RECIPES"
for r in "${R[@]}"; do
  case "$r" in
    boil)     add_vf "frei0r=squigglevision:0.5" ;;
    ink)      add_vf "split[a][b];[a]frei0r=sobel:0.9,negate[c];[b][c]blend=all_mode=multiply" ;;
    toon)     add_vf "frei0r=cartoon:0.7,frei0r=posterize:4" ;;
    halftone) add_vf "frei0r=colorhalftone:4" ;;
    grain)    add_vf "frei0r=filmgrain:0.18" ;;
    weave)    add_vf "frei0r=gateweave:0.3" ;;
    scan)     add_vf "frei0r=scanline0r:0.25" ;;
    vig)      add_vf "frei0r=vignette:0.55" ;;
    sharp)    add_vf "frei0r=sharpness:0.6" ;;
    *) echo "unknown recipe: $r (see --list)"; exit 1 ;;
  esac
done

ffmpeg -hide_banner -y -i "$IN" -vf "$VF" -c:a copy "$OUT"
