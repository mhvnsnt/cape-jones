import json, csv, math, os
from pathlib import Path
D=Path.home()/"workspace/cape-jones-rig/tempo-confusion-research-20261101"
FPS=24
def beat_sec(bpm): return 60.0/bpm
def beat_frames(bpm): return beat_sec(bpm)*FPS
for bpm in (107,152):
    print(bpm, round(beat_sec(bpm),4), round(beat_frames(bpm),3))
# 1 beat grid csv: 32 beats both tempos, frame, time, timecode
rows=[]
for i in range(33):
    rows.append({"beat":i, "time_107_s":round(i*beat_sec(107),3), "frame_107":round(i*beat_frames(107),2),
                 "time_152_s":round(i*beat_sec(152),3), "frame_152":round(i*beat_frames(152),2)})
with open(D/"beat-grid-107-vs-152-20261101.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# 2 tempo map json, SMPTE-locked hit points: animatic 332f, plus mixes
tempo_map={
 "fps":FPS, "tempos":{"picture_current_BPM":107,"song_BPM":152},
 "beat":{"107_BPM":{"seconds":round(beat_sec(107),4),"frames":round(beat_frames(107),3)},
         "152_BPM":{"seconds":round(beat_sec(152),4),"frames":round(beat_frames(152),3)}},
 "bar_4beats":{"107_frames":round(4*beat_frames(107),2),"152_frames":round(4*beat_frames(152),2)},
 "stretch":{"152_to_107_duration_factor":round(152/107,5),"152_to_107_speed":round(107/152,5),
            "107_to_152_duration_factor":round(107/152,5)},
 "existing_mixes":{"107_BPM":{"duration_s":17.94,"frames_at_24fps":round(17.94*24,1)},
                   "152_BPM":{"duration_s":12.63,"frames_at_24fps":round(12.63*24,1)},
                   "ratio_107_over_152":round(17.94/12.63,4),"LUFS":"-14.0 PASS both"},
 "animatic":{"frames":332,"seconds":round(332/24,3)},
 "rule":"Hit points are locked to SMPTE/time (seconds+frames), NOT to bars/beats. Changing tempo moves bars/beats, hit points stay put. That is why a tempo change forces either picture re-time, song re-time, or decoupling.",
 "beat_grid_32_beats":rows,
}
json.dump(tempo_map,open(D/"tempo-map-20261101.json","w"),indent=2)
# 3 re-time calculator table: same musical length in beats -> frames at each tempo; same picture length in frames -> beats at each tempo
calc=[]
for beats in [1,2,4,8,12,16,24,32,48]:
    calc.append({"beats":beats,"frames_at_107":round(beats*beat_frames(107),1),"frames_at_152":round(beats*beat_frames(152),1),
                 "frames_saved_going_107_to_152":round(beats*(beat_frames(107)-beat_frames(152)),1),
                 "seconds_at_107":round(beats*beat_sec(107),2),"seconds_at_152":round(beats*beat_sec(152),2)})
for frames in [24,48,96,132,200,332,430]:
    calc.append({"picture_frames":frames,"beats_at_107":round(frames/beat_frames(107),2),"beats_at_152":round(frames/beat_frames(152),2)})
json.dump(calc,open(D/"retime-calculator-20261101.json","w"),indent=2)
with open(D/"retime-calculator-20261101.csv","w",newline="") as f:
    # separate sections: write beats table only for csv simplicity
    w=csv.DictWriter(f,fieldnames=["beats","frames_at_107","frames_at_152","frames_saved_going_107_to_152","seconds_at_107","seconds_at_152"])
    w.writeheader()
    for r in calc:
        if "beats" in r: w.writerow(r)
print("wrote", len(rows), "beat rows,", len(calc), "calc rows")
# worked example: a 13-14f move (1 beat at 107) becomes 9-10f at 152; a 332f animatic holding 24.7 beats at 107 holds 35.0 beats at 152
print("332f beats 107:",332/beat_frames(107),"152:",332/beat_frames(152))
print("24 beats: 107 frames",24*beat_frames(107),"152 frames",24*beat_frames(152))
