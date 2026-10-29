#!/bin/bash
set -e
cd ~/workspace/mochiichao-work/title-music/vocal-mix
V=vocal.wav
# Step 1: ONE global tempo warp to 140 BPM (vocal ~121.5 BPM -> 140, factor 1.156), pitch preserved
ffmpeg -y -v error -i $V -af "atrim=start=0.82,asetpts=PTS-STARTPTS,atempo=1.156" warped.wav
# Warped phrase times (scaled from original, start trimmed at 0.82):
# P1 0-6.51, P2 7.39-13.06, P3 13.95-19.89, P4 20.93-26.45, P5 27.41-33.32, P6 33.77-35.12, P7 35.46-36.89, P8 37.24-39.81
# Bar starts: P1 0, P2 6857, P3 13714, P4 20571, P5 27429, P6 34286, P7 36000, P8 37714 (ms)
ffmpeg -y -v error -i warped.wav \
 -i ../stem-title-melody.wav -i ../stem-title-bass.wav -i ../stem-title-drums.wav \
 -i ../stem-title-guitar.wav -i ../stem-title-synth.wav -i ../stem-title-organ.wav \
 -filter_complex "
[0:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[w1];
[0:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[w2];
[0:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[w3];
[0:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[w4];
[0:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[w5];
[0:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[w6];
[0:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[w7];
[0:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[w8];
[w1][w2][w3][w4][w5][w6][w7][w8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS[vwarp];
[vwarp]highpass=f=150,equalizer=f=250:width_type=o:width=1.2:g=-4,equalizer=f=5000:width_type=o:width=1:g=5,equalizer=f=11000:width_type=o:width=1:g=4,volume=4,acompressor=threshold=0.10:ratio=6:attack=5:release=80:makeup=2[vbase];
[vbase]asplit=4[main][up7][orig][sat];
[main]rubberband=pitch=1.189:tempo=1.0,volume=1.0[lead];
[up7]rubberband=pitch=1.498:tempo=1.0,volume=0.35,pan=stereo|c0=0.8*c0|c1=0.2*c1[g7];
[orig]volume=0.30,pan=stereo|c0=0.2*c0|c1=0.8*c1[gorig];
[sat]acrusher=level_in=1:level_out=1:bits=10:mix=0.5,volume=0.25[gsat];
[lead][g7][gorig][gsat]amix=inputs=4:normalize=0,chorus=0.9:0.9:20|30:0.4|0.5:4|6:0.5|0.8,aecho=0.8:0.35:180|320|520:0.40|0.30|0.20,volume=2.4[vproc];
[1:a]equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.50[tmel];
[2:a]volume=0.90[tbass];
[3:a]volume=0.90[tdrum];
[4:a]equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.50[tgtr];
[5:a]equalizer=f=4000:width_type=o:width=1:g=-3,volume=0.50[tsyn];
[6:a]volume=0.40[torg];
[tmel][tbass][tdrum][tgtr][tsyn][torg]amix=inputs=6:normalize=0,volume=0.35[title];
[vproc][title]amix=inputs=2:normalize=0,volume=1.2,alimiter=limit=0.89,afade=t=out:st=40.6:d=0.543[out]
" -map "[out]" -ar 44100 -ac 2 mochiichao-title-v3-vocal-mix-v2.wav
ffmpeg -y -v error -i mochiichao-title-v3-vocal-mix-v2.wav -t 41.143 mochiichao-title-v3-vocal-mix-v2-trim.wav && mv mochiichao-title-v3-vocal-mix-v2-trim.wav mochiichao-title-v3-vocal-mix-v2.wav
ls -lh mochiichao-title-v3-vocal-mix-v2.wav
ffmpeg -i mochiichao-title-v3-vocal-mix-v2.wav -af volumedetect -vn -sn -dn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 mochiichao-title-v3-vocal-mix-v2.wav
