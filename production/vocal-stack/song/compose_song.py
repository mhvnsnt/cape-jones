#!/usr/bin/env python3
"""Compose the Cape Jones dance song (extends the Tamagotchi loop to full
anime-intro length) following tools/music-production/compose_v3.py conventions:
type-1 MIDI, TPB 480, one voice per track, fixed GM voicegroup, balance in
velocities. Key C major, 152 BPM, 48 bars = 75.79 s.
Outputs: song-full.mid, stem-*.mid, vocal-melody.mid, vocal_notes.json."""
import json, os, sys
import mido
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song_data import PHRASES, SECTIONS, CHORDS, BPM, TOTAL_BARS

TPB = 480
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
os.makedirs(OUT, exist_ok=True)

def make_track(ch, prog, notes):
    tr = mido.MidiTrack()
    if prog is not None and ch != 9:
        tr.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    ev = []
    for midi, start, dur, vel in notes:
        ev.append((int(round(start * TPB)), 'on', midi, vel))
        ev.append((int(round((start + dur) * TPB)), 'off', midi, 0))
    ev.sort(key=lambda e: (e[0], 0 if e[1] == 'off' else 1))
    last = 0
    for tick, kind, midi, vel in ev:
        d = tick - last; last = tick
        tr.append(mido.Message('note_on' if kind == 'on' else 'note_off',
                               channel=ch, note=midi,
                               velocity=vel if kind == 'on' else 0, time=d))
    tr.append(mido.MetaMessage('end_of_track', time=0))
    return tr

def save_midi(path, tracks):
    mid = mido.MidiFile(type=1, ticks_per_beat=TPB)
    meta = mido.MidiTrack()
    meta.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM), time=0))
    meta.append(mido.MetaMessage('end_of_track', time=0))
    mid.tracks.append(meta)
    for tr in tracks:
        mid.tracks.append(tr)
    mid.save(path)

# instrumental lead phrases for the intro (reprise of the loop's LEAD_A/B)
LEAD_A = {0: [(76,0,.5,104),(79,.5,.5,100),(84,1,.75,108),(79,1.75,.25,96),(81,2,.5,102),(79,2.5,.5,98),(76,3,.5,100),(74,3.5,.5,96)],
          1: [(74,0,.5,100),(79,.5,.5,102),(83,1,.75,106),(79,1.75,.25,95),(81,2,.5,100),(83,2.5,.5,102),(86,3,.5,106),(83,3.5,.5,98)],
          2: [(84,0,.5,104),(83,.5,.5,98),(81,1,.75,102),(76,1.75,.25,94),(81,2,.5,100),(84,2.5,.5,104),(83,3,.5,99),(81,3.5,.5,96)],
          3: [(81,0,.5,102),(84,.5,.5,104),(89,1,.75,108),(84,1.75,.25,96),(83,2,.5,100),(81,2.5,.5,98),(79,3,.5,98),(76,3.5,.5,95)]}
LEAD_B = {0: [(84,0,.25,106),(84,.25,.25,100),(84,.5,.5,104),(79,1,.5,96),(81,1.5,.5,100),(79,2,.5,97),(76,2.5,.5,95),(72,3,1,103)],
          1: [(86,0,.5,104),(83,.5,.5,99),(79,1,.75,100),(74,1.75,.25,92),(79,2,.5,98),(83,2.5,.5,101),(81,3,.5,100),(79,3.5,.5,97)],
          2: [(76,0,.5,98),(81,.5,.5,102),(84,1,.75,106),(81,1.75,.25,95),(79,2,.5,98),(76,2.5,.5,95),(74,3,.5,94),(76,3.5,.5,96)],
          3: [(77,0,.5,100),(81,.5,.5,102),(84,1,.75,105),(81,1.75,.25,95),(79,2,.5,99),(81,2.5,.5,100),(84,3,1,108)]}

def in_sec(bar, name):
    return any(s == name and a <= bar < b for s, a, b in SECTIONS)

lead, arp, bass, spark, pad, drums = [], [], [], [], [], []
for bar in range(TOTAL_BARS):
    ci = bar % 4
    root, tones = CHORDS[ci]
    base = bar * 4
    chorus = in_sec(bar, "chorusA") or in_sec(bar, "chorusB")
    # lead: intro riff (bars 0-3), quiet octave-up double under chorus B
    if bar < 4:
        phr = LEAD_A if (bar // 4) % 2 == 0 else LEAD_B
        for n, s, d, v in phr[ci]:
            lead.append((n, base + s, d, v))
    # arp 16ths (loop recipe)
    seq = [tones[0] + 12, tones[1] + 12, tones[2] + 12, tones[1] + 12,
           tones[0] + 24, tones[1] + 12, tones[2] + 12, tones[1] + 12]
    for i in range(16):
        arp.append((seq[i % len(seq)], base + i * 0.25, 0.22, 56 if chorus else (52 if i % 4 else 60)))
    # bass: bouncing roots; chorus adds mid-beat pop
    for b in range(4):
        bass.append((root, base + b, 0.45, 108))
        bass.append((root + 12, base + b + 0.5, 0.22, 88))
        if chorus:
            bass.append((root + 12, base + b + 0.75, 0.15, 70))
    # sparkle on cycle starts + chorus answers
    if bar % 4 == 0:
        spark.append((tones[2] + 36, base, 0.9, 62))
        spark.append((tones[1] + 36, base + 2, 0.7, 54))
    if chorus and bar % 2 == 1:
        spark.append((tones[0] + 36, base + 3, 0.5, 50))
    # pad: whole-bar chords under bridge + choruses
    if chorus or in_sec(bar, "bridge"):
        for t in tones:
            pad.append((t + 12, base, 3.9, 40))
    # drums
    for b, (kn, kv) in enumerate([(36, 112), (38, 104), (36, 110), (38, 106)]):
        drums.append((kn, base + b, 0.2, kv))
    for e in range(8):
        drums.append((42, base + e * 0.5, 0.1, 66 if e % 2 == 0 else 50))
    if bar % 4 == 3:
        drums.append((46, base + 3.5, 0.4, 70))
    if bar in (12, 34):  # chorus crashes
        drums.append((49, base, 1.5, 100))
    if bar == 46:
        drums.append((49, base, 1.5, 90))

# chorus-B lead double (octave up, quiet) from the vocal phrases
vocal_notes = []
for pi, p in enumerate(PHRASES):
    t = p["start_bar"] * 4.0
    for (midi, dur), mora in zip(p["notes"], p["morae"]):
        vocal_notes.append(dict(phrase=pi, section=p["section"], mora=mora,
                                midi=midi, start_beat=t, dur_beats=dur))
        if p["section"] == "chorusB":
            lead.append((midi + 12, t, dur * 0.9, 58))
        t += dur

tracks = [make_track(0, 80, lead), make_track(1, 80, arp), make_track(2, 38, bass),
          make_track(3, 112, spark), make_track(4, 89, pad), make_track(9, None, drums)]
save_midi(os.path.join(OUT, 'song-full.mid'), tracks)
for name, tr in zip(['lead', 'arp', 'bass', 'sparkle', 'pad', 'drums'], tracks):
    save_midi(os.path.join(OUT, f'stem-{name}.mid'), [tr])
mel = [(n["midi"], n["start_beat"], n["dur_beats"], 100) for n in vocal_notes]
save_midi(os.path.join(OUT, 'vocal-melody.mid'), [make_track(0, 80, mel)])
json.dump(vocal_notes, open(os.path.join(OUT, 'vocal_notes.json'), 'w'), ensure_ascii=False, indent=1)
print(f"composed {TOTAL_BARS} bars; vocal notes={len(vocal_notes)}; "
      f"lead {len(lead)} arp {len(arp)} bass {len(bass)} spark {len(spark)} pad {len(pad)} drums {len(drums)}")
