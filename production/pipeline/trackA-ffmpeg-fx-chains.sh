#!/usr/bin/env bash
# Track A: FFmpeg effect chains wired to Track-A pulls.
# Sources pulled: frei0r (GPL-2.0), openfx-* (Natron OFX, GPL-2.0),
# Motion-Synthesizer (post-FX reference), claude-motion-skills (recipes).
# Prereqs: ffmpeg built with --enable-frei0r. Usage: bash trackA-ffmpeg-fx-chains.sh
set -euo pipefail
OUT="${1:-./trackA_out}"; mkdir -p "$OUT"
IN="${2:-}"   # input mp4; many chains below use $IN

echo "== chain list (edit vars at top, call functions) =="

# 1. GLOW / BLOOM (anime power-up aura): screen-blended blurred copy
fx_glow() { # $1 in $2 out $3 strength(0.3-1.0)
  ffmpeg -y -i "$1" -vf "split[a][b];[b]gblur=sigma=20[b];[a][b]blend=all_mode=screen:all_opacity=${3:-0.6}" -c:v libx264 -pix_fmt yuv420p "$2"
}

# 2. SPEEDLINES (action background): use a white speedlines PNG loop as overlay
fx_speedlines() { # $1 in $2 out $3 speedlines_png_loop $4 opacity
  ffmpeg -y -i "$1" -stream_loop -1 -i "$3" -filter_complex "[0:v]split[bg][a];[1:v]scale=iw:ih,colorchannelmixer=aa=${4:-0.35},format=rgba[sl];[bg][sl]overlay=0:0,format=yuv420p" -shortest -c:v libx264 -pix_fmt yuv420p "$2"
}

# 3. IMPACT FLASH (hit frames): 2-frame white flash at cut point
fx_impact() { # $1 in $2 out $3 timestamp(s) of hit
  ffmpeg -y -i "$1" -vf "eq=brightness=if(lt(abs(t-$3)\,0.08)\,0.9\,0):saturation=if(lt(abs(t-$3)\,0.08)\,0.2\,1)" -c:v libx264 -pix_fmt yuv420p "$2"
}

# 4. XFADE TRANSITIONS (show edit transitions): fade/wipe/dissolve between two clips
fx_xfade() { # $1 clipA $2 clipB $3 out $4 transition $5 duration $6 offset
  ffmpeg -y -i "$1" -i "$2" -filter_complex "xfade=transition=${4:-fade}:duration=${5:-0.5}:offset=${6:-2}" -c:v libx264 -pix_fmt yuv420p "$3"
}
# available transitions: fade,fadeblack,fadewhite,distance,pixelize,wipeleft,wiperight,wipeup,wipedown,slideleft,slideright,slideup,slidedown,smoothleft,smoothright,smoothup,smoothdown,circlecrop,rectcrop,circleopen,circleclose,vertopen,verthclose,horzopen,horzclose,dissolve,radial,fadegrays

# 5. FREI0R glow (needs ffmpeg --enable-frei0r; plugin from ~/workspace/tools/trackA-vfx/frei0r)
fx_frei0r_glow() { # $1 in $2 out
  ffmpeg -y -i "$1" -vf "frei0r=filter_name=glow:filter_params=0.8|0.5" -c:v libx264 -pix_fmt yuv420p "$2"
}

# 6. ANIME GRAIN + VIGNETTE (film look): noise + vignette
fx_filmlook() { # $1 in $2 out
  ffmpeg -y -i "$1" -vf "noise=alls=6:allf=t,vignette=PI/5,eq=contrast=1.06:saturation=1.08" -c:v libx264 -pix_fmt yuv420p "$2"
}

# 7. CHROMA-KEY COMPOSITE (green-screen fx plate over scene)
fx_keycomp() { # $1 fx_plate(green) $2 background $3 out
  ffmpeg -y -i "$1" -i "$2" -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.2[fg];[1:v][fg]overlay=0:0,format=yuv420p" -c:v libx264 -pix_fmt yuv420p "$3"
}

# 8. WIGGLE / SHAKE (impact shake, params in px)
fx_shake() { # $1 in $2 out $3 amplitude $4 start_s $5 end_s
  ffmpeg -y -i "$1" -vf "crop=iw-2*${3:-8}:ih-2*${3:-8}:$3:$3,scale=iw:ih,translate=x='if(between(t,$4,$5),${3:-8}*sin(80*t),0)':y='if(between(t,$4,$5),${3:-8}*cos(63*t),0)'" -c:v libx264 -pix_fmt yuv420p "$2"
}

echo "trackA-ffmpeg-fx-chains: 8 chains defined. Source with 'source ...' or copy a function."
