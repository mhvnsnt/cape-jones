#!/usr/bin/env bash
# ffmpeg-animation-filters.sh — FFmpeg filter recipes for 2D cartoon/animation production
# All filters are built into the local FFmpeg. No downloads needed.
# Usage: ./ffmpeg-animation-filters.sh <recipe> <input> <output> [extra args]
# Run with no args to list recipes.

set -euo pipefail

list_recipes() {
cat << 'EOF'
ANIMATION FILTER RECIPES (all built-in):

  smooth60      12fps -> smooth 60fps motion interpolation (no scene ghosting)
  celshade      Posterize to flat cel-shaded color bands
  deband        Kill gradient banding in compressed skies/backgrounds
  denoise-fast  Quick denoise for line art before upscale
  denoise-best  Slow but line-preserving denoise
  sharpen       Line-art sharpening (unsharp)
  sharpen-cas   Contrast-adaptive sharpening (CAS)
  deflicker     Fix flicker in scanned/stop-motion frames
  deshake       Stabilize shaky camera passes
  grade-pop     Punchy cel grade (contrast + saturation)
  grade-warm    Warm cartoon grade via curves
  vignette      Retro vignette framing
  grain         Film grain for retro look
  motontrail   Motion trails / ghosting (onion-skin-in-post)
  zoompan       Ken Burns camera move on a still (10s, 1080p, 24fps)
  gif           High-quality GIF export (palettegen/paletteuse)
  dither-retro  Ordered dithering for 8-bit retro look
  drawtext-tc   Burn in timecode for editorial review
  cartoon       frei0r cartoon effect (check params)
  edgeglow      frei0r edge glow

EXAMPLES:
  ./ffmpeg-animation-filters.sh smooth60 in.mp4 out.mp4
  ./ffmpeg-animation-filters.sh celshade in.mp4 out.mp4
  ./ffmpeg-animation-filters.sh zoompan still.png out.mp4
EOF
}

recipe_filter() {
  case "$1" in
    smooth60)      echo "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:scd=none" ;;
    celshade)      echo "elbg=levels=8" ;;
    deband)        echo "deband=range=16:thr1=24:thr2=24:thr3=24" ;;
    denoise-fast)  echo "hqdn3d=1.5:1.5:6:6" ;;
    denoise-best)  echo "nlmeans=s=3:p=7:r=15" ;;
    sharpen)       echo "unsharp=5:5:1.0:5:5:0.0" ;;
    sharpen-cas)   echo "cas=0.8" ;;
    deflicker)     echo "deflicker" ;;
    deshake)       echo "deshake" ;;
    grade-pop)     echo "eq=contrast=1.1:saturation=1.4:brightness=0.02" ;;
    grade-warm)    echo "curves=r='0/0 0.5/0.6 1/1':g='0/0 0.5/0.55 1/1':b='0/0 0.5/0.5 1/1'" ;;
    vignette)      echo "vignette=PI/4" ;;
    grain)         echo "noise=alls=8:allf=t" ;;
    motiontrail)   echo "tblend=all_mode=average" ;;
    dither-retro)  echo "dither=bayer:bayer_scale=3,format=rgb24" ;;
    cartoon)       echo "frei0r=cartoon:0.3|0.9" ;;
    edgeglow)      echo "frei0r=edgeglow:0.5" ;;
    *) echo "UNKNOWN RECIPE: $1" >&2; list_recipes; exit 1 ;;
  esac
}

if [ $# -lt 1 ]; then list_recipes; exit 0; fi

RECIPE="$1"; IN="${2:-}"; OUT="${3:-}"
if [ -z "$IN" ] || [ -z "$OUT" ]; then echo "Usage: $0 <recipe> <input> <output>" >&2; exit 1; fi

case "$RECIPE" in
  zoompan)
    ffmpeg -y -loop 1 -i "$IN" -vf "zoompan=z='min(zoom+0.0015,1.5)':d=250:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=24" -t 10 -c:v libx264 -pix_fmt yuv420p "$OUT"
    ;;
  gif)
    PALETTE=$(mktemp /tmp/palette-XXXXXX.png)
    ffmpeg -y -i "$IN" -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" "$PALETTE"
    ffmpeg -y -i "$IN" -i "$PALETTE" -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse" "$OUT"
    rm -f "$PALETTE"
    ;;
  drawtext-tc)
    FONT="${4:-/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf}"
    ffmpeg -y -i "$IN" -vf "drawtext=fontfile=$FONT:text='%{pts\:hms}':fontsize=36:fontcolor=white:x=10:y=10" -c:a copy "$OUT"
    ;;
  *)
    VF=$(recipe_filter "$RECIPE")
    ffmpeg -y -i "$IN" -vf "$VF" -c:a copy "$OUT"
    ;;
esac
echo "DONE: $OUT"
