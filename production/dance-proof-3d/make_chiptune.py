#!/usr/bin/env python3
"""Tamagotchi-style chiptune loop generator for the Cape Jones dance proof.

Pure numpy: square-wave lead (toy digital-pet bleep), triangle bass,
tiny noise ticks. Deterministic, no samples, no API. Output: 16-bit WAV.

Usage: python3 make_chiptune.py [duration_seconds] [out.wav]
"""
import sys
import numpy as np
from scipy.io import wavfile

SR = 44100
DURATION = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
OUT = sys.argv[2] if len(sys.argv) > 2 else "chiptune.wav"

BPM = 150.0
EIGHTH = 60.0 / BPM / 2.0  # seconds per eighth note

# Cute pentatonic melody, midi notes, one per eighth. 32 eighths = 2 bars... 
# pattern is 64 eighths (~12.8s) then loops/tiled by timeline fill below.
MELODY = [
    72, 76, 79, 76,  81, 79, 76, 72,   # C E G E | A G E C
    74, 76, 74, 69,  72, -1, 76, -1,   # D E D A | C . E .
    72, 76, 79, 76,  81, 84, 81, 79,   # C E G E | A C' A G
    76, 74, 72, 74,  72, -1, -1, -1,   # E D C D | C . . .
    67, 72, 76, 72,  74, 79, 76, 74,   # G C E C | D G E D
    69, 74, 77, 74,  76, -1, 79, -1,   # A D F D | E . G .
    81, 79, 76, 79,  81, 84, 88, 84,   # A G E G | A C' E' C'
    79, 76, 74, 76,  72, -1, -1, -1,   # G E D E | C . . .
]
# Chord roots per 2 bars of melody (each entry spans 16 eighths): C, F, C, G... 
BASS_ROOTS = [48, 53, 48, 55]  # C3, F3, C3, G3 (midi)

def midi_hz(m):
    return 440.0 * 2.0 ** ((m - 69) / 12.0)

def square(t, freq, duty=0.30):
    ph = (t * freq) % 1.0
    return np.where(ph < duty, 1.0, -1.0)

def tri(t, freq):
    ph = (t * freq) % 1.0
    return 2.0 * np.abs(2.0 * ph - 1.0) - 1.0

def note_env(n, sr):
    """Short plucky envelope: fast attack, exponential decay."""
    t = np.arange(n) / sr
    return np.exp(-t * 6.0) * np.minimum(1.0, t * 200.0)

total = int(SR * DURATION)
mix = np.zeros(total, dtype=np.float64)
rng = np.random.default_rng(20261029)

n_steps = int(DURATION / EIGHTH) + 2
for i in range(n_steps):
    start = int(i * EIGHTH * SR)
    if start >= total:
        break
    seg = int(EIGHTH * SR * 0.95)
    seg = min(seg, total - start)
    if seg <= 0:
        continue
    t = np.arange(seg) / SR
    env = note_env(seg, SR)
    m = MELODY[i % len(MELODY)]
    if m > 0:
        mix[start:start + seg] += 0.30 * square(t, midi_hz(m)) * env
    # bass: one pluck per beat (every 2 eighths)
    if i % 2 == 0:
        root = BASS_ROOTS[(i // 16) % len(BASS_ROOTS)]
        bseg = min(int(EIGHTH * 2 * SR * 0.9), total - start)
        bt = np.arange(bseg) / SR
        mix[start:start + bseg] += 0.22 * tri(bt, midi_hz(root)) * note_env(bseg, SR)
    # toy tick on offbeats
    if i % 2 == 1:
        tseg = min(int(0.03 * SR), total - start)
        noise = rng.standard_normal(tseg) * np.exp(-np.arange(tseg) / (0.008 * SR))
        mix[start:start + tseg] += 0.05 * noise

# gentle master fade at the very ends so the loop point is clean
fade = int(0.05 * SR)
mix[:fade] *= np.linspace(0, 1, fade)
mix[-fade:] *= np.linspace(1, 0, fade)
mix = np.clip(mix, -0.9, 0.9)
wavfile.write(OUT, SR, (mix * 32767).astype(np.int16))
print(f"wrote {OUT}: {DURATION:.1f}s @ {SR} Hz, peak {np.abs(mix).max():.2f}")
