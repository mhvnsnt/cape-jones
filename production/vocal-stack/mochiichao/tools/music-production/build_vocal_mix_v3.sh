#!/bin/bash
set -e
cd ~/workspace/mochiichao-work/title-music/vocal-mix
# Source: warped-norm.wav (global 1.156x warp to 140 BPM, per-phrase RMS normalized to 0.09)
ffmpeg -y -v error -i warped-norm.wav \
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
[vwarp]highpass=f=150,equalizer=f=250:width_type=o:width=1.2:g=-4,equalizer=f=2000:width_type=o:width=1:g=3,equalizer=f=5000:width_type=o:width=1:g=6,equalizer=f=11000:width_type=o:width=1:g=5,acompressor=threshold=0.10:ratio=6:attack=5:release=80:makeup=2,acompressor=threshold=0.08:ratio=4:attack=5:release=60:makeup=1.5[vbase];
[vbase]asplit=5[main7][harm3][orig][sat][sc];
[main7]rubberband=pitch=1.498:tempo=1.0,volume=1.0[lead];
[harm3]rubberband=pitch=1.189:tempo=1.0,volume=0.50[gh3];
[orig]volume=0.15[go];
[sat]acrusher=level_in=1:level_out=1:bits=10:mix=0.5,volume=0.40[gsat];
[sc]volume=1.0[vsc];
[lead][gh3][go][gsat]amix=inputs=4:normalize=0,chorus=0.9:0.9:20|30:0.4|0.5:4|6:0.5|0.8,aecho=0.8:0.35:180|320|520:0.40|0.30|0.20,volume=4.0[vproc];
[1:a]equalizer=f=4000:width_type=o:width=1:g=-8,volume=0.50[tmel];
[2:a]volume=0.90[tbass];
[3:a]volume=0.90[tdrum];
[4:a]equalizer=f=4000:width_type=o:width=1:g=-8,volume=0.50[tgtr];
[5:a]equalizer=f=4000:width_type=o:width=1:g=-6,volume=0.50[tsyn];
[6:a]volume=0.40[torg];
[tmel][tbass][tdrum][tgtr][tsyn][torg]amix=inputs=6:normalize=0,volume=0.25[title];
[title][vsc]sidechaincompress=threshold=0.08:ratio=5:attack=10:release=200:makeup=1[titleduck];
[vproc][titleduck]amix=inputs=2:normalize=0,volume=1.0,alimiter=limit=0.89,afade=t=out:st=40.6:d=0.543[out]
" -map "[out]" -ar 44100 -ac 2 mochiichao-title-v3-vocal-mix-v3.wav
ffmpeg -y -v error -i mochiichao-title-v3-vocal-mix-v3.wav -t 41.143 mochiichao-title-v3-vocal-mix-v3-trim.wav && mv mochiichao-title-v3-vocal-mix-v3-trim.wav mochiichao-title-v3-vocal-mix-v3.wav
ls -lh mochiichao-title-v3-vocal-mix-v3.wav
ffmpeg -i mochiichao-title-v3-vocal-mix-v3.wav -af volumedetect -vn -sn -dn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 mochiichao-title-v3-vocal-mix-v3.wav
