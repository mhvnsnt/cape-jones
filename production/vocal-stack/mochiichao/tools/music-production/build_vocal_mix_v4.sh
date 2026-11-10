#!/bin/bash
set -e
cd ~/workspace/mochiichao-work/title-music/vocal-mix
# V4: reference-derived from PSO + neptune babii analysis (2026-10-26)
# - beat BACK UP: title bus 0.50 (v3 was 0.25), gentle sidechain ratio 2 (v3 was 5)
# - vocal BETWEEN v2/v3: bus 2.5 (v2 2.4, v3 4.0), master 1.3 -> target mix RMS ~0.18 (neptune level)
# - pitch: main lead +9 semitones (1.682) to match neptune HP-pitch median ~350Hz vs Mars raw ~210Hz
# - reverb DOWN: echo wet 0.18 (v3 0.35), delays 140/240ms only, chorus lighter
# - EQ: air boost cut back (+3@5k, +2@11k vs v3 +6/+5) - references are bass-heavy, not air-heavy
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
[vwarp]highpass=f=120,equalizer=f=250:width_type=o:width=1.2:g=-3,equalizer=f=2000:width_type=o:width=1:g=3,equalizer=f=5000:width_type=o:width=1:g=3,equalizer=f=11000:width_type=o:width=1:g=2,acompressor=threshold=0.10:ratio=6:attack=5:release=80:makeup=2,acompressor=threshold=0.10:ratio=3:attack=5:release=60:makeup=1.3[vbase];
[vbase]asplit=5[main9][harm5][orig][sat][sc];
[main9]rubberband=pitch=1.682:tempo=1.0,volume=1.0[lead];
[harm5]rubberband=pitch=1.335:tempo=1.0,volume=0.45[gh5];
[orig]volume=0.10[go];
[sat]acrusher=level_in=1:level_out=1:bits=10:mix=0.5,volume=0.50[gsat];
[sc]volume=1.0[vsc];
[lead][gh5][go][gsat]amix=inputs=4:normalize=0,chorus=0.6:0.6:20|30:0.3|0.4:4|6:0.4|0.6,aecho=0.8:0.18:140|240:0.35|0.25,volume=2.5[vproc];
[1:a]equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.70[tmel];
[2:a]volume=1.0[tbass];
[3:a]volume=1.0[tdrum];
[4:a]equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.70[tgtr];
[5:a]equalizer=f=4000:width_type=o:width=1:g=-3,volume=0.70[tsyn];
[6:a]volume=0.50[torg];
[tmel][tbass][tdrum][tgtr][tsyn][torg]amix=inputs=6:normalize=0,volume=0.50[title];
[title][vsc]sidechaincompress=threshold=0.12:ratio=2:attack=10:release=200:makeup=1[titleduck];
[vproc][titleduck]amix=inputs=2:normalize=0,volume=1.3,alimiter=limit=0.89,afade=t=out:st=40.6:d=0.543[out]
" -map "[out]" -ar 44100 -ac 2 mochiichao-title-v3-vocal-mix-v4.wav
ls -lh mochiichao-title-v3-vocal-mix-v4.wav
ffmpeg -i mochiichao-title-v3-vocal-mix-v4.wav -af volumedetect -vn -sn -dn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 mochiichao-title-v3-vocal-mix-v4.wav
