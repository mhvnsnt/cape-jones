"""Beat-sync PREP ONLY, 2026-11-01. No decision applied to any final.
Song: 152 BPM (song_data.py BPM=152, 48 bars, 75.789s). Visual grid: ~107 BPM nominal
(task + 12-principles checklist: ~14f beat grid). Ratio 152/107 = 1.42056.
Measured cross-check (dance-flash-fix REPORT): v2 SFX events per 123f loop at
frames 0,14,27,41,68,82,96,110; gaps 14,13,14,27(=2 beats),14,14,14,13-to-loop.
Beat slots per loop = 9, mean slot 123/9 = 13.67f @24fps = 0.569s = 105.4 BPM,
so the measured grid is 103-107 BPM depending on median vs mean; samples below
use the task nominal 107 BPM (factor 1.42056) and say so. Mars decides."""
import math, wave, struct, csv, os
OUT = os.path.dirname(os.path.abspath(__file__))
SONG_BPM, VIS_BPM = 152.0, 107.0
SONG_BEAT, VIS_BEAT = 60/SONG_BPM, 60/VIS_BPM
DUR = 75.789
print(f"song beat={SONG_BEAT:.5f}s bar={4*SONG_BEAT:.5f}s beats_in_song={DUR/SONG_BEAT:.1f}")
print(f"visual beat={VIS_BEAT:.5f}s beats_in_75.789s={DUR/VIS_BEAT:.1f} drift/sec={(SONG_BPM-VIS_BPM)/60:.3f} beats/s")
print(f"ratio={SONG_BPM/VIS_BPM:.5f} stretched_duration={DUR*SONG_BPM/VIS_BPM:.2f}s semitones={12*math.log2(VIS_BPM/SONG_BPM):.2f}")
# --- timing tables ---
with open(os.path.join(OUT,'beatsync-timing-tables-20261101.csv'),'w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['t_sec','song_beat_index','song_beat_time','visual_beat_index_nom107','visual_beat_time','drift_beats_song_minus_visual','drift_sec_at_song_grid'])
    for t in [0,5,10,15,20,30,40,50,60,75.789]:
        sb=t/SONG_BEAT; vb=t/VIS_BEAT
        w.writerow([t, round(sb,2), round(sb*SONG_BEAT,3), round(vb,2), round(vb*VIS_BEAT,3), round(sb-vb,2), round((sb-vb)*SONG_BEAT,3)])
with open(os.path.join(OUT,'beatsync-option-tables-20261101.csv'),'w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['option','event_or_beat','original_frame_24fps','original_time_s','new_frame_24fps','new_time_s','shift_frames','note'])
    events=[0,14,27,41,68,82,96,110,123]
    beat_idx=[0,1,2,3,5,6,7,8,9]
    # A: uniform speedup 1.42056
    for e in events:
        nf=e/(SONG_BPM/VIS_BPM)
        w.writerow(['A_retime_visual_to_152',f'sfx_event_orig_f{e}',e,round(e/24,3),round(nf,1),round(nf/24,3),round(nf-e,1),'uniform /1.42056; grid now = song grid'])
    # C: snap each event to its song-beat frame, snapped to even (on-2s)
    for e,b in zip(events,beat_idx):
        raw=b*SONG_BEAT*24; snapped=round(raw/2)*2
        w.writerow(['C_regrid_visual_to_song_beats',f'sfx_event_beat{b}',e,round(e/24,3),snapped,round(snapped/24,3),snapped-e,'nearest song beat, even-frame snap; holds absorb shift'])
    # B: stretched audio beat times (first 10 beats)
    for k in range(11):
        w.writerow(['B_stretch_audio_to_107',f'song_beat{k}',round(k*SONG_BEAT*24,1),round(k*SONG_BEAT,3),round(k*VIS_BEAT*24,1),round(k*VIS_BEAT,3),round(k*(VIS_BEAT-SONG_BEAT)*24,1),'atempo 0.70395; beat k moves later'])
# --- click track: 1000 Hz ping 0.04s at song-beat times, 4s ---
def click_wav(path, dur, beat):
    sr=44100; n=int(sr*dur); data=bytearray()
    beats=[i*beat for i in range(int(dur/beat)+1)]
    for i in range(n):
        t=i/sr; v=0.0
        for b in beats:
            if b<=t<b+0.04:
                v=0.5*math.sin(2*math.pi*1000*(t-b))*(1-(t-b)/0.04)
        data+=struct.pack('<h', int(v*32767))
    with wave.open(path,'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(bytes(data))
    print('click', path, 'beats at', [round(b,3) for b in beats])
click_wav(os.path.join(OUT,'song-beat-click-152bpm-20261101.wav'), 4.0, SONG_BEAT)
print('tables written')
