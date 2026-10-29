#!/bin/bash
set -e
cd ~/workspace/mochiichao-work/title-music/vocal-mix
# V7: lead = WORLD/AVANNA-style transform of Mars's own voice (avanna_style.py, F0 x1.682 + formant shift + breath x0.5)
# No AVANNA voicebank used. Harmonies from warped-norm via rubberband. Vocal bus 10.0, title 0.80, dry lead direct.
ffmpeg -y -v error -i vocal-avanna-autotune-236.wav -i warped-norm.wav \
 -i ../stem-title-melody.wav -i ../stem-title-bass.wav -i ../stem-title-drums.wav \
 -i ../stem-title-guitar.wav -i ../stem-title-synth.wav -i ../stem-title-organ.wav \
 -filter_complex "
[0:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[a1];
[0:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[a2];
[0:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[a3];
[0:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[a4];
[0:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[a5];
[0:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[a6];
[0:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[a7];
[0:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[a8];
[a1][a2][a3][a4][a5][a6][a7][a8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS[leadraw];
[1:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[h1];
[1:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[h2];
[1:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[h3];
[1:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[h4];
[1:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[h5];
[1:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[h6];
[1:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[h7];
[1:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[h8];
[h1][h2][h3][h4][h5][h6][h7][h8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS[hraw];
[leadraw]highpass=f=120,equalizer=f=250:width_type=o:width=1.2:g=-4,equalizer=f=3000:width_type=o:width=1:g=4,equalizer=f=5000:width_type=o:width=1:g=4,equalizer=f=11000:width_type=o:width=1:g=3,agate=threshold=0.02:ratio=10:attack=5:release=100:range=0.05,deesser,acompressor=threshold=0.10:ratio=6:attack=5:release=80:makeup=2,acompressor=threshold=0.10:ratio=4:attack=5:release=60:makeup=1.3,volume=5.0[vlead];
[hraw]highpass=f=120,rubberband=pitch=1.335:tempo=1.0,volume=0.50[vharm];
[vlead]asplit=2[vleadA][vleadB];
[vleadB]adelay=12:all=1,volume=0.30[vhaas];
[vleadA]volume=1.0[vdry];
[vharm][vhaas]amix=inputs=2:normalize=0,chorus=0.6:0.6:20|30:0.3|0.4:4|6:0.4|0.6,aecho=0.8:0.18:140|240:0.35|0.25[wet];
[vdry][wet]amix=inputs=2:normalize=0,volume=6.0[vproc];
[2:a]equalizer=f=3000:width_type=o:width=1:g=-6,equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.70[tmel];
[3:a]volume=1.0[tbass];
[4:a]volume=1.0[tdrum];
[5:a]equalizer=f=3000:width_type=o:width=1:g=-6,equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.70[tgtr];
[6:a]equalizer=f=4000:width_type=o:width=1:g=-3,volume=0.70[tsyn];
[7:a]volume=0.50[torg];
[tmel][tbass][tdrum][tgtr][tsyn][torg]amix=inputs=6:normalize=0,volume=1.00[title];
[title][vsc]sidechaincompress=threshold=0.12:ratio=2:attack=10:release=200:makeup=1[titleduck];
[vproc][titleduck]amix=inputs=2:normalize=0,alimiter=limit=0.89,afade=t=out:st=40.6:d=0.543[out]
" -map "[out]" -ar 44100 -ac 2 mochiichao-title-v3-vocal-mix-v9.wav
ffmpeg -y -v error -i mochiichao-title-v3-vocal-mix-v9.wav -t 41.143 mochiichao-title-v3-vocal-mix-v9-trim.wav && mv mochiichao-title-v3-vocal-mix-v9-trim.wav mochiichao-title-v3-vocal-mix-v9.wav
ls -lh mochiichao-title-v3-vocal-mix-v9.wav
ffmpeg -i mochiichao-title-v3-vocal-mix-v9.wav -af volumedetect -vn -sn -dn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 mochiichao-title-v3-vocal-mix-v9.wav
