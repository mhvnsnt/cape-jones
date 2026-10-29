#!/bin/bash
set -e
cd ~/workspace/mochiichao-work/title-music/vocal-mix
V=vocal.wav
T=../mochiichao-title-v3.wav
# Phrases: source_start-source_end -> bar_start, atempo (orig_len/target_len)
# P1 0.82-8.35 -> 0.000, atempo 1.098 ; P2 9.36-15.91 -> 6.857, 0.955 ; P3 16.94-23.81 -> 13.714, 1.002
# P4 25.02-31.35 -> 20.571, 0.923 ; P5 32.51-39.49 -> 27.429, 1.018 ; P6 39.85-41.42 -> 34.286, 0.916
# P7 41.80-43.53 -> 36.000, 1.009 ; P8 43.85-46.72 -> 37.714, 1.000 (natural, ends 40.58)
ffmpeg -y -v error -i $V -i $T -filter_complex "
[0:a]atrim=start=0.82:end=8.35,asetpts=PTS-STARTPTS,atempo=1.098,adelay=0:all=1[p1];
[0:a]atrim=start=9.36:end=15.91,asetpts=PTS-STARTPTS,atempo=0.955,adelay=6857:all=1[p2];
[0:a]atrim=start=16.94:end=23.81,asetpts=PTS-STARTPTS,atempo=1.002,adelay=13714:all=1[p3];
[0:a]atrim=start=25.02:end=31.35,asetpts=PTS-STARTPTS,atempo=0.923,adelay=20571:all=1[p4];
[0:a]atrim=start=32.51:end=39.49,asetpts=PTS-STARTPTS,atempo=1.018,adelay=27429:all=1[p5];
[0:a]atrim=start=39.85:end=41.42,asetpts=PTS-STARTPTS,atempo=0.916,adelay=34286:all=1[p6];
[0:a]atrim=start=41.80:end=43.53,asetpts=PTS-STARTPTS,atempo=1.009,adelay=36000:all=1[p7];
[0:a]atrim=start=43.85:end=46.72,asetpts=PTS-STARTPTS,adelay=37714:all=1[p8];
[p1][p2][p3][p4][p5][p6][p7][p8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS[vraw];
[vraw]highpass=f=100,equalizer=f=250:width_type=o:width=1.2:g=-3,equalizer=f=4000:width_type=o:width=1:g=3,equalizer=f=11000:width_type=o:width=1:g=2,volume=6,acompressor=threshold=0.12:ratio=4:attack=10:release=100:makeup=2[vlead];
[vlead]asplit=3[lead][ghost_up][ghost_down];
[ghost_up]rubberband=pitch=1.189:tempo=1.0,volume=0.35,adelay=15:all=1[gup];
[ghost_down]rubberband=pitch=0.891:tempo=1.0,volume=0.20,adelay=30:all=1[gdown];
[lead][gup][gdown]amix=inputs=3:normalize=0,chorus=0.8:0.8:20|30:0.4|0.5:4|6:0.5|0.8,aecho=0.8:0.25:180|320|520:0.35|0.25|0.15[vproc];
[1:a]volume=0.60[title];
[vproc][title]amix=inputs=2:normalize=0,volume=1.4,alimiter=limit=0.89,afade=t=out:st=40.6:d=0.543[out]
" -map "[out]" -ar 44100 -ac 2 mochiichao-title-v3-vocal-mix-v1.wav
ls -lh mochiichao-title-v3-vocal-mix-v1.wav
ffmpeg -i mochiichao-title-v3-vocal-mix-v1.wav -af volumedetect -vn -sn -dn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume|Duration"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 mochiichao-title-v3-vocal-mix-v1.wav
