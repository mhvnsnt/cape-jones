#!/usr/bin/env python3
"""Verify a v2 mix: per-section loudness of the two premaster buses and the
delivered master, vocal-vs-inst offsets, and the beat-body (40-250 Hz)
intro->verse drop inside the delivered file (v1's was ~7.8 dB).
Usage: verify_v2.py <lang> <delivered_mp3>"""
import json, subprocess, sys
import numpy as np
from pedalboard.io import AudioFile

SR = 44100
LANG = sys.argv[1]
MP3 = sys.argv[2]
SECTIONS = [("intro", 0.0, 6.316), ("verseA", 6.316, 18.947), ("chorusA", 18.947, 31.579),
            ("verseB", 31.579, 44.211), ("bridge", 44.211, 53.684), ("chorusB", 53.684, 66.316),
            ("outro", 66.316, 75.789)]
OUT = f"/home/hatch/cj-song-v2-work/work/build/mix2/{LANG}"

def loudness(path, a, b):
    err = subprocess.run(["ffmpeg", "-nostats", "-ss", f"{a}", "-to", f"{b}", "-i", path,
                          "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    j = json.loads(err[err.index("{"):err.rindex("}") + 1])
    return float(j["input_i"]), float(j["input_tp"])

def load(path):
    with AudioFile(path) as f:
        return f.read(f.frames)

def lowband_db(x, a, b):
    seg = x[:, int(a * SR):int(b * SR)].mean(axis=0)
    n = len(seg)
    spec = np.fft.rfft(seg * np.hanning(n))
    fr = np.fft.rfftfreq(n, 1 / SR)
    m = (fr >= 40) & (fr < 250)
    return 10 * np.log10(2 * np.sum(np.abs(spec[m]) ** 2) / n ** 2 + 1e-20)

print(f"--- {LANG} ---")
tot_i, tot_tp = loudness(MP3, 0, 75.789)
print(f"delivered full mix: {tot_i:.1f} LUFS integrated, TP {tot_tp:.1f}")
vb = f"{OUT}/vocal_bus.wav"; ib = f"{OUT}/instrumental.wav"
full = load(MP3)
print("section   vocal_bus  inst_bus  offset   masterLUFS  beatbody(full)")
for name, a, b in SECTIONS:
    v, _ = loudness(vb, a, b)
    i, _ = loudness(ib, a, b)
    m, _ = loudness(MP3, a, b)
    off = f"{v - i:+.1f}" if v > -60 and i > -60 else "  -  "
    print(f"{name:<9} {v:>8.1f} {i:>9.1f} {off:>7} {m:>10.1f} {lowband_db(full, a, b):>10.1f}")
lb = {name: lowband_db(full, a, b) for name, a, b in SECTIONS}
print(f"beat-body drop intro->verseA in delivered mix: {lb['intro'] - lb['verseA']:.1f} dB (v1: 7.8 dB)")
