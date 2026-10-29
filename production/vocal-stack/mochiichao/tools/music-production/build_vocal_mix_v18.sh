#!/bin/bash
set -e
cd ~/workspace/mochiichao-work/title-music/vocal-mix
# V10 SIMPLIFIED: the WORLD resynthesis in v8/v9 was stripping notes (6.5% silent
# 50ms frames inside phrases vs 0% in the source) and the gate + aggressive denoise
# chopped words further. V10 removes all three: NO world, NO gate, NO afftdn.
# Lead = rubberband +9 (warped-norm median 203Hz -> ~341Hz, neptune target) with
# formant shifted, the same smooth lead style as v6 which Mars called "a lot closer".
# Beat fix from v9 kept: title 1.00, vocal 6.0, NO master compressor, gentle sidechain only.
ffmpeg -y -v error -i vocal-autotune-v6.wav -i warped-norm.wav \
 -i ../stem-title-melody.wav -i ../stem-title-bass.wav -i ../stem-title-drums.wav \
 -i ../stem-title-guitar.wav -i ../stem-title-synth.wav -i ../stem-title-organ.wav -i vocal-overdub-v6.wav -i vocal-autotune-v7.wav -i vocal-harm-v6.wav -i vocal-oct-v6.wav \
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
[vwarp]highpass=f=120,equalizer=f=250:width_type=o:width=1.2:g=-4,equalizer=f=3000:width_type=o:width=1:g=6,equalizer=f=5000:width_type=o:width=1:g=6,equalizer=f=8000:width_type=o:width=1:g=5,equalizer=f=12000:width_type=s:width=1:g=4,deesser=i=0.6:f=0.16,acompressor=threshold=0.10:ratio=4:attack=5:release=80:makeup=2,volume=3.0[vlead];
[10:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[h1];
[10:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[h2];
[10:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[h3];
[10:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[h4];
[10:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[h5];
[10:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[h6];
[10:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[h7];
[10:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[h8];
[h1][h2][h3][h4][h5][h6][h7][h8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS,volume=0.50[vharm];
[8:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[o1];
[8:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[o2];
[8:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[o3];
[8:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[o4];
[8:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[o5];
[8:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[o6];
[8:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[o7];
[8:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[o8];
[o1][o2][o3][o4][o5][o6][o7][o8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS,chorus=0.5:0.5:25|35:0.4|0.5:5|7:0.5|0.6,volume=0.35[overdub];
[11:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[u1];
[11:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[u2];
[11:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[u3];
[11:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[u4];
[11:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[u5];
[11:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[u6];
[11:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[u7];
[11:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[u8];
[u1][u2][u3][u4][u5][u6][u7][u8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS,volume=0.25[voct];
[9:a]atrim=start=0:end=6.51,asetpts=PTS-STARTPTS,adelay=0:all=1[t1];
[9:a]atrim=start=7.39:end=13.06,asetpts=PTS-STARTPTS,adelay=6857:all=1[t2];
[9:a]atrim=start=13.95:end=19.89,asetpts=PTS-STARTPTS,adelay=13714:all=1[t3];
[9:a]atrim=start=20.93:end=26.45,asetpts=PTS-STARTPTS,adelay=20571:all=1[t4];
[9:a]atrim=start=27.41:end=33.32,asetpts=PTS-STARTPTS,adelay=27429:all=1[t5];
[9:a]atrim=start=33.77:end=35.12,asetpts=PTS-STARTPTS,adelay=34286:all=1[t6];
[9:a]atrim=start=35.46:end=36.89,asetpts=PTS-STARTPTS,adelay=36000:all=1[t7];
[9:a]atrim=start=37.24:end=39.81,asetpts=PTS-STARTPTS,adelay=37714:all=1[t8];
[t1][t2][t3][t4][t5][t6][t7][t8]amix=inputs=8:normalize=0,apad=whole_dur=41.143,atrim=0:41.143,asetpts=PTS-STARTPTS,highpass=f=120,equalizer=f=250:width_type=o:width=1.2:g=-4,equalizer=f=3000:width_type=o:width=1:g=6,equalizer=f=5000:width_type=o:width=1:g=6,equalizer=f=8000:width_type=o:width=1:g=5,equalizer=f=12000:width_type=s:width=1:g=4,deesser=i=0.6:f=0.16,acompressor=threshold=0.10:ratio=4:attack=5:release=80:makeup=2,volume=3.0,volume=1.5[third];
[vlead]volume=0.30[vor];
[vlead]acrusher=level_in=1:level_out=1:bits=10:mix=0.3,volume=0.50[vsat];
[vlead]volume=1.0[vsc];
[vlead]asplit=3[vleadA][vleadB][vleadC];
[vleadB]adelay=12:all=1,volume=0.30[vhaas];
[vleadC]acompressor=threshold=0.05:ratio=10:attack=5:release=50:makeup=3,volume=0.15[vott];
[vleadA]volume=1.0[vdry];
[vharm][vor][vsat][vhaas][overdub][vott][voct][third]amix=inputs=8:normalize=0,chorus=0.6:0.6:20|30:0.3|0.4:4|6:0.4|0.6,aecho=0.8:0.25:321|642:0.35|0.18[wet];
[vdry][wet]amix=inputs=2:normalize=0,volume=4.0,afade=t=out:st=39.81:d=0.5[vproc];
[2:a]equalizer=f=3000:width_type=o:width=1:g=-8,equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.70[tmel];
[3:a]volume=1.0[tbass];
[4:a]volume=1.0[tdrum];
[6:a]equalizer=f=3000:width_type=o:width=1:g=-8,equalizer=f=4000:width_type=o:width=1:g=-4,volume=0.70[tgtr];
[6:a]equalizer=f=3000:width_type=o:width=1:g=-8,volume=0.70[tsyn];
[7:a]volume=0.50[torg];
[tmel][tbass][tdrum][tgtr][tsyn][torg]amix=inputs=6:normalize=0,volume=1.00[title];
[title][vsc]sidechaincompress=threshold=0.12:ratio=2:attack=10:release=200:makeup=1[titleduck];
[vproc][titleduck]amix=inputs=2:normalize=0,equalizer=f=100:width_type=s:width=1:g=-2,equalizer=f=400:width_type=o:width=1:g=-3,equalizer=f=10000:width_type=s:width=1:g=2,acompressor=threshold=0.20:ratio=2:attack=10:release=120:makeup=2,alimiter=limit=0.89,afade=t=in:st=0:d=4,afade=t=out:st=40.6:d=0.543[out]
" -map "[out]" -ar 44100 -ac 2 mochiichao-title-v3-vocal-mix-v18.wav
ffmpeg -y -v error -i mochiichao-title-v3-vocal-mix-v18.wav -t 41.143 mochiichao-title-v3-vocal-mix-v18-trim.wav && mv mochiichao-title-v3-vocal-mix-v18-trim.wav mochiichao-title-v3-vocal-mix-v18.wav
ls -lh mochiichao-title-v3-vocal-mix-v18.wav
ffmpeg -i mochiichao-title-v3-vocal-mix-v18.wav -af volumedetect -vn -sn -dn -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 mochiichao-title-v3-vocal-mix-v18.wav
