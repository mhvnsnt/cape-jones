#!/usr/bin/env python3
"""Step 2 measurement: diagnose the v1 vocal-vs-beat clash.
Per-section loudness (ffmpeg loudnorm = BS.1770) of the v1 mix ingredients
and the delivered master, plus band-energy masking maps (numpy).
Run with the music-pullin venv python."""
import json, subprocess
import numpy as np
from pedalboard.io import AudioFile

SR = 44100
SECTIONS = [("intro", 0.0, 6.316), ("verseA", 6.316, 18.947), ("chorusA", 18.947, 31.579),
            ("verseB", 31.579, 44.211), ("bridge", 44.211, 53.684), ("chorusB", 53.684, 66.316),
            ("outro", 66.316, 75.789)]
W = "/home/hatch/workspace/_cj-song-work/build"
YF = "/home/hatch/workspace/your_files/cape-jones-dance-proof/song"

def loudness(path, a, b):
    cmd = ["ffmpeg", "-nostats", "-ss", f"{a}", "-to", f"{b}", "-i", path,
           "-af", "loudnorm=print_format=json", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    j = json.loads(err[err.index("{"):err.rindex("}") + 1])
    return float(j["input_i"]), float(j["input_tp"])

def load(path):
    with AudioFile(path) as f:
        return f.read(f.frames)  # (ch, n) float

def band_share(x, a, b, lo, hi):
    seg = x[:, int(a * SR):int(b * SR)]
    mono = seg.mean(axis=0)
    n = len(mono)
    spec = np.abs(np.fft.rfft(mono * np.hanning(n))) ** 2
    fr = np.fft.rfftfreq(n, 1 / SR)
    tot = spec[(fr >= 20) & (fr <= 16000)].sum()
    band = spec[(fr >= lo) & (fr < hi)].sum()
    return band / max(tot, 1e-20), band

print("=== per-section integrated loudness (LUFS) ===")
files = {"vocal_bus(v1 premaster)": f"{W}/mix/vocal_bus.wav",
         "instrumental(v1 premaster)": f"{W}/mix/instrumental.wav",
         "full(v1 delivered master)": f"{YF}/song-full.mp3",
         "instrumental-only(v1 delivered)": f"{YF}/song-instrumental.mp3"}
table = {}
for tag, p in files.items():
    table[tag] = {name: loudness(p, a, b)[0] for name, a, b in SECTIONS}
print("section   " + "".join(f"{t[:22]:>24}" for t in files))
for name, a, b in SECTIONS:
    print(f"{name:<10}" + "".join(f"{table[t][name]:>24.1f}" for t in files))
print("\nvocal-bus minus instrumental (premaster, dB) per section:")
for name, a, b in SECTIONS:
    print(f"  {name:<9} {table['vocal_bus(v1 premaster)'][name] - table['instrumental(v1 premaster)'][name]:+.1f}")

print("\n=== masking map: band share of total energy (%), verseA ===")
a, b = 6.316, 18.947
for tag, p in [("vocal_bus", f"{W}/mix/vocal_bus.wav"), ("stem-lead", f"{W}/wav/stem-lead.wav"),
               ("stem-arp", f"{W}/wav/stem-arp.wav"), ("stem-sparkle", f"{W}/wav/stem-sparkle.wav"),
               ("stem-drums", f"{W}/wav/stem-drums.wav"), ("stem-bass", f"{W}/wav/stem-bass.wav")]:
    x = load(p)
    shares = []
    for lo, hi in [(200, 800), (800, 2000), (2000, 5000), (5000, 9000)]:
        s, _ = band_share(x, a, b, lo, hi)
        shares.append(s * 100)
    print(f"  {tag:<12} 200-800:{shares[0]:5.1f}  800-2k:{shares[1]:5.1f}  2-5k:{shares[2]:5.1f}  5-9k:{shares[3]:5.1f}")

print("\n=== beat body (40-250 Hz) level per section: full master vs instrumental premaster ===")
full = load(f"{YF}/song-full.mp3")
inst = load(f"{W}/mix/instrumental.wav")
def lowband_db(x, a, b):
    seg = x[:, int(a * SR):int(b * SR)].mean(axis=0)
    n = len(seg)
    spec = np.fft.rfft(seg * np.hanning(n))
    fr = np.fft.rfftfreq(n, 1 / SR)
    m = (fr >= 40) & (fr < 250)
    return 10 * np.log10(2 * np.sum(np.abs(spec[m]) ** 2) / n ** 2 + 1e-20)
for name, a, b in SECTIONS:
    print(f"  {name:<9} full:{lowband_db(full, a, b):6.1f}   inst-alone:{lowband_db(inst, a, b):6.1f}")

print("\n=== presence band (2-5 kHz) absolute energy, verseA: vocal vs lead vs arp ===")
def bandabs(p):
    x = load(p)
    _, v = band_share(x, 6.316, 18.947, 2000, 5000)
    return 10 * np.log10(v + 1e-20)
print(f"  vocal_bus {bandabs(f'{W}/mix/vocal_bus.wav'):.1f}   lead {bandabs(f'{W}/wav/stem-lead.wav'):.1f}   arp {bandabs(f'{W}/wav/stem-arp.wav'):.1f}")
