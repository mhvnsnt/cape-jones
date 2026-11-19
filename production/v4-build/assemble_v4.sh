#!/bin/bash
# Assemble cj-dance-proof-3d-v4.mp4 from frames/ (1824 rendered; final
# video uses 1819 = 75.79 s at 24 fps, matching the song). Same section
# plan as v3; song = JP v2 mix (v3 used EN; approved mixes rotate).
set -e
cd /home/hatch/workspace/_cj_v4_build
SONG=/home/hatch/workspace/your_files/cape-jones-dance-proof/song/song-full-v2-jp.mp3
OUT=/home/hatch/workspace/your_files/cape-jones-dance-proof/cj-dance-proof-3d-v4.mp4
enc() {
  if [ -n "$3" ]; then VF="-vf $3"; else VF=""; fi
  ffmpeg -v error -y -framerate 24 -start_number $1 -i frames/f%04d.jpg -frames:v $2 $VF -c:v libx264 -crf 18 -pix_fmt yuv420p $4
}
enc 1    384 ""      seg1.mp4
enc 385  384 "hflip" seg2.mp4
enc 769  384 ""      seg3.mp4
enc 1153 384 "hflip" seg4.mp4
enc 1537 283 ""      seg5.mp4
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\nfile 'seg5.mp4'\n" > concat.txt
ffmpeg -v error -y -f concat -safe 0 -i concat.txt -i "$SONG" -c:v copy -c:a aac -b:a 160k -movflags +faststart "$OUT"
echo "ASSEMBLED $OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
