#!/usr/bin/env python3
"""WORLD vocaloid transform + hard autotune to D major (title v3 key).
Open-source Antares-style function, NOT Antares software: F0 is snapped to the
nearest D-major scale note with zero smoothing (retune speed 0 = hard tune),
after the +9 semitone vocaloid shift. D major scale: D E F# G A B C#.
No cracked or paid plugin is used or copied. If Mars has a legit paid Antares
licence, the equivalent settings are: Key D Major, Retune Speed 0, Humanize 0,
Flex-Tune 0, Natural Vibrato low — same snap, same key.
Usage: python3 avanna_style_autotune.py <in.wav> <out.wav>
"""
import sys, wave, numpy as np, pyworld as pw
# D major note frequencies (MIDI 50..77: D3..F#5)
SCALE = [0, 2, 4, 5, 7, 9, 11]  # semitones in D major (D=0)
def snap(f):
    if f <= 0: return 0.0
    midi = 69 + 12*np.log2(f/440.0)
    # find nearest D-major midi note
    base = int(np.floor(midi))
    best, bestd = None, 1e9
    for m in range(base-2, base+3):
        if (m - 2) % 12 in SCALE:  # D is midi 2 mod 12
            d = abs(m - midi)
            if d < bestd: best, bestd = m, d
    return 440.0 * 2**((best-69)/12) if best is not None else f

def load(p):
    w = wave.open(p); n = w.getnframes(); sr = w.getframerate(); ch = w.getnchannels()
    d = np.frombuffer(w.readframes(n), dtype=np.int16).astype(float)/32768
    if ch > 1: d = d.reshape(-1, ch).mean(axis=1)
    return d, sr

x, sr = load(sys.argv[1])
f0, t = pw.harvest(x, sr); f0 = pw.stonemask(x, f0, t, sr)
sp = pw.cheaptrick(x, f0, t, sr); ap = pw.d4c(x, f0, t, sr)
f0_shift = np.where(f0 > 0, f0 * 1.682, 0)
f0_tuned = np.array([snap(v) for v in f0_shift])
n_freq = sp.shape[1]; sp_new = np.zeros_like(sp)
for i in range(sp.shape[0]):
    src = np.arange(n_freq) / 1.682
    sp_new[i] = np.interp(np.arange(n_freq), src, sp[i], left=sp[i,0], right=sp[i,-1])
y = pw.synthesize(f0_tuned, sp_new, ap * 0.5, sr)
y = np.clip(y, -0.95, 0.95)
w = wave.open(sys.argv[2], "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((y*32767).astype(np.int16).tobytes()); w.close()
print(f"wrote {sys.argv[2]}: {len(y)/sr:.2f}s, autotune D major, hard snap, F0 x1.682")
