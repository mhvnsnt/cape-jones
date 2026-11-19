#!/bin/bash
# Post-assembly verification assets for cj-dance-proof-3d-v3:
#  - contact sheet across lighting states (dip + shrug frames)
#  - full-res frames at motion extremes + zoomed crops (shoulders, hem,
#    between-the-legs) for the one-piece-cape check
set -e
cd /home/hatch/workspace/_cj-dance3d-v3
V=/home/hatch/workspace/your_files/cape-jones-dance-proof/cj-dance-proof-3d-v3.mp4
mkdir -p verify
# sheet: day dip(33) magenta shrug(423) cyan dip(801) / night dip(1185) day dip2(1569) day shrug(1575)
for f in 33 423 801 1185 1569 1575; do
  ffmpeg -v error -y -i "$V" -vf "select='eq(n\,$((f-1)))',scale=640:360" -vsync 0 -frames:v 1 verify/tile_$f.png
done
ffmpeg -v error -y -i verify/tile_33.png -i verify/tile_423.png -i verify/tile_801.png \
  -i verify/tile_1185.png -i verify/tile_1569.png -i verify/tile_1575.png \
  -filter_complex "[0][1][2][3][4][5]xstack=inputs=6:layout=0_0|640_0|1280_0|0_360|640_360|1280_360" \
  /home/hatch/workspace/your_files/cape-jones-dance-proof/cj-dance-proof-3d-v3-sheet.png
# extremes for zoom crops: biggest dip 33 (day), 801 (cyan), night dip 1185, shrug 1575
for f in 33 801 1185 1575; do
  ffmpeg -v error -y -i "$V" -vf "select='eq(n\,$((f-1)))'" -vsync 0 -frames:v 1 verify/x_$f.png
done
# zoomed crops (character sits center-frame; coords from the check stills)
ffmpeg -v error -y -i verify/x_33.png   -vf "crop=520:210:220:30,scale=1040:420"  verify/z_shoulders_33.png
ffmpeg -v error -y -i verify/x_33.png   -vf "crop=520:190:220:350,scale=1040:380" verify/z_hem_33.png
ffmpeg -v error -y -i verify/x_33.png   -vf "crop=320:280:320:250,scale=960:840"  verify/z_legs_33.png
ffmpeg -v error -y -i verify/x_1185.png -vf "crop=520:210:220:30,scale=1040:420"  verify/z_shoulders_1185.png
ffmpeg -v error -y -i verify/x_1185.png -vf "crop=520:190:220:350,scale=1040:380" verify/z_hem_1185.png
ffmpeg -v error -y -i verify/x_1575.png -vf "crop=520:210:220:30,scale=1040:420"  verify/z_shoulders_1575.png
echo VERIFY_ASSETS_DONE
ls verify/
